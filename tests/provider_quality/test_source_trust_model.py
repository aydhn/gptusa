import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.provider_quality.source_trust_model import (
    source_trust_level_from_score,
    trust_score_from_quality_scores,
    build_source_trust_profile,
    source_trust_profile_summary,
    source_trust_profile_to_text,
)

from usa_signal_bot.core.enums import (
    SourceTrustLevel,
    ProviderQualityRiskFlag,
    DataQualityComponent,
)

class TestSourceTrustModel(unittest.TestCase):
    def test_source_trust_level_from_score(self):
        self.assertEqual(source_trust_level_from_score(100.0, blocked=True), SourceTrustLevel.BLOCKED)
        self.assertEqual(source_trust_level_from_score(85.0), SourceTrustLevel.HIGH_TRUST)
        self.assertEqual(source_trust_level_from_score(60.0), SourceTrustLevel.MEDIUM_TRUST)
        self.assertEqual(source_trust_level_from_score(30.0), SourceTrustLevel.LOW_TRUST)
        self.assertEqual(source_trust_level_from_score(29.9), SourceTrustLevel.UNTRUSTED)

    def test_trust_score_from_quality_scores(self):
        self.assertEqual(trust_score_from_quality_scores([]), 50.0)

        qs1 = MagicMock(total_score=80.0)
        qs2 = MagicMock(total_score=90.0)
        self.assertEqual(trust_score_from_quality_scores([qs1, qs2]), 85.0)

    @patch("usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id")
    @patch("usa_signal_bot.provider_quality.source_trust_model.datetime")
    def test_build_source_trust_profile_medium_trust(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_123"
        mock_datetime.datetime.utcnow.return_value = MagicMock(isoformat=lambda: "2023-01-01T00:00:00")

        comp1 = MagicMock(component=DataQualityComponent.SCHEMA_VALIDITY, score=90.0)
        comp2 = MagicMock(component=DataQualityComponent.SAFETY_COMPLIANCE, score=100.0)
        qs1 = MagicMock(blocked=False, total_score=80.0, components=[comp1, comp2])

        profile = build_source_trust_profile("TEST_PROV", quality_scores=[qs1])

        self.assertEqual(profile.provider_name, "TEST_PROV")
        self.assertEqual(profile.trust_score, 80.0)
        self.assertEqual(profile.schema_reliability_score, 90.0)
        self.assertEqual(profile.safety_reliability_score, 100.0)
        self.assertEqual(profile.trust_level, SourceTrustLevel.MEDIUM_TRUST)
        self.assertEqual(profile.warnings, [])
        self.assertEqual(profile.risk_flags, [])

    @patch("usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id")
    @patch("usa_signal_bot.provider_quality.source_trust_model.datetime")
    def test_build_source_trust_profile_blocked_safety(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_123"
        mock_datetime.datetime.utcnow.return_value = MagicMock(isoformat=lambda: "2023-01-01T00:00:00")

        comp1 = MagicMock(component=DataQualityComponent.SCHEMA_VALIDITY, score=90.0)
        comp2 = MagicMock(component=DataQualityComponent.SAFETY_COMPLIANCE, score=95.0)
        qs1 = MagicMock(blocked=False, total_score=80.0, components=[comp1, comp2])

        profile = build_source_trust_profile("TEST_PROV", quality_scores=[qs1])

        self.assertEqual(profile.trust_level, SourceTrustLevel.BLOCKED)
        self.assertIn("Safety reliability is below 100, blocking trust.", profile.warnings)
        self.assertEqual(profile.risk_flags, [])

    @patch("usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id")
    @patch("usa_signal_bot.provider_quality.source_trust_model.datetime")
    def test_build_source_trust_profile_low_trust(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_123"
        mock_datetime.datetime.utcnow.return_value = MagicMock(isoformat=lambda: "2023-01-01T00:00:00")

        qs1 = MagicMock(blocked=False, total_score=30.0, components=[])

        profile = build_source_trust_profile("TEST_PROV", quality_scores=[qs1])

        self.assertEqual(profile.trust_level, SourceTrustLevel.LOW_TRUST)
        self.assertIn(ProviderQualityRiskFlag.TRUST_SCORE_LOW, profile.risk_flags)

    @patch("usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id")
    @patch("usa_signal_bot.provider_quality.source_trust_model.datetime")
    def test_build_source_trust_profile_blocked_qs(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_123"
        mock_datetime.datetime.utcnow.return_value = MagicMock(isoformat=lambda: "2023-01-01T00:00:00")

        qs1 = MagicMock(blocked=True, total_score=80.0, components=[])

        profile = build_source_trust_profile("TEST_PROV", quality_scores=[qs1])

        self.assertEqual(profile.trust_level, SourceTrustLevel.BLOCKED)

    def test_source_trust_profile_summary(self):
        profile = MagicMock(
            profile_id="123", provider_name="PROV", trust_score=85.0,
            trust_level=MagicMock(value="HIGH_TRUST")
        )
        summary = source_trust_profile_summary(profile)
        self.assertEqual(summary["profile_id"], "123")
        self.assertEqual(summary["provider"], "PROV")
        self.assertEqual(summary["trust_score"], 85.0)
        self.assertEqual(summary["trust_level"], "HIGH_TRUST")

    def test_source_trust_profile_to_text(self):
        profile = MagicMock(
            provider_name="PROV", trust_score=85.0,
            trust_level=MagicMock(value="HIGH_TRUST")
        )
        text = source_trust_profile_to_text(profile)
        self.assertEqual(text, "Source Trust Profile: PROV | Score: 85.0 (HIGH_TRUST)")

if __name__ == '__main__':
    unittest.main()
