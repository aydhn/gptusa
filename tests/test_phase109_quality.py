import pytest
from unittest.mock import MagicMock
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderCacheIngestionResult,
    ProviderQualityContext,
    ProviderSelectionScore,
    ProviderQualityValidationError,
    validate_provider_ranking,
)
from usa_signal_bot.provider_quality.completeness_scorer import score_completeness
from usa_signal_bot.provider_quality.schema_validity_scorer import score_schema_validity
from usa_signal_bot.provider_quality.outlier_penalty_scorer import score_outlier_profile
from usa_signal_bot.provider_quality.provider_safety_compliance_scorer import (
    score_provider_safety_compliance,
    SafetyComplianceFlags,
)
from usa_signal_bot.provider_quality.data_quality_scorer import (
    build_provider_data_quality_score,
    ProviderDataQualityScoreParams,
)
from usa_signal_bot.provider_quality.provider_ranking_engine import (
    rank_providers_for_symbol,
)
from usa_signal_bot.provider_quality.score_explanation import (
    score_explanation_safety_check,
)
from usa_signal_bot.provider_quality.provider_quality_validation import (
    validate_no_unsafe_provider_quality_fields,
)


def test_completeness_scorer():
    records = [{"open": 1, "high": 2, "low": 1, "close": 2, "volume": 100}]
    comp = score_completeness(records)
    assert comp.score == 100.0
    assert comp.grade.value == "EXCELLENT"


def test_schema_validity_scorer():
    comp = score_schema_validity(["Missing column"])
    assert comp.score < 100
    assert "SCHEMA_INVALID" in [rf.value for rf in comp.risk_flags]


def test_outlier_penalty():
    records = [{"open": 100, "high": 90, "low": 105, "close": -5, "volume": 100}]
    comp = score_outlier_profile(records)
    assert comp.score < 100
    assert "OUTLIER_RISK" in [rf.value for rf in comp.risk_flags]


def test_safety_compliance():
    flags = SafetyComplianceFlags(broker_used=True)
    comp = score_provider_safety_compliance("DUMMY", flags=flags)
    assert comp.score == 0.0
    assert "BROKER_RISK" in [rf.value for rf in comp.risk_flags]


def test_data_quality_score():
    records = [{"open": 1, "high": 2, "low": 1, "close": 2, "volume": 100}]
    params = ProviderDataQualityScoreParams(provider_name="DUMMY", symbol="AAPL", capability="OHLCV", records=records)
    score = build_provider_data_quality_score(params)
    assert score.total_score > 0
    assert not score.blocked


def test_ranking_engine():
    from usa_signal_bot.provider_quality.provider_selection_scorer import (
        build_provider_selection_score,
        ProviderSelectionParams,
    )

    params = ProviderSelectionParams(
        provider_name="P1",
        symbol="AAPL",
        capability="OHLCV",
        quality_score=None,
        trust_profile=None,
    )
    s1 = build_provider_selection_score(params)
    rank = rank_providers_for_symbol("AAPL", "OHLCV", [s1])
    assert rank.preferred_provider == "P1"
    assert rank.produces_trade_signal is False


def test_explanation_safety():
    assert len(score_explanation_safety_check("This guarantees a buy signal!")) > 0
    assert len(score_explanation_safety_check("Data quality is good for research")) == 0


def test_validation():
    rep = validate_no_unsafe_provider_quality_fields({"network_used": True})
    assert not rep.valid
    assert rep.issue_count == 1

    rep2 = validate_no_unsafe_provider_quality_fields(
        {"network_used": False, "paper_state_mutated": False}
    )
    assert rep2.valid


def test_validate_provider_ranking():
    # Happy path
    mock_item = MagicMock()
    mock_item.ranking_is_research_data_only = True
    mock_item.produces_trade_signal = False
    mock_item.produces_order_decision = False
    validate_provider_ranking(mock_item)  # Should not raise

    # Error: ranking_is_research_data_only is False
    mock_item.ranking_is_research_data_only = False
    with pytest.raises(ProviderQualityValidationError) as exc:
        validate_provider_ranking(mock_item)
    assert "ranking_is_research_data_only must be True" in str(exc.value)
    mock_item.ranking_is_research_data_only = True  # reset

    # Error: produces_trade_signal is True
    mock_item.produces_trade_signal = True
    with pytest.raises(ProviderQualityValidationError) as exc:
        validate_provider_ranking(mock_item)
    assert "produces_trade_signal must be False" in str(exc.value)
    mock_item.produces_trade_signal = False  # reset

    # Error: produces_order_decision is True
    mock_item.produces_order_decision = True
    with pytest.raises(ProviderQualityValidationError) as exc:
        validate_provider_ranking(mock_item)
    assert "produces_order_decision must be False" in str(exc.value)
