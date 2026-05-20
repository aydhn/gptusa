import pytest
from usa_signal_bot.paper_quarantine.quarantine_validation import (
    validate_no_sensitive_data_in_quarantine_payload,
    validate_no_broker_execution_fields_in_quarantine,
    validate_no_paper_state_mutation_fields_in_quarantine,
    validate_no_live_execution_language_in_quarantine,
)

def test_validation():
    r = validate_no_sensitive_data_in_quarantine_payload({"api_key": "secret"})
    assert r.valid is False

    r = validate_no_broker_execution_fields_in_quarantine({"broker_order_id": "1"})
    assert r.valid is False

    r = validate_no_paper_state_mutation_fields_in_quarantine({"paper_state_committed": True})
    assert r.valid is False

    r = validate_no_live_execution_language_in_quarantine("sent to broker")
    assert r.valid is False
