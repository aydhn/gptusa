
from usa_signal_bot.diagnostics.diagnostics_validation import validate_no_live_execution_language_in_diagnostics, validate_no_sensitive_data_in_diagnostics_payload

def test_validate_no_live_execution_language():
    report = validate_no_live_execution_language_in_diagnostics("This is safe.")
    assert report.valid

    report = validate_no_live_execution_language_in_diagnostics("This is live approved to run")
    assert not report.valid
    assert "live approved" in report.issues[0].message

def test_validate_no_sensitive_data():
    report = validate_no_sensitive_data_in_diagnostics_payload({"metadata": {"api_key": "12345"}})
    assert not report.valid
