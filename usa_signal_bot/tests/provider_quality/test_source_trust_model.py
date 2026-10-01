import pytest
from unittest.mock import MagicMock
from usa_signal_bot.provider_quality.phase109_models import ProviderDataQualityScore, DataQualityScoreComponent
from usa_signal_bot.provider_quality.source_trust_model import (
    source_trust_level_from_score,
    trust_score_from_quality_scores,
    build_source_trust_profile,
    source_trust_profile_summary,
    source_trust_profile_to_text,
)

def test_source_trust_level_from_score():
    assert source_trust_level_from_score(100, blocked=True).value == "BLOCKED"
    assert source_trust_level_from_score(85).value == "HIGH_TRUST"
    assert source_trust_level_from_score(60).value == "MEDIUM_TRUST"
    assert source_trust_level_from_score(30).value == "LOW_TRUST"
    assert source_trust_level_from_score(29).value == "UNTRUSTED"



def test_trust_score_from_quality_scores():
    # Empty list
    assert trust_score_from_quality_scores([]) == 50.0

    # Mock scores
    score1 = MagicMock(spec=ProviderDataQualityScore)
    score1.total_score = 80.0

    score2 = MagicMock(spec=ProviderDataQualityScore)
    score2.total_score = 60.0

    assert trust_score_from_quality_scores([score1, score2]) == 70.0

def test_build_source_trust_profile():
    # Empty scores
    profile = build_source_trust_profile("TestProvider")
    assert profile.provider_name == "TestProvider"
    assert profile.trust_score == 50.0 # From empty list
    assert profile.trust_level.value == "LOW_TRUST"

    assert len(profile.risk_flags) == 1 # TRUST_SCORE_LOW

    # With scores
    comp1 = MagicMock(spec=DataQualityScoreComponent)
    comp1.component = "SCHEMA_VALIDITY"
    comp1.score = 90.0

    comp2 = MagicMock(spec=DataQualityScoreComponent)
    comp2.component = "SAFETY_COMPLIANCE"
    comp2.score = 95.0

    score = MagicMock(spec=ProviderDataQualityScore)
    score.total_score = 92.0
    score.blocked = False
    score.components = [comp1, comp2]

    profile2 = build_source_trust_profile("TestProvider2", quality_scores=[score])

    assert profile2.trust_score == 92.0
    assert profile2.trust_level.value == "BLOCKED" # Because safety_rel is 95 (< 100)
    assert profile2.schema_reliability_score == 90.0
    assert profile2.safety_reliability_score == 95.0
    assert "Safety reliability is below 100, blocking trust." in profile2.warnings

def test_source_trust_profile_summary():
    profile = MagicMock()
    profile.profile_id = "test_id"
    profile.provider_name = "TestProvider"
    profile.trust_score = 85.5
    profile.trust_level.value = "HIGH_TRUST"

    summary = source_trust_profile_summary(profile)
    assert summary["profile_id"] == "test_id"
    assert summary["provider"] == "TestProvider"
    assert summary["trust_score"] == 85.5
    assert summary["trust_level"] == "HIGH_TRUST"

def test_source_trust_profile_to_text():
    profile = MagicMock()
    profile.provider_name = "TestProvider"
    profile.trust_score = 85.5
    profile.trust_level.value = "HIGH_TRUST"

    text = source_trust_profile_to_text(profile)
    assert text == "Source Trust Profile: TestProvider | Score: 85.5 (HIGH_TRUST)"
