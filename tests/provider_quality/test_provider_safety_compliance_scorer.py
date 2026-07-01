import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.provider_quality.provider_safety_compliance_scorer import (
    SafetyComplianceFlags,
    provider_safety_compliance_grade,
    provider_safety_compliance_score_from_flags,
    score_provider_safety_compliance,
    provider_safety_compliance_to_text,
)

from usa_signal_bot.core.enums import (
    DataQualityGrade,
    ProviderQualityRiskFlag,
    DataQualityComponent,
)


class TestProviderSafetyComplianceScorer(unittest.TestCase):
    def test_provider_safety_compliance_grade(self):
        self.assertEqual(provider_safety_compliance_grade(100.0), DataQualityGrade.EXCELLENT)
        self.assertEqual(provider_safety_compliance_grade(100), DataQualityGrade.EXCELLENT)
        self.assertEqual(provider_safety_compliance_grade(99.9), DataQualityGrade.BLOCKED)
        self.assertEqual(provider_safety_compliance_grade(0.0), DataQualityGrade.BLOCKED)

    def test_provider_safety_compliance_score_from_flags(self):
        flags = SafetyComplianceFlags()
        self.assertEqual(provider_safety_compliance_score_from_flags(flags.to_dict()), 100.0)

        flags.network_used = True
        self.assertEqual(provider_safety_compliance_score_from_flags(flags.to_dict()), 0.0)

    @patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.datetime")
    def test_score_provider_safety_compliance_happy_path(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_safety_1"
        mock_datetime.datetime.now.return_value = MagicMock(
            isoformat=MagicMock(return_value="2023-01-01T00:00:00+00:00")
        )
        mock_datetime.timezone = MagicMock()
        mock_datetime.timezone.utc = "UTC"

        flags = SafetyComplianceFlags()
        result = score_provider_safety_compliance("SAFE_PROV", flags, "BTC")

        self.assertEqual(result.component_id, "dq_comp_safety_1")
        self.assertEqual(result.created_at_utc, "2023-01-01T00:00:00Z")
        self.assertEqual(result.provider_name, "SAFE_PROV")
        self.assertEqual(result.symbol, "BTC")
        self.assertEqual(result.component, DataQualityComponent.SAFETY_COMPLIANCE)
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.grade, DataQualityGrade.EXCELLENT)
        self.assertEqual(result.risk_flags, [])
        self.assertEqual(result.errors, [])
        self.assertIn("Safety Compliance scored 100.0", result.explanation)

    @patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.datetime")
    def test_score_provider_safety_compliance_with_flags(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_safety_2"
        mock_datetime.datetime.now.return_value = MagicMock(
            isoformat=MagicMock(return_value="2023-01-01T00:00:00+00:00")
        )
        mock_datetime.timezone = MagicMock()
        mock_datetime.timezone.utc = "UTC"

        flags = SafetyComplianceFlags(network_used=True, broker_used=True)
        result = score_provider_safety_compliance("UNSAFE_PROV", flags)

        self.assertEqual(result.provider_name, "UNSAFE_PROV")
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.grade, DataQualityGrade.BLOCKED)
        self.assertIn(ProviderQualityRiskFlag.NETWORK_FETCH_ATTEMPTED, result.risk_flags)
        self.assertIn(ProviderQualityRiskFlag.BROKER_RISK, result.risk_flags)
        self.assertIn("network_used=True", result.errors)
        self.assertIn("broker_used=True", result.errors)
        self.assertIn("Safety Compliance scored 0.0", result.explanation)

    @patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.datetime")
    def test_provider_safety_compliance_to_text(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_safety_3"
        mock_datetime.datetime.now.return_value = MagicMock(
            isoformat=MagicMock(return_value="2023-01-01T00:00:00+00:00")
        )
        mock_datetime.timezone = MagicMock()
        mock_datetime.timezone.utc = "UTC"

        flags = SafetyComplianceFlags()
        result = score_provider_safety_compliance("TEXT_PROV", flags)
        text = provider_safety_compliance_to_text(result)

        self.assertIn("Safety Compliance: 100.0", text)
        self.assertIn("EXCELLENT", text)

if __name__ == '__main__':
    unittest.main()
