import pytest
from unittest.mock import MagicMock
from usa_signal_bot.provider_quality.selection_safety_validator import (
    validate_provider_selection_safety,
    validate_provider_ranking_safety,
    validate_provider_quality_context_safety,
    collect_provider_quality_risk_flags,
    selection_safety_validator_summary,
    selection_safety_validator_to_text,
)

def test_validate_provider_selection_safety_safe():
    score = MagicMock()
    score.decision.value = "ACCEPT"
    score.explanation = "good"
    score.selectable_for_research = True
    assert validate_provider_selection_safety(score) == []

def test_validate_provider_selection_safety_unsafe_execution_language():
    score = MagicMock()
    score.decision.value = "PREFER_FOR_RESEARCH_DATA"
    score.explanation = "this is a trade signal"
    score.selectable_for_research = True
    assert validate_provider_selection_safety(score) == ["Explanation contains unsafe execution language"]

    score.explanation = "make an order now"
    assert validate_provider_selection_safety(score) == ["Explanation contains unsafe execution language"]

def test_validate_provider_selection_safety_contradicts_research():
    score = MagicMock()
    score.decision.value = "PREFER_FOR_RESEARCH_DATA"
    score.explanation = "good"
    score.selectable_for_research = False
    assert validate_provider_selection_safety(score) == ["Score decision contradicts research selection capability"]

def test_validate_provider_ranking_safety_safe():
    ranking = MagicMock()
    ranking.ranking_is_research_data_only = True
    ranking.produces_trade_signal = False
    ranking.produces_order_decision = False
    assert validate_provider_ranking_safety(ranking) == []

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
    context = MagicMock()
    context.research_data_only = True
    context.produces_trade_signal = False
    context.produces_order_decision = False
    context.network_used = False
    context.paid_api_used = False
    context.scraping_used = False
    context.html_parsing_used = False
    context.broker_used = False
    context.order_created = False
    context.paper_state_mutated = False
    context.telegram_real_sent = False
    context.dashboard_started = False
    assert validate_provider_quality_context_safety(context) == []

def test_validate_provider_quality_context_safety_unsafe():
    context = MagicMock()
    context.research_data_only = False
    context.produces_trade_signal = True
    context.produces_order_decision = True
    context.network_used = True
    context.paid_api_used = True
    context.scraping_used = True
    context.html_parsing_used = True
    context.broker_used = True
    context.order_created = True
    context.paper_state_mutated = True
    context.telegram_real_sent = True
    context.dashboard_started = True

    errors = validate_provider_quality_context_safety(context)
    assert "research_data_only is False" in errors
    assert "produces_trade_signal is True" in errors
    assert "produces_order_decision is True" in errors
    assert "network_used is True" in errors
    assert "paid_api_used is True" in errors
    assert "scraping_used is True" in errors
    assert "html_parsing_used is True" in errors
    assert "broker_used is True" in errors
    assert "order_created is True" in errors
    assert "paper_state_mutated is True" in errors
    assert "telegram_real_sent is True" in errors
    assert "dashboard_started is True" in errors

def test_collect_provider_quality_risk_flags():
    context = MagicMock()
    context.risk_flags = ["FLAG1"]

    dq = MagicMock()
    dq.risk_flags = ["FLAG2"]

    comp = MagicMock()
    comp.risk_flags = ["FLAG3"]
    dq.components = [comp]

    context.data_quality_scores = [dq]

    tp = MagicMock()
    tp.risk_flags = ["FLAG4"]
    context.trust_profiles = [tp]

    ss = MagicMock()
    ss.risk_flags = ["FLAG5"]
    context.selection_scores = [ss]

    pr = MagicMock()
    pr.risk_flags = ["FLAG6"]
    context.rankings = [pr]

    flags = collect_provider_quality_risk_flags(context)
    assert set(flags) == {"FLAG1", "FLAG2", "FLAG3", "FLAG4", "FLAG5", "FLAG6"}

def test_collect_provider_quality_risk_flags_none():
    assert collect_provider_quality_risk_flags(None) == []

def test_selection_safety_validator_summary():
    assert selection_safety_validator_summary([]) == {"safe": True, "error_count": 0, "errors": []}
    assert selection_safety_validator_summary(["err1"]) == {"safe": False, "error_count": 1, "errors": ["err1"]}

def test_selection_safety_validator_to_text():
    assert selection_safety_validator_to_text([]) == "Selection Safety Validator: PASSED"
    assert selection_safety_validator_to_text(["err1", "err2"]) == "Selection Safety Validator: FAILED\n  err1\n  err2"
