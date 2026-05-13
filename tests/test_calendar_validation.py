"""Test calendar validation."""
from usa_signal_bot.calendar.calendar_validation import validate_no_sensitive_data_in_calendar_payload, validate_no_live_execution_language_in_calendar

def test_calendar_validation_no_secrets():
    rep = validate_no_sensitive_data_in_calendar_payload({"data": "some_token_here"})
    assert rep.valid is False
    assert len(rep.errors) > 0

def test_calendar_validation_no_live_lang():
    rep = validate_no_live_execution_language_in_calendar("This is a live approved signal")
    assert rep.valid is False
    assert len(rep.errors) > 0
