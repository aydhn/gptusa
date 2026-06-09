from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_safety_validator import (
    portfolio_risk_text_has_trade_or_execution_language,
    portfolio_risk_payload_has_forbidden_fields
)

def test_portfolio_risk_text_has_trade_or_execution_language():
    assert portfolio_risk_text_has_trade_or_execution_language("This is investment advice.") is True
    assert portfolio_risk_text_has_trade_or_execution_language("Research diagnostic result.") is False

def test_portfolio_risk_payload_has_forbidden_fields():
    assert portfolio_risk_payload_has_forbidden_fields({"broker_order": "buy"}) is True
    assert portfolio_risk_payload_has_forbidden_fields({"sandbox_optimizer_weight": 0.5}) is False
