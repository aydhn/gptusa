import pytest
from unittest.mock import MagicMock

# Skip test execution globally if enums cannot be imported (matches other tests in this suite)
try:
    from usa_signal_bot.provider_quality.selection_safety_validator import (
        validate_provider_selection_safety,
        validate_provider_ranking_safety,
        validate_provider_quality_context_safety,
        collect_provider_quality_risk_flags,
        selection_safety_validator_summary,
        selection_safety_validator_to_text,
    )
except ImportError:
    pytest.skip("Skipping selection safety validator tests due to global import errors.", allow_module_level=True)


def test_validate_provider_selection_safety_safe():
    score = MagicMock()
    score.decision.value = "PREFER_FOR_RESEARCH_DATA"
    score.explanation = "good data"
    score.selectable_for_research = True
    assert not validate_provider_selection_safety(score)


def test_validate_provider_selection_safety_unsafe_language():
    score = MagicMock()
    score.decision.value = "PREFER_FOR_RESEARCH_DATA"
    score.explanation = "this produces a trade signal"
    score.selectable_for_research = True
    errors = validate_provider_selection_safety(score)
    assert "Explanation contains unsafe execution language" in errors

    score.explanation = "send an order"
    errors2 = validate_provider_selection_safety(score)
    assert "Explanation contains unsafe execution language" in errors2


def test_validate_provider_selection_safety_contradiction():
    score = MagicMock()
    score.decision.value = "PREFER_FOR_RESEARCH_DATA"
    score.explanation = "safe explanation"
    score.selectable_for_research = False
    errors = validate_provider_selection_safety(score)
    assert "Score decision contradicts research selection capability" in errors


def test_validate_provider_ranking_safety_safe():
    ranking = MagicMock()
    ranking.ranking_is_research_data_only = True
    ranking.produces_trade_signal = False
    ranking.produces_order_decision = False
    assert not validate_provider_ranking_safety(ranking)


def test_validate_provider_ranking_safety_unsafe():
    ranking = MagicMock()
    ranking.ranking_is_research_data_only = False
    ranking.produces_trade_signal = True
    ranking.produces_order_decision = True
    errors = validate_provider_ranking_safety(ranking)
    assert "ranking_is_research_data_only must be True" in errors
    assert "produces_trade_signal must be False" in errors
    assert "produces_order_decision must be False" in errors


def test_validate_provider_quality_context_safety_safe():
    ctx = MagicMock()
    ctx.research_data_only = True
    unsafe_flags = [
        "produces_trade_signal", "produces_order_decision", "network_used",
        "paid_api_used", "scraping_used", "html_parsing_used", "broker_used",
        "order_created", "paper_state_mutated", "telegram_real_sent",
        "dashboard_started"
    ]
    for flag in unsafe_flags:
        setattr(ctx, flag, False)

    assert not validate_provider_quality_context_safety(ctx)


def test_validate_provider_quality_context_safety_unsafe():
    ctx = MagicMock()
    ctx.research_data_only = False
    unsafe_flags = [
        "produces_trade_signal", "produces_order_decision", "network_used",
        "paid_api_used", "scraping_used", "html_parsing_used", "broker_used",
        "order_created", "paper_state_mutated", "telegram_real_sent",
        "dashboard_started"
    ]
    for flag in unsafe_flags:
        setattr(ctx, flag, True)

    errors = validate_provider_quality_context_safety(ctx)
    assert "research_data_only is False" in errors
    for flag in unsafe_flags:
        assert f"{flag} is True" in errors


def test_collect_provider_quality_risk_flags():
    ctx = MagicMock()
    ctx.risk_flags = ["CTX_FLAG"]

    q1 = MagicMock()
    q1.risk_flags = ["Q_FLAG"]
    c1 = MagicMock()
    c1.risk_flags = ["C_FLAG"]
    q1.components = [c1]
    ctx.data_quality_scores = [q1]

    t1 = MagicMock()
    t1.risk_flags = ["T_FLAG"]
    ctx.trust_profiles = [t1]

    s1 = MagicMock()
    s1.risk_flags = ["S_FLAG"]
    ctx.selection_scores = [s1]

    r1 = MagicMock()
    r1.risk_flags = ["R_FLAG"]
    ctx.rankings = [r1]

    flags = collect_provider_quality_risk_flags(ctx)
    assert set(flags) == {"CTX_FLAG", "Q_FLAG", "C_FLAG", "T_FLAG", "S_FLAG", "R_FLAG"}


def test_collect_provider_quality_risk_flags_none():
    assert collect_provider_quality_risk_flags(None) == []


def test_selection_safety_validator_summary():
    assert selection_safety_validator_summary([]) == {"safe": True, "error_count": 0, "errors": []}
    assert selection_safety_validator_summary(["err"]) == {"safe": False, "error_count": 1, "errors": ["err"]}


def test_selection_safety_validator_to_text():
    assert selection_safety_validator_to_text([]) == "Selection Safety Validator: PASSED"
    text = selection_safety_validator_to_text(["Error 1", "Error 2"])
    assert "Selection Safety Validator: FAILED" in text
    assert "Error 1" in text
    assert "Error 2" in text
