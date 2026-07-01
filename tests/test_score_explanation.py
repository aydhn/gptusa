import pytest
import sys
from unittest.mock import MagicMock

# Mock out core.enums to avoid ImportError during test collection
class DummyEnum:
    def __init__(self, value):
        self.value = value

mock_enums = MagicMock()
mock_enums.ProviderQualityRiskFlag = DummyEnum
sys.modules['usa_signal_bot.core.enums'] = mock_enums

from usa_signal_bot.provider_quality.score_explanation import explain_quality_score
from usa_signal_bot.provider_quality.phase109_models import ProviderDataQualityScore, DataQualityScoreComponent

def test_explain_quality_score_blocked():
    comp = MagicMock()
    comp.score = 40.0
    comp.component.value = "FRESHNESS"
    comp.explanation = "Data is stale."

    score = ProviderDataQualityScore(
        score_id="id123",
        created_at_utc="2023-01-01",
        provider_name="TestProvider",
        symbol="BTCUSD",
        capability="PRICE",
        components=[comp],
        total_score=45.0,
        grade=DummyEnum("BLOCKED"),
        usable_for_research=False,
        use_with_warning=False,
        blocked=True,
        explanation=""
    )
    result = explain_quality_score(score)
    assert "Data Quality Score for TestProvider (BTCUSD) is 45.0 (BLOCKED)." in result
    assert "The provider is BLOCKED for data quality issues." in result
    assert "Weakness: FRESHNESS scored 40.0. Data is stale." in result

def test_explain_quality_score_usable_research():
    score = ProviderDataQualityScore(
        score_id="id123",
        created_at_utc="2023-01-01",
        provider_name="TestProvider",
        symbol="BTCUSD",
        capability="PRICE",
        components=[],
        total_score=75.0,
        grade=DummyEnum("ACCEPTABLE"),
        usable_for_research=True,
        use_with_warning=False,
        blocked=False,
        explanation=""
    )
    result = explain_quality_score(score)
    assert "The provider data is deemed USABLE FOR RESEARCH." in result

def test_explain_quality_score_not_usable():
    score = ProviderDataQualityScore(
        score_id="id123",
        created_at_utc="2023-01-01",
        provider_name="TestProvider",
        symbol="BTCUSD",
        capability="PRICE",
        components=[],
        total_score=55.0,
        grade=DummyEnum("WEAK"),
        usable_for_research=False,
        use_with_warning=False,
        blocked=False,
        explanation=""
    )
    result = explain_quality_score(score)
    assert "The provider data is NOT USABLE FOR RESEARCH without major caveats." in result

def test_explain_quality_score_unsafe_language():
    comp = MagicMock()
    comp.score = 40.0
    comp.component.value = "FRESHNESS"
    comp.explanation = "Contains trade signal"

    score = ProviderDataQualityScore(
        score_id="id123",
        created_at_utc="2023-01-01",
        provider_name="TestProvider",
        symbol="BTCUSD",
        capability="PRICE",
        components=[comp],
        total_score=45.0,
        grade=DummyEnum("BLOCKED"),
        usable_for_research=False,
        use_with_warning=False,
        blocked=True,
        explanation=""
    )
    result = explain_quality_score(score)
    assert result == "Explanation blocked due to unsafe language."
