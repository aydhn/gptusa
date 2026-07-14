import unittest
import pandas as pd
from datetime import datetime

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent
from usa_signal_bot.provider_quality.continuity_scorer import (
    continuity_grade,
    detect_timestamp_gaps,
    continuity_score_from_gaps,
    score_continuity,
    continuity_scorer_to_text
)

class TestContinuityScorer(unittest.TestCase):
    def test_continuity_grade(self):
        self.assertEqual(continuity_grade(100.0).value, "EXCELLENT")
        self.assertEqual(continuity_grade(95.0).value, "EXCELLENT")
        self.assertEqual(continuity_grade(85.0).value, "GOOD")
        self.assertEqual(continuity_grade(70.0).value, "ACCEPTABLE")
        self.assertEqual(continuity_grade(50.0).value, "WEAK")
        self.assertEqual(continuity_grade(49.9).value, "POOR")
        self.assertEqual(continuity_grade(0.0).value, "POOR")

    def test_detect_timestamp_gaps(self):
        # < 2 records
        self.assertEqual(detect_timestamp_gaps([]), [])
        self.assertEqual(detect_timestamp_gaps([{"timestamp": "2023-01-01"}]), [])

        # Missing timestamp column
        self.assertEqual(detect_timestamp_gaps([{"date": "2023-01-01"}, {"date": "2023-01-02"}]), ["Missing 'timestamp' column"])

        # No gap
        records = [
            {"timestamp": "2023-01-01"},
            {"timestamp": "2023-01-02"},
            {"timestamp": "2023-01-03"},
            {"timestamp": "2023-01-04"}
        ]
        self.assertEqual(detect_timestamp_gaps(records), [])

        # With large gap (>4 days)
        records_with_gap = [
            {"timestamp": "2023-01-01"},
            {"timestamp": "2023-01-02"},
            {"timestamp": "2023-01-08"}, # 6 day gap
        ]
        gaps = detect_timestamp_gaps(records_with_gap)
        self.assertEqual(len(gaps), 1)
        self.assertIn("Found 1 large gaps (>4 days)", gaps[0])

        # Multiple large gaps
        records_with_multiple_gaps = [
            {"timestamp": "2023-01-01"},
            {"timestamp": "2023-01-02"},
            {"timestamp": "2023-01-08"}, # 6 day gap
            {"timestamp": "2023-01-09"},
            {"timestamp": "2023-01-15"}  # 6 day gap
        ]
        gaps2 = detect_timestamp_gaps(records_with_multiple_gaps)
        self.assertEqual(len(gaps2), 1)
        self.assertIn("Found 2 large gaps (>4 days)", gaps2[0])

    def test_continuity_score_from_gaps(self):
        # < 2 row count
        self.assertEqual(continuity_score_from_gaps(0, 1), 100.0)

        # ratio penalty logic
        self.assertEqual(continuity_score_from_gaps(1, 100), 90.0) # 1 gap / 100 rows * 1000 = 10 -> score 90
        self.assertEqual(continuity_score_from_gaps(5, 100), 50.0)
        self.assertEqual(continuity_score_from_gaps(15, 100), 0.0) # < 0 capped at 0

    def test_score_continuity(self):
        records = [
            {"timestamp": "2023-01-01"},
            {"timestamp": "2023-01-08"},
        ]
        result = score_continuity(records, provider_name="TEST_PROVIDER", symbol="TEST_SYMBOL")

        self.assertEqual(result.provider_name, "TEST_PROVIDER")
        self.assertEqual(result.symbol, "TEST_SYMBOL")
        self.assertEqual(result.component.value, "CONTINUITY")

        # Score calculation: 1 gap, 2 rows => ratio 0.5 * 1000 = 500 penalty => score 0.0
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.grade.value, "POOR")
        self.assertEqual(result.raw_value, 1.0)

        self.assertEqual(len(result.risk_flags), 1)
        self.assertEqual(result.risk_flags[0].value, "CONTINUITY_GAP")

        self.assertEqual(len(result.warnings), 1)
        self.assertIn("Found 1 large gaps (>4 days)", result.warnings[0])

    def test_score_continuity_no_gaps(self):
        records = [
            {"timestamp": "2023-01-01"},
            {"timestamp": "2023-01-02"},
            {"timestamp": "2023-01-03"},
        ]
        result = score_continuity(records, provider_name="TEST_PROVIDER", symbol="TEST_SYMBOL")

        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.grade.value, "EXCELLENT")
        self.assertEqual(result.raw_value, 0.0)

        self.assertEqual(len(result.risk_flags), 0)
        self.assertEqual(len(result.warnings), 0)

    def test_continuity_scorer_to_text(self):
        records = [
            {"timestamp": "2023-01-01"},
            {"timestamp": "2023-01-02"}
        ]
        component = score_continuity(records, provider_name="TEST_PROVIDER", symbol="TEST_SYMBOL")
        text = continuity_scorer_to_text(component)

        self.assertIn("Continuity: 100.0 (EXCELLENT)", text)
        self.assertIn("Continuity scored 100.0 with 0 detected gap warnings", text)

if __name__ == "__main__":
    unittest.main()
