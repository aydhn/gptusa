import unittest
from unittest.mock import patch, MagicMock
import datetime

# Dummy fallbacks for out-of-scope missing dependencies in sys.modules during test collection
try:
    from usa_signal_bot.core.enums import SourceTrustLevel, ProviderQualityRiskFlag, DataQualityComponent
except ImportError:
    class DummyEnum:
        def __init__(self, value):
            self.value = value
            self.name = value

    class SourceTrustLevel:
        BLOCKED = DummyEnum("BLOCKED")
        HIGH_TRUST = DummyEnum("HIGH_TRUST")
        MEDIUM_TRUST = DummyEnum("MEDIUM_TRUST")
        LOW_TRUST = DummyEnum("LOW_TRUST")
        UNTRUSTED = DummyEnum("UNTRUSTED")

    class ProviderQualityRiskFlag:
        TRUST_SCORE_LOW = DummyEnum("TRUST_SCORE_LOW")

    class DataQualityComponent:
        SCHEMA_VALIDITY = DummyEnum("SCHEMA_VALIDITY")
        FRESHNESS = DummyEnum("FRESHNESS")
        SOURCE_AGREEMENT = DummyEnum("SOURCE_AGREEMENT")
        CACHE_RELIABILITY = DummyEnum("CACHE_RELIABILITY")
        SAFETY_COMPLIANCE = DummyEnum("SAFETY_COMPLIANCE")

try:
    from usa_signal_bot.provider_quality.phase109_models import SourceTrustProfile, ProviderDataQualityScore
except ImportError:
    class SourceTrustProfile:
        pass
    class ProviderDataQualityScore:
        pass

from usa_signal_bot.provider_quality.source_trust_model import (
    source_trust_level_from_score,
    trust_score_from_quality_scores,
    build_source_trust_profile,
    source_trust_profile_summary,
    source_trust_profile_to_text
)

class TestSourceTrustModel(unittest.TestCase):

    def test_source_trust_level_from_score(self):
        self.assertEqual(source_trust_level_from_score(90).value, "HIGH_TRUST")
        self.assertEqual(source_trust_level_from_score(85).value, "HIGH_TRUST")
        self.assertEqual(source_trust_level_from_score(84.9).value, "MEDIUM_TRUST")
        self.assertEqual(source_trust_level_from_score(60).value, "MEDIUM_TRUST")
        self.assertEqual(source_trust_level_from_score(59.9).value, "LOW_TRUST")
        self.assertEqual(source_trust_level_from_score(30).value, "LOW_TRUST")
        self.assertEqual(source_trust_level_from_score(29.9).value, "UNTRUSTED")
        self.assertEqual(source_trust_level_from_score(0).value, "UNTRUSTED")
        self.assertEqual(source_trust_level_from_score(100, blocked=True).value, "BLOCKED")

    def test_trust_score_from_quality_scores_empty(self):
        self.assertEqual(trust_score_from_quality_scores([]), 50.0)
        self.assertEqual(trust_score_from_quality_scores(None), 50.0)

    def test_trust_score_from_quality_scores_list(self):
        s1 = MagicMock()
        s1.total_score = 80.0
        s2 = MagicMock()
        s2.total_score = 90.0
        self.assertEqual(trust_score_from_quality_scores([s1, s2]), 85.0)

    @patch('usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id')
    @patch('usa_signal_bot.provider_quality.source_trust_model.datetime')
    def test_build_source_trust_profile_empty(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "profile_123"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2024-01-01T00:00:00"
        )

        profile = build_source_trust_profile("TEST_PROV")

        self.assertEqual(profile.profile_id, "profile_123")
        self.assertEqual(profile.provider_name, "TEST_PROV")
        self.assertEqual(profile.provider_kind, "MARKET_DATA")
        self.assertEqual(profile.trust_score, 50.0)
        self.assertEqual(profile.trust_level.value, "LOW_TRUST")
        self.assertEqual(profile.created_at_utc, "2024-01-01T00:00:00Z")
        self.assertTrue(any(f.value == "TRUST_SCORE_LOW" for f in profile.risk_flags))

    @patch('usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id')
    @patch('usa_signal_bot.provider_quality.source_trust_model.datetime')
    def test_build_source_trust_profile_with_scores(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "profile_123"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2024-01-01T00:00:00"
        )

        # Build mock components
        c1 = MagicMock()
        c1.component = DataQualityComponent.SCHEMA_VALIDITY
        c1.score = 100.0

        c2 = MagicMock()
        c2.component = DataQualityComponent.FRESHNESS
        c2.score = 90.0

        s1 = MagicMock()
        s1.total_score = 95.0
        s1.blocked = False
        s1.components = [c1, c2]

        profile = build_source_trust_profile("TEST_PROV", quality_scores=[s1])

        self.assertEqual(profile.trust_score, 95.0)
        self.assertEqual(profile.trust_level.value, "HIGH_TRUST")
        self.assertEqual(profile.schema_reliability_score, 100.0)
        self.assertEqual(profile.freshness_reliability_score, 90.0)
        self.assertIsNone(profile.agreement_reliability_score)

    @patch('usa_signal_bot.provider_quality.source_trust_model.create_source_trust_profile_id')
    @patch('usa_signal_bot.provider_quality.source_trust_model.datetime')
    def test_build_source_trust_profile_safety_blocked(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "profile_123"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2024-01-01T00:00:00"
        )

        c1 = MagicMock()
        c1.component = DataQualityComponent.SAFETY_COMPLIANCE
        c1.score = 99.0

        s1 = MagicMock()
        s1.total_score = 100.0
        s1.blocked = False
        s1.components = [c1]

        profile = build_source_trust_profile("TEST_PROV", quality_scores=[s1])

        self.assertEqual(profile.trust_score, 100.0)
        self.assertEqual(profile.trust_level.value, "BLOCKED")
        self.assertIn("Safety reliability is below 100, blocking trust.", profile.warnings)

    def test_source_trust_profile_summary(self):
        profile = MagicMock()
        profile.profile_id = "p_1"
        profile.provider_name = "P1"
        profile.trust_score = 88.5
        profile.trust_level.value = "HIGH_TRUST"

        summary = source_trust_profile_summary(profile)
        self.assertEqual(summary, {
            "profile_id": "p_1",
            "provider": "P1",
            "trust_score": 88.5,
            "trust_level": "HIGH_TRUST"
        })

    def test_source_trust_profile_to_text(self):
        profile = MagicMock()
        profile.provider_name = "P1"
        profile.trust_score = 88.5
        profile.trust_level.value = "HIGH_TRUST"

        text = source_trust_profile_to_text(profile)
        self.assertEqual(text, "Source Trust Profile: P1 | Score: 88.5 (HIGH_TRUST)")

if __name__ == '__main__':
    unittest.main()
