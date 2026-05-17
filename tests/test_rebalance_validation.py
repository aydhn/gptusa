import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_validation import (
    validate_current_portfolio_state_report, validate_rebalance_plan_report,
    validate_no_sensitive_data_in_rebalance_payload, validate_no_live_execution_language_in_rebalance,
    validate_no_broker_execution_fields_in_rebalance
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, PortfolioPosition, RebalancePlan
)

def test_validate_current_portfolio_state_report():
    curr = CurrentPortfolioState("1", "now", 1000, 1000, [
        PortfolioPosition("p1", "AAPL", -10, 1000) # Negative quantity
    ])
    report = validate_current_portfolio_state_report(curr)
    assert report.valid is False
    assert len(report.errors) == 1
    assert "negative quantity" in report.errors[0]

def test_validate_no_sensitive_data():
    payload = {"api_key": "12345"}
    report = validate_no_sensitive_data_in_rebalance_payload(payload)
    assert report.valid is False
    assert "api_key" in report.errors[0]

def test_validate_no_live_execution_language():
    text = "This is live approved and sent to broker."
    report = validate_no_live_execution_language_in_rebalance(text)
    assert report.valid is False
    assert len(report.errors) >= 2 # Should catch both phrases

def test_validate_no_broker_execution_fields():
    payload = {"sent_to_broker": True}
    report = validate_no_broker_execution_fields_in_rebalance(payload)
    assert report.valid is False
    assert "sent_to_broker" in report.errors[0]
