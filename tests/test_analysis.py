from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()

