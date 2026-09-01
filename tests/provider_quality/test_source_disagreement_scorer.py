import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.provider_quality.source_disagreement_scorer import (
    source_agreement_grade,
    source_agreement_score_from_disagreement,
    score_source_agreement,
    source_disagreement_scorer_to_text,
)

from usa_signal_bot.core.enums import (
    DataQualityGrade,
    ProviderQualityRiskFlag,
    DataQualityComponent,
)

class TestSourceDisagreementScorer(unittest.TestCase):

    def test_source_agreement_grade(self):
        self.assertEqual(source_agreement_grade(100.0), DataQualityGrade.EXCELLENT)
        self.assertEqual(source_agreement_grade(90.0), DataQualityGrade.EXCELLENT)
        self.assertEqual(source_agreement_grade(89.9), DataQualityGrade.GOOD)
        self.assertEqual(source_agreement_grade(75.0), DataQualityGrade.GOOD)
        self.assertEqual(source_agreement_grade(74.9), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(source_agreement_grade(50.0), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(source_agreement_grade(49.9), DataQualityGrade.WEAK)
        self.assertEqual(source_agreement_grade(30.0), DataQualityGrade.WEAK)
        self.assertEqual(source_agreement_grade(29.9), DataQualityGrade.POOR)
        self.assertEqual(source_agreement_grade(0.0), DataQualityGrade.POOR)

    def test_source_agreement_score_from_disagreement(self):
        self.assertEqual(source_agreement_score_from_disagreement(None), 50.0)
        self.assertEqual(source_agreement_score_from_disagreement(0.1), 100.0)
        self.assertEqual(source_agreement_score_from_disagreement(0.5), 100.0)
        self.assertEqual(source_agreement_score_from_disagreement(0.6), 90.0)
        self.assertEqual(source_agreement_score_from_disagreement(1.0), 90.0)
        self.assertEqual(source_agreement_score_from_disagreement(1.1), 75.0)
        self.assertEqual(source_agreement_score_from_disagreement(2.0), 75.0)
        self.assertEqual(source_agreement_score_from_disagreement(2.1), 50.0)
        self.assertEqual(source_agreement_score_from_disagreement(5.0), 50.0)
        self.assertEqual(source_agreement_score_from_disagreement(6.0), 40.0)
        self.assertEqual(source_agreement_score_from_disagreement(10.0), 0.0)
        self.assertEqual(source_agreement_score_from_disagreement(15.0), 0.0)

    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.datetime")
    def test_score_source_agreement(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_test1"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_source_agreement(2.5, provider_name="TEST_PROV", symbol="BTC")

        self.assertEqual(result.component_id, "dq_comp_test1")
        self.assertEqual(result.created_at_utc, "2023-01-01T00:00:00Z")
        self.assertEqual(result.provider_name, "TEST_PROV")
        self.assertEqual(result.symbol, "BTC")
        self.assertEqual(result.component, DataQualityComponent.SOURCE_AGREEMENT)
        self.assertEqual(result.raw_value, 2.5)
        self.assertEqual(result.score, 50.0)
        self.assertEqual(result.weight, 0.0)
        self.assertEqual(result.weighted_score, 0.0)
        self.assertEqual(result.grade, DataQualityGrade.ACCEPTABLE)
        self.assertIn("Source Agreement scored 50.0 based on 2.5% disagreement", result.explanation)
        self.assertEqual(result.risk_flags, [])
        self.assertEqual(result.warnings, [])

    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.datetime")
    def test_score_source_agreement_none(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_test2"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_source_agreement(None, provider_name="TEST_PROV2")

        self.assertEqual(result.raw_value, None)
        self.assertEqual(result.score, 50.0)
        self.assertEqual(result.grade, DataQualityGrade.ACCEPTABLE)
        self.assertIn("Source Agreement scored 50.0 based on unknown% disagreement", result.explanation)
        self.assertEqual(result.risk_flags, [])
        self.assertEqual(result.warnings, ["No source comparison disagreement score available"])

    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.datetime")
    def test_score_source_agreement_high(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_test3"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_source_agreement(6.0, provider_name="TEST_PROV3")

        self.assertEqual(result.raw_value, 6.0)
        self.assertEqual(result.score, 40.0)
        self.assertEqual(result.grade, DataQualityGrade.WEAK)
        self.assertIn(ProviderQualityRiskFlag.SOURCE_DISAGREEMENT_HIGH, result.risk_flags)
        self.assertEqual(result.warnings, ["High disagreement score: 6.0%"])

    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.source_disagreement_scorer.datetime")
    def test_source_disagreement_scorer_to_text(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_test4"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_source_agreement(1.0, provider_name="PROV")
        text = source_disagreement_scorer_to_text(result)

        self.assertIn("Source Agreement: 90.0", text)
        self.assertIn("EXCELLENT", text)
        self.assertIn("Source Agreement scored 90.0 based on 1.0% disagreement", text)

if __name__ == "__main__":
    unittest.main()
