import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.provider_quality.source_trust_model import (
    source_trust_level_from_score,
    trust_score_from_quality_scores,
    build_source_trust_profile,
    source_trust_profile_summary,
    source_trust_profile_to_text
)
from usa_signal_bot.core.enums import SourceTrustLevel, ProviderQualityRiskFlag, DataQualityComponent
from usa_signal_bot.provider_quality.phase109_models import SourceTrustProfile, ProviderDataQualityScore

class TestSourceTrustModel(unittest.TestCase):

    def test_source_trust_level_from_score(self):
        self.assertEqual(source_trust_level_from_score(100.0, blocked=True), SourceTrustLevel.BLOCKED)
        self.assertEqual(source_trust_level_from_score(90.0), SourceTrustLevel.HIGH_TRUST)
        self.assertEqual(source_trust_level_from_score(85.0), SourceTrustLevel.HIGH_TRUST)
        self.assertEqual(source_trust_level_from_score(84.9), SourceTrustLevel.MEDIUM_TRUST)
        self.assertEqual(source_trust_level_from_score(60.0), SourceTrustLevel.MEDIUM_TRUST)
        self.assertEqual(source_trust_level_from_score(59.9), SourceTrustLevel.LOW_TRUST)
        self.assertEqual(source_trust_level_from_score(30.0), SourceTrustLevel.LOW_TRUST)
        self.assertEqual(source_trust_level_from_score(29.9), SourceTrustLevel.UNTRUSTED)
        self.assertEqual(source_trust_level_from_score(0.0), SourceTrustLevel.UNTRUSTED)

    def test_trust_score_from_quality_scores(self):
        self.assertEqual(trust_score_from_quality_scores([]), 50.0)
        self.assertEqual(trust_score_from_quality_scores(None), 50.0)

        qs1 = MagicMock(spec=ProviderDataQualityScore, total_score=80.0)
        qs2 = MagicMock(spec=ProviderDataQualityScore, total_score=90.0)
        self.assertEqual(trust_score_from_quality_scores([qs1, qs2]), 85.0)

    @patch('usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id')
    @patch('usa_signal_bot.provider_quality.source_trust_model.datetime')
    def test_build_source_trust_profile_blocked(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_mocked"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        qs = MagicMock(spec=ProviderDataQualityScore)
        qs.total_score = 90.0
        qs.blocked = True
        qs.components = []

        profile = build_source_trust_profile("TEST_PROVIDER", quality_scores=[qs])
        self.assertEqual(profile.profile_id, "trust_prof_mocked")
        self.assertEqual(profile.created_at_utc, "2023-01-01T00:00:00Z")
        self.assertEqual(profile.provider_name, "TEST_PROVIDER")
        self.assertEqual(profile.trust_score, 90.0)
        self.assertEqual(profile.trust_level, SourceTrustLevel.BLOCKED)
        self.assertNotIn(ProviderQualityRiskFlag.TRUST_SCORE_LOW, profile.risk_flags)

    @patch('usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id')
    @patch('usa_signal_bot.provider_quality.source_trust_model.datetime')
    def test_build_source_trust_profile_components(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_mocked2"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        c1 = MagicMock(component=DataQualityComponent.SCHEMA_VALIDITY, score=90.0)
        c2 = MagicMock(component=DataQualityComponent.SAFETY_COMPLIANCE, score=50.0)

        qs = MagicMock(spec=ProviderDataQualityScore)
        qs.total_score = 40.0
        qs.blocked = False
        qs.components = [c1, c2]

        profile = build_source_trust_profile("TEST_PROVIDER2", quality_scores=[qs])

        self.assertEqual(profile.trust_score, 40.0)
        self.assertEqual(profile.trust_level, SourceTrustLevel.BLOCKED)
        self.assertEqual(profile.schema_reliability_score, 90.0)
        self.assertEqual(profile.safety_reliability_score, 50.0)
        self.assertIn("Safety reliability is below 100, blocking trust.", profile.warnings)

    @patch('usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id')
    @patch('usa_signal_bot.provider_quality.source_trust_model.datetime')
    def test_build_source_trust_profile_low_score(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_mocked3"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        qs = MagicMock(spec=ProviderDataQualityScore)
        qs.total_score = 40.0
        qs.blocked = False
        qs.components = []

        profile = build_source_trust_profile("TEST_PROVIDER3", quality_scores=[qs])
        self.assertEqual(profile.trust_level, SourceTrustLevel.LOW_TRUST)
        self.assertIn(ProviderQualityRiskFlag.TRUST_SCORE_LOW, profile.risk_flags)

    @patch('usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id')
    @patch('usa_signal_bot.provider_quality.source_trust_model.datetime')
    def test_build_source_trust_profile_no_scores(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "trust_prof_mocked4"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        profile = build_source_trust_profile("TEST_PROVIDER4")
        self.assertEqual(profile.trust_score, 50.0)
        self.assertEqual(profile.trust_level, SourceTrustLevel.LOW_TRUST)
        self.assertEqual(profile.schema_reliability_score, None)

    def test_source_trust_profile_summary(self):
        profile = MagicMock(spec=SourceTrustProfile)
        profile.profile_id = "id"
        profile.provider_name = "provider"
        profile.trust_score = 80.0
        profile.trust_level = MagicMock()
        profile.trust_level.value = "HIGH_TRUST"

        summary = source_trust_profile_summary(profile)
        self.assertEqual(summary, {
            "profile_id": "id",
            "provider": "provider",
            "trust_score": 80.0,
            "trust_level": "HIGH_TRUST"
        })

    def test_source_trust_profile_to_text(self):
        profile = MagicMock(spec=SourceTrustProfile)
        profile.provider_name = "provider"
        profile.trust_score = 80.123
        profile.trust_level = MagicMock()
        profile.trust_level.value = "HIGH_TRUST"

        text = source_trust_profile_to_text(profile)
        self.assertEqual(text, "Source Trust Profile: provider | Score: 80.1 (HIGH_TRUST)")

if __name__ == '__main__':
    unittest.main()
