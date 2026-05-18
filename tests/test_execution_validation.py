import pytest
from usa_signal_bot.research_execution.execution_validation import (
    validate_no_live_execution_language_in_execution,
    validate_no_auto_apply_or_optimizer_language,
    validate_no_broker_execution_fields_in_execution
)

def test_validate_no_live_execution_language():
    res = validate_no_live_execution_language_in_execution("This strategy is live approved and sent to broker.")
    assert not res.valid
    assert any("live approved" in e for e in res.errors)

def test_validate_no_auto_apply_language():
    res = validate_no_auto_apply_or_optimizer_language("We will otomatik optimize et the parameters.")
    assert not res.valid
    assert any("otomatik optimize et" in e for e in res.errors)

def test_validate_no_broker_execution_fields():
    payload = {"metrics": {"drawdown": 10}, "broker_order_id": "12345"}
    res = validate_no_broker_execution_fields_in_execution(payload)
    assert not res.valid
    assert any("broker_order_id" in e for e in res.errors)
