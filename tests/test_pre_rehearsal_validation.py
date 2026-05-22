import pytest
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_validation import validate_no_sensitive_data_in_pre_paper_payload

def test_sensitive_validation():
    payload = {"api_key": "123"}
    report = validate_no_sensitive_data_in_pre_paper_payload(payload)
    assert not report.valid

    payload_safe = {"api_key": "[REDACTED]"}
    report2 = validate_no_sensitive_data_in_pre_paper_payload(payload_safe)
    assert report2.valid
