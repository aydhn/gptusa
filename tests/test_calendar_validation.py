"""Test calendar validation."""
from usa_signal_bot.calendar.calendar_validation import validate_no_sensitive_data_in_calendar_payload, validate_no_live_execution_language_in_calendar, CalendarValidationReport, calendar_validation_report_to_text

def test_calendar_validation_no_secrets():
    rep = validate_no_sensitive_data_in_calendar_payload({"data": "some_token_here"})
    assert rep.valid is False
    assert len(rep.errors) > 0

def test_calendar_validation_no_live_lang():
    rep = validate_no_live_execution_language_in_calendar("This is a live approved signal")
    assert rep.valid is False
    assert len(rep.errors) > 0


def test_calendar_validation_report_to_text_valid():
    report = CalendarValidationReport(
        valid=True,
        issue_count=0,
        warning_count=0,
        error_count=0,
        blocked_count=0,
        issues=[]
    )
    text = calendar_validation_report_to_text(report)
    assert text == "Calendar Validation Report: VALID\n  Issues: 0 (Errors: 0, Warnings: 0)"

def test_calendar_validation_report_to_text_invalid_with_errors():
    report = CalendarValidationReport(
        valid=False,
        issue_count=1,
        warning_count=0,
        error_count=1,
        blocked_count=0,
        issues=[],
        errors=["A serious error"]
    )
    text = calendar_validation_report_to_text(report)
    expected = "Calendar Validation Report: INVALID\n  Issues: 1 (Errors: 1, Warnings: 0)\n  Errors:\n    - A serious error"
    assert text == expected

def test_calendar_validation_report_to_text_with_warnings():
    report = CalendarValidationReport(
        valid=True,
        issue_count=1,
        warning_count=1,
        error_count=0,
        blocked_count=0,
        issues=[],
        warnings=["A slight warning"]
    )
    text = calendar_validation_report_to_text(report)
    expected = "Calendar Validation Report: VALID\n  Issues: 1 (Errors: 0, Warnings: 1)\n  Warnings:\n    - A slight warning"
    assert text == expected

def test_calendar_validation_report_to_text_errors_and_warnings():
    report = CalendarValidationReport(
        valid=False,
        issue_count=2,
        warning_count=1,
        error_count=1,
        blocked_count=0,
        issues=[],
        errors=["Fatal error"],
        warnings=["Just a warning"]
    )
    text = calendar_validation_report_to_text(report)
    expected = "Calendar Validation Report: INVALID\n  Issues: 2 (Errors: 1, Warnings: 1)\n  Errors:\n    - Fatal error\n  Warnings:\n    - Just a warning"
    assert text == expected
