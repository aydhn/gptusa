"""Test calendar validation."""

from usa_signal_bot.calendar.calendar_validation import (
    validate_no_sensitive_data_in_calendar_payload,
    validate_no_live_execution_language_in_calendar,
)
from usa_signal_bot.calendar.calendar_validation import (
    validate_session_validation_report_report,
)
from usa_signal_bot.calendar.calendar_models import SessionValidationResult
from usa_signal_bot.core.enums import SessionValidationStatus, MarketCalendarName


def test_calendar_validation_no_secrets():
    rep = validate_no_sensitive_data_in_calendar_payload({"data": "some_token_here"})
    assert rep.valid is False
    assert len(rep.errors) > 0


def test_calendar_validation_no_live_lang():
    rep = validate_no_live_execution_language_in_calendar(
        "This is a live approved signal"
    )
    assert rep.valid is False
    assert len(rep.errors) > 0


def test_validate_session_validation_report_report_invalid():
    result = SessionValidationResult(
        validation_id="val_1",
        created_at_utc="2024-01-01T00:00:00Z",
        symbol="AAPL",
        calendar_name=MarketCalendarName.NYSE,
        status=SessionValidationStatus.INVALID,
        row_count=100,
        trading_day_count=100,
        non_trading_day_rows=0,
        missing_trading_days=0,
        early_close_rows=0,
        warnings=["A normal warning"],
        errors=["A normal error"],
        metadata={},
    )
    report = validate_session_validation_report_report(result)
    assert report.valid is False
    assert report.error_count == 2  # 1 from INVALID status + 1 from explicit error
    assert report.warning_count == 1  # 1 from explicit warning


def test_validate_session_validation_report_report_warning():
    result = SessionValidationResult(
        validation_id="val_2",
        created_at_utc="2024-01-01T00:00:00Z",
        symbol="AAPL",
        calendar_name=MarketCalendarName.NYSE,
        status=SessionValidationStatus.WARNING,
        row_count=100,
        trading_day_count=100,
        non_trading_day_rows=0,
        missing_trading_days=0,
        early_close_rows=0,
        warnings=["Another normal warning"],
        errors=[],
        metadata={},
    )
    report = validate_session_validation_report_report(result)
    assert report.valid is True
    assert report.error_count == 0
    assert report.warning_count == 2  # 1 from WARNING status + 1 from explicit warning


def test_validate_session_validation_report_report_valid():
    result = SessionValidationResult(
        validation_id="val_3",
        created_at_utc="2024-01-01T00:00:00Z",
        symbol="AAPL",
        calendar_name=MarketCalendarName.NYSE,
        status=SessionValidationStatus.VALID,
        row_count=100,
        trading_day_count=100,
        non_trading_day_rows=0,
        missing_trading_days=0,
        early_close_rows=0,
        warnings=[],
        errors=[],
        metadata={},
    )
    report = validate_session_validation_report_report(result)
    assert report.valid is True
    assert report.error_count == 0
    assert report.warning_count == 0
