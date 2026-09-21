from __future__ import annotations

import csv
import json
import re
import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.analyze import (  # noqa: E402
    GROUP_ORDER,
    METRICS,
    belief_group,
    build_outputs,
)


class MappingTests(unittest.TestCase):
    def test_religion_groups_are_mutually_exclusive(self) -> None:
        expected = {
            1: "Christian",
            2: "Christian",
            10: "Christian",
            11: "Christian",
            13: "Christian",
            3: "Other faith",
            5: "Other faith",
            6: "Other faith",
            7: "Other faith",
            8: "Other faith",
            9: "Other faith",
            12: "Other faith",
            4: "No religious affiliation",
        }
        self.assertEqual({code: belief_group(code) for code in expected}, expected)
        self.assertIsNone(belief_group(float("nan")))
        self.assertIsNone(belief_group(99))


class OutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.output, cls.quality = build_outputs()

    def test_public_schema(self) -> None:
        expected_columns = [
            "belief_group",
            "metric_id",
            "metric_label",
            "estimate",
            "ci_low",
            "ci_high",
            "unit",
            "unweighted_n",
            "source_year",
            "sort_order",
        ]
        self.assertEqual(list(self.output.columns), expected_columns)

    def test_complete_metric_group_grid(self) -> None:
        self.assertEqual(len(self.output), len(METRICS) * len(GROUP_ORDER))
        self.assertEqual(set(self.output["belief_group"]), set(GROUP_ORDER))

    def test_estimates_and_intervals_are_valid(self) -> None:
        self.assertTrue(self.output["estimate"].between(0, 100).all())
        self.assertTrue(self.output["ci_low"].between(0, 100).all())
        self.assertTrue(self.output["ci_high"].between(0, 100).all())
        self.assertTrue((self.output["ci_low"] <= self.output["estimate"]).all())
        self.assertTrue((self.output["estimate"] <= self.output["ci_high"]).all())
        self.assertTrue((self.output["unweighted_n"] > 0).all())

    def test_reviewed_release_counts(self) -> None:
        self.assertEqual(self.quality["raw_rows"], 4149)
        self.assertEqual(self.quality["weighted_core_rows"], 3544)
        self.assertEqual(self.quality["rows_excluded_missing_weight"], 605)
        self.assertEqual(self.quality["eligible_grouped_rows"], 3483)
        self.assertFalse(self.quality["respondent_level_data_published"])

    def test_results_match_reviewed_values(self) -> None:
        expected = {
            ("good_or_better_pct", "Christian"): 72.45,
            ("good_or_better_pct", "Other faith"): 75.85,
            ("good_or_better_pct", "No religious affiliation"): 70.96,
            ("physical_8plus_pct", "Christian"): 8.48,
            ("physical_8plus_pct", "Other faith"): 8.83,
            ("physical_8plus_pct", "No religious affiliation"): 11.10,
            ("mental_8plus_pct", "Christian"): 14.65,
            ("mental_8plus_pct", "Other faith"): 22.52,
            ("mental_8plus_pct", "No religious affiliation"): 25.42,
        }
        indexed = self.output.set_index(["metric_id", "belief_group"])["estimate"]
        for key, value in expected.items():
            self.assertAlmostEqual(float(indexed.loc[key]), value, places=2)


class PowerBIProjectTests(unittest.TestCase):
    """Keep the aggregate-only PBIP table synchronized with the reviewed CSV."""

    PBIP_ROOT = ROOT / "powerbi" / "project" / "ChristianWellbeing2022"
    TABLE_FILE = (
        PBIP_ROOT
        / "ChristianWellbeing2022.SemanticModel"
        / "definition"
        / "tables"
        / "ChartData.tmdl"
    )
    PAGES_ROOT = PBIP_ROOT / "ChristianWellbeing2022.Report" / "definition" / "pages"
    ROW_PATTERN = re.compile(
        r'\{"([^"]+)", "([^"]+)", "([^"]+)", '
        r'([0-9.]+), ([0-9.]+), ([0-9.]+), "([^"]+)", '
        r'(\d+), (\d+), (\d+)\}'
    )

    @staticmethod
    def _normalized_row(values: list[str] | tuple[str, ...]) -> tuple[object, ...]:
        return (
            values[0], values[1], values[2],
            round(float(values[3]), 2),
            round(float(values[4]), 2),
            round(float(values[5]), 2),
            values[6], int(values[7]), int(values[8]), int(values[9]),
        )

    def test_embedded_chart_data_matches_csv(self) -> None:
        with (ROOT / "data" / "processed" / "chart_data.csv").open(
            newline="", encoding="utf-8"
        ) as source:
            csv_rows = [
                self._normalized_row(tuple(row.values()))
                for row in csv.DictReader(source)
            ]
        tmdl_rows = [
            self._normalized_row(match)
            for match in self.ROW_PATTERN.findall(
                self.TABLE_FILE.read_text(encoding="utf-8")
            )
        ]
        self.assertEqual(tmdl_rows, csv_rows)

    def test_pbip_contains_no_private_or_binary_inputs(self) -> None:
        tracked_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in self.PBIP_ROOT.rglob("*")
            if path.is_file() and path.suffix in {".pbip", ".pbir", ".json", ".tmdl", ".pbism"}
        )
        self.assertNotIn("GSS 2024", tracked_text)
        self.assertNotRegex(tracked_text, r"[A-Za-z]:[\\/]Users[\\/]")
        self.assertFalse(any(self.PBIP_ROOT.rglob("*.pbix")))
        self.assertFalse(any(self.PBIP_ROOT.rglob("*.pbit")))

    def test_required_pages_measures_and_accessibility_metadata_exist(self) -> None:
        pages = (
            self.PBIP_ROOT
            / "ChristianWellbeing2022.Report"
            / "definition"
            / "pages"
            / "pages.json"
        ).read_text(encoding="utf-8")
        model = self.TABLE_FILE.read_text(encoding="utf-8")
        visuals = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.PBIP_ROOT.rglob("visual.json")
        )
        self.assertLess(pages.index('"MentalHealth"'), pages.index('"FullHealthOverview"'))
        self.assertIn('"activePageName": "MentalHealth"', pages)
        for measure in (
            "Estimate %", "CI Low %", "CI High %", "Valid Respondents", "Source Label",
        ):
            self.assertIn(f"measure '{measure}'", model)
        self.assertEqual(visuals.count('"altText"'), 4)
        self.assertEqual(visuals.count('"errorRange"'), 4)

    def test_charts_bind_metric_specific_bounds_and_fixed_scales(self) -> None:
        charts = {
            ("MentalHealth", "Dashboard_current"): ("Mental Health", "0.35D"),
            ("FullHealthOverview", "Growth_current"): ("General Health", "1D"),
            ("FullHealthOverview", "Growth_gain"): ("Physical Health", "0.35D"),
            ("FullHealthOverview", "Growth_gain_history"): ("Mental Health", "0.35D"),
        }
        for (page, visual_name), (metric, axis_max) in charts.items():
            with self.subTest(page=page, visual=visual_name):
                path = self.PAGES_ROOT / page / "visuals" / visual_name / "visual.json"
                visual = json.loads(path.read_text(encoding="utf-8"))["visual"]
                self.assertEqual(visual["visualType"], "clusteredBarChart")
                query = visual["query"]["queryState"]
                self.assertEqual(
                    query["Y"]["projections"][0]["field"]["Measure"]["Property"],
                    f"{metric} %",
                )
                tooltip_measures = {
                    projection["field"]["Measure"]["Property"]
                    for projection in query["Tooltips"]["projections"]
                }
                self.assertEqual(
                    tooltip_measures,
                    {f"{metric} CI Low %", f"{metric} CI High %", f"{metric} Respondents"},
                )
                axis = visual["objects"]["valueAxis"][0]["properties"]
                self.assertEqual(axis["start"]["expr"]["Literal"]["Value"], "0D")
                self.assertEqual(axis["end"]["expr"]["Literal"]["Value"], axis_max)
                bounds = visual["objects"]["error"][0]["properties"]["errorRange"]["explicit"]
                self.assertEqual(
                    bounds["lowerBound"]["expr"]["Measure"]["Property"],
                    f"{metric} CI Low %",
                )
                self.assertEqual(
                    bounds["upperBound"]["expr"]["Measure"]["Property"],
                    f"{metric} CI High %",
                )
                self.assertEqual(bounds["isRelative"]["expr"]["Literal"]["Value"], "false")


if __name__ == "__main__":
    unittest.main()
