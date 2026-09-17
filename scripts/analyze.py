"""Create survey-weighted aggregate health estimates for Power BI.

The public output contains aggregate estimates only. Respondent-level data
remains in data/raw, which is excluded from version control.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "2022" / "GSS2022.dta"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_CSV = PROCESSED_DIR / "chart_data.csv"
QUALITY_JSON = PROCESSED_DIR / "quality_report.json"

REQUIRED_COLUMNS = {
    "relig",
    "health",
    "physhlth",
    "mntlhlth",
    "wtssnrps",
    "vstrat",
    "vpsu",
}

GROUP_ORDER = {
    "Christian": 1,
    "Other faith": 2,
    "No religious affiliation": 3,
}

CHRISTIAN_CODES = {1, 2, 10, 11, 13}
OTHER_FAITH_CODES = {3, 5, 6, 7, 8, 9, 12}
NO_AFFILIATION_CODES = {4}


@dataclass(frozen=True)
class Metric:
    metric_id: str
    metric_label: str
    source_column: str
    valid: Callable[[pd.Series], pd.Series]
    event: Callable[[pd.Series], pd.Series]


METRICS = (
    Metric(
        "good_or_better_pct",
        "Excellent or good general health",
        "health",
        lambda s: s.isin([1, 2, 3, 4]),
        lambda s: s.isin([1, 2]),
    ),
    Metric(
        "physical_8plus_pct",
        "8+ physically unhealthy days (past 30 days)",
        "physhlth",
        lambda s: s.between(0, 30),
        lambda s: s >= 8,
    ),
    Metric(
        "mental_8plus_pct",
        "8+ mentally unhealthy days (past 30 days)",
        "mntlhlth",
        lambda s: s.between(0, 30),
        lambda s: s >= 8,
    ),
)


def belief_group(code: float) -> str | None:
    if pd.isna(code):
        return None
    value = int(code)
    if value in CHRISTIAN_CODES:
        return "Christian"
    if value in OTHER_FAITH_CODES:
        return "Other faith"
    if value in NO_AFFILIATION_CODES:
        return "No religious affiliation"
    return None


def survey_proportion(
    design_frame: pd.DataFrame,
    domain: pd.Series,
    event: pd.Series,
) -> tuple[float, float, float, float]:
    """Return estimate, lower CI, upper CI, and standard error.

    Variance uses a Taylor-linearized ratio estimator. Linearized values are
    aggregated to PSU within variance stratum before the between-PSU sum of
    squares is calculated. A normal 1.96 critical value is used for the 95% CI.
    """

    if not design_frame.index.equals(domain.index) or not design_frame.index.equals(event.index):
        raise ValueError("Domain, event, and design frame indexes must match")

    weights = design_frame["wtssnrps"].to_numpy(dtype=float)
    domain_values = domain.to_numpy(dtype=bool)
    outcome = event.to_numpy(dtype=float)
    denominator = float(weights[domain_values].sum())
    if denominator <= 0:
        raise ValueError("Survey-weight denominator must be positive")

    estimate = float(np.sum(weights[domain_values] * outcome[domain_values]) / denominator)
    work = design_frame[["vstrat", "vpsu", "wtssnrps"]].copy()
    work["linearized"] = (
        work["wtssnrps"]
        * domain_values.astype(float)
        * (outcome - estimate)
        / denominator
    )
    psu_totals = (
        work.groupby(["vstrat", "vpsu"], observed=True)["linearized"]
        .sum()
        .reset_index()
    )

    variance = 0.0
    singleton_strata: list[int] = []
    for stratum, values in psu_totals.groupby("vstrat", observed=True)["linearized"]:
        psu_values = values.to_numpy(dtype=float)
        count = len(psu_values)
        if count < 2:
            singleton_strata.append(int(stratum))
            continue
        variance += count / (count - 1) * float(np.sum((psu_values - psu_values.mean()) ** 2))

    if singleton_strata:
        raise ValueError(f"Singleton variance strata encountered: {singleton_strata}")

    standard_error = math.sqrt(max(variance, 0.0))
    lower = max(0.0, estimate - 1.96 * standard_error)
    upper = min(1.0, estimate + 1.96 * standard_error)
    return estimate, lower, upper, standard_error


def build_outputs(raw_data: Path = RAW_DATA) -> tuple[pd.DataFrame, dict]:
    if not raw_data.exists():
        raise FileNotFoundError(
            f"Missing {raw_data}. Run scripts/download_data.py before analysis."
        )

    frame = pd.read_stata(
        raw_data,
        columns=sorted(REQUIRED_COLUMNS),
        convert_categoricals=False,
    )
    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Required GSS columns are missing: {sorted(missing_columns)}")

    raw_rows = len(frame)
    frame = frame.assign(belief_group=frame["relig"].map(belief_group))
    weighted_core = frame[frame["wtssnrps"].notna() & (frame["wtssnrps"] > 0)].copy()
    eligible = weighted_core[
        weighted_core["belief_group"].notna()
        & weighted_core["vstrat"].notna()
        & weighted_core["vpsu"].notna()
    ].copy()

    rows: list[dict] = []
    metric_valid_rows: dict[str, int] = {}
    for metric in METRICS:
        valid_mask = metric.valid(eligible[metric.source_column])
        event = metric.event(eligible[metric.source_column]).astype(float)
        metric_valid_rows[metric.metric_id] = int(valid_mask.sum())

        for group, sort_order in GROUP_ORDER.items():
            domain = valid_mask & (eligible["belief_group"] == group)
            estimate, lower, upper, standard_error = survey_proportion(
                eligible,
                domain,
                event,
            )
            rows.append(
                {
                    "belief_group": group,
                    "metric_id": metric.metric_id,
                    "metric_label": metric.metric_label,
                    "estimate": round(estimate * 100, 2),
                    "ci_low": round(lower * 100, 2),
                    "ci_high": round(upper * 100, 2),
                    "unit": "% of adults",
                    "unweighted_n": int(domain.sum()),
                    "source_year": 2022,
                    "sort_order": sort_order,
                }
            )

    output = pd.DataFrame(rows).sort_values(["metric_id", "sort_order"], kind="stable")
    quality = {
        "raw_rows": raw_rows,
        "weighted_core_rows": int(len(weighted_core)),
        "rows_excluded_missing_weight": int(frame["wtssnrps"].isna().sum()),
        "eligible_grouped_rows": int(len(eligible)),
        "rows_excluded_unmapped_or_missing_religion": int(len(weighted_core) - len(eligible)),
        "belief_group_counts": {
            key: int(value)
            for key, value in eligible["belief_group"].value_counts().sort_index().items()
        },
        "metric_valid_rows": metric_valid_rows,
        "weight": "WTSSNRPS",
        "variance_design": "VSTRAT + VPSU; Taylor-linearized ratio estimator",
        "confidence_level": 0.95,
        "respondent_level_data_published": False,
    }
    return output, quality


def main() -> None:
    output, quality = build_outputs()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_CSV, index=False, lineterminator="\n")
    QUALITY_JSON.write_text(json.dumps(quality, indent=2) + "\n", encoding="utf-8")
    print(output.to_string(index=False))
    print(f"\nWrote {OUTPUT_CSV}")
    print(f"Wrote {QUALITY_JSON}")


if __name__ == "__main__":
    main()
