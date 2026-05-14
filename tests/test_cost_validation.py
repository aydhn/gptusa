import pytest
from usa_signal_bot.transaction_costs.cost_validation import validate_no_live_execution_language_in_cost, validate_no_sensitive_data_in_cost_payload

def test_no_live_execution_language():
    rep = validate_no_live_execution_language_in_cost("This is guaranteed fill")
    assert rep.valid is False
    assert rep.blocked_count > 0

def test_no_sensitive_data():
    rep = validate_no_sensitive_data_in_cost_payload({"api_key": "12345"})
    assert rep.valid is False
    assert rep.blocked_count > 0
