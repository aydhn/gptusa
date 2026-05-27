import pytest
from usa_signal_bot.feature_engine.factor_explainability.report_qa_validator import qa_rule_no_investment_advice, qa_rule_no_trade_signal_language

def test_qa_rule_no_investment_advice():
    res = qa_rule_no_investment_advice("Bu faktör kesin al diyor")
    assert res.passed is False
    assert res.language_risk is not None
    assert "kesin al" in res.matched_terms

def test_qa_rule_no_trade_signal_language():
    res = qa_rule_no_trade_signal_language("We see a strong buy")
    assert res.passed is False
    assert "strong buy" in res.matched_terms
