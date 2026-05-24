import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_validation import validate_no_live_execution_language_in_handoff_freeze, validate_no_sensitive_data_in_handoff_freeze_payload

def test_validate_no_live_execution_language():
    text = "The system is live approved and sent to broker"
    report = validate_no_live_execution_language_in_handoff_freeze(text)
    assert report.valid is False
    assert report.error_count == 2

def test_validate_no_sensitive_data():
    payload = {"api_key": "12345"}
    report = validate_no_sensitive_data_in_handoff_freeze_payload(payload)
    assert report.valid is False
    assert report.error_count == 1
