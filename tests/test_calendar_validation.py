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


def test_assert_calendar_valid_passes():
    """Test that assert_calendar_valid does not raise an exception when the report is valid."""
    from usa_signal_bot.calendar.calendar_validation import assert_calendar_valid, CalendarValidationReport

    report = CalendarValidationReport(
        valid=True,
        issue_count=0,
        warning_count=0,
        error_count=0,
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=[]
    )

    # Should not raise any exception
    assert_calendar_valid(report)

def test_assert_calendar_valid_raises():
    """Test that assert_calendar_valid raises a CalendarValidationError when the report is invalid."""
    import pytest
    from usa_signal_bot.calendar.calendar_validation import assert_calendar_valid, CalendarValidationReport
    from usa_signal_bot.core.exceptions import CalendarValidationError

    report = CalendarValidationReport(
        valid=False,
        issue_count=2,
        warning_count=0,
        error_count=2,
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=["First error", "Second error"]
    )

    with pytest.raises(CalendarValidationError) as exc_info:
        assert_calendar_valid(report)

    error_msg = str(exc_info.value)
    assert "Calendar validation failed:" in error_msg
    assert "First error" in error_msg
    assert "Second error" in error_msg
