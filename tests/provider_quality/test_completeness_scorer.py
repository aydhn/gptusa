import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.core.enums import DataQualityGrade, ProviderQualityRiskFlag, DataQualityComponent
from usa_signal_bot.provider_quality.completeness_scorer import (
    completeness_grade,
    missing_value_rate,
    completeness_ratio,
    score_completeness,
    completeness_scorer_to_text
)
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent

class TestCompletenessScorer(unittest.TestCase):

    def test_completeness_grade(self):
        self.assertEqual(completeness_grade(96.0), DataQualityGrade.EXCELLENT)
        self.assertEqual(completeness_grade(95.0), DataQualityGrade.EXCELLENT)
        self.assertEqual(completeness_grade(85.0), DataQualityGrade.GOOD)
        self.assertEqual(completeness_grade(75.0), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(completeness_grade(70.0), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(completeness_grade(55.0), DataQualityGrade.WEAK)
        self.assertEqual(completeness_grade(50.0), DataQualityGrade.WEAK)
        self.assertEqual(completeness_grade(49.9), DataQualityGrade.POOR)
        self.assertEqual(completeness_grade(0.0), DataQualityGrade.POOR)

    def test_missing_value_rate(self):
        required = ["A", "B"]

        # Empty records
        self.assertEqual(missing_value_rate([], required), 1.0)

        # Zero expected (empty required columns)
        self.assertEqual(missing_value_rate([{"A": 1}], []), 0.0)

        # No missing
        records = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
        self.assertEqual(missing_value_rate(records, required), 0.0)

        # Some missing
        records_partial = [{"A": 1, "B": None}, {"A": None, "C": 5}]
        # Record 1: B is None (1 missing)
        # Record 2: A is None (1 missing), B is missing entirely (1 missing) -> 2 missing
        # Total expected = 2 * 2 = 4, Total missing = 3
        self.assertEqual(missing_value_rate(records_partial, required), 0.75)

    def test_completeness_ratio(self):
        required = ["A", "B"]
        records = [{"A": 1, "B": None}, {"A": None, "C": 5}]
        # missing rate is 0.75, so ratio should be 0.25
        self.assertEqual(completeness_ratio(records, required), 0.25)

    @patch("usa_signal_bot.provider_quality.completeness_scorer.datetime")
    @patch("usa_signal_bot.provider_quality.completeness_scorer.create_data_quality_component_id")
    def test_score_completeness_empty_records(self, mock_create_id, mock_datetime):
        mock_create_id.return_value = "test-comp-id"
        mock_datetime.datetime.utcnow.return_value.isoformat.return_value = "2023-01-01T00:00:00"

        result = score_completeness([], provider_name="TestProvider", symbol="AAPL")

        self.assertEqual(result.component_id, "test-comp-id")
        self.assertEqual(result.created_at_utc, "2023-01-01T00:00:00Z")
        self.assertEqual(result.provider_name, "TestProvider")
        self.assertEqual(result.symbol, "AAPL")
        self.assertEqual(result.component, DataQualityComponent.COMPLETENESS)
        self.assertEqual(result.raw_value, 0.0)
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.grade, DataQualityGrade.POOR)
        self.assertIn("Empty records list provided", result.warnings)
        self.assertIn(ProviderQualityRiskFlag.COMPLETENESS_LOW, result.risk_flags)
        self.assertEqual(result.explanation, "Completeness is 0.0% based on 0 records.")

    @patch("usa_signal_bot.provider_quality.completeness_scorer.datetime")
    @patch("usa_signal_bot.provider_quality.completeness_scorer.create_data_quality_component_id")
    def test_score_completeness_low_ratio(self, mock_create_id, mock_datetime):
        mock_create_id.return_value = "test-comp-id"
        mock_datetime.datetime.utcnow.return_value.isoformat.return_value = "2023-01-01T00:00:00"

        # 3 missing out of 4 expected = 0.75 missing, 0.25 ratio -> score 25.0
        records = [{"open": 1}, {"close": 1}]
        required = ["open", "close"]
        result = score_completeness(records, required_columns=required)

        self.assertEqual(result.raw_value, 0.5)
        self.assertEqual(result.score, 50.0)
        self.assertEqual(result.grade, DataQualityGrade.WEAK)
        self.assertTrue(any("High missing value rate" in w for w in result.warnings))
        self.assertIn(ProviderQualityRiskFlag.COMPLETENESS_LOW, result.risk_flags)

    @patch("usa_signal_bot.provider_quality.completeness_scorer.datetime")
    @patch("usa_signal_bot.provider_quality.completeness_scorer.create_data_quality_component_id")
    def test_score_completeness_high_ratio(self, mock_create_id, mock_datetime):
        mock_create_id.return_value = "test-comp-id"
        mock_datetime.datetime.utcnow.return_value.isoformat.return_value = "2023-01-01T00:00:00"

        records = [
            {"open": 1, "high": 2, "low": 1, "close": 2, "volume": 100},
            {"open": 2, "high": 3, "low": 2, "close": 3, "volume": 200}
        ]
        # Uses default columns
        result = score_completeness(records)

        self.assertEqual(result.raw_value, 1.0)
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.grade, DataQualityGrade.EXCELLENT)
        self.assertEqual(len(result.warnings), 0)
        self.assertEqual(len(result.risk_flags), 0)

    def test_completeness_scorer_to_text(self):
        component = DataQualityScoreComponent(
            component_id="id1",
            created_at_utc="2023-01-01T00:00:00Z",
            provider_name="Prov1",
            symbol="SYM1",
            component=DataQualityComponent.COMPLETENESS,
            raw_value=0.9,
            score=90.0,
            weight=0.0,
            weighted_score=0.0,
            grade=DataQualityGrade.GOOD,
            explanation="Completeness is 90.0% based on 10 records.",
            risk_flags=[],
            warnings=[]
        )
        text = completeness_scorer_to_text(component)
        self.assertEqual(text, f"Completeness: 90.0 (GOOD) - Completeness is 90.0% based on 10 records.")

if __name__ == "__main__":
    unittest.main()
