"""Test session validation."""
from usa_signal_bot.calendar.session_validation import validate_rows_against_calendar, validate_non_trading_rows
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar
from usa_signal_bot.core.enums import SessionValidationStatus
from usa_signal_bot.calendar.session_validation import session_validation_summary_to_text
from usa_signal_bot.calendar.calendar_models import SessionValidationResult
from usa_signal_bot.core.enums import MarketCalendarName

def test_session_validation():
    cal = LocalMarketCalendar()
    rows = [
        {"date": "2024-01-02"},
        {"date": "2024-01-04"},
        {"date": "2024-01-06"}
    ]
    res = validate_rows_against_calendar("SPY", rows, cal)
    assert res.status == SessionValidationStatus.INVALID # Because of Saturday
    assert res.non_trading_day_rows == 1
    assert res.missing_trading_days == 2

def test_validate_non_trading_rows():
    cal = LocalMarketCalendar()

    # 1. Happy path: only trading days
    rows_valid = [
        {"date": "2024-01-02"}, # Tuesday
        {"date": "2024-01-04"}  # Thursday
    ]
    non_trading_valid, errors_valid = validate_non_trading_rows("SPY", rows_valid, cal)
    assert len(non_trading_valid) == 0
    assert len(errors_valid) == 0

    # 2. Error path: mixed trading and non-trading days
    rows_invalid = [
        {"date": "2024-01-02"}, # Tuesday
        {"date": "2024-01-06"}, # Saturday
        {"date": "2024-01-07"}  # Sunday
    ]
    non_trading_invalid, errors_invalid = validate_non_trading_rows("SPY", rows_invalid, cal)
    assert len(non_trading_invalid) == 2
    assert len(errors_invalid) == 1
    assert "Symbol SPY has 2 rows on non-trading days" in errors_invalid[0]

    # 3. Edge case: empty rows
    non_trading_empty, errors_empty = validate_non_trading_rows("SPY", [], cal)
    assert len(non_trading_empty) == 0
    assert len(errors_empty) == 0


def test_session_validation_summary_to_text_clean():
    # Happy path: no warnings, no errors
    res = SessionValidationResult(
        validation_id="val_123",
        created_at_utc="2024-01-01T00:00:00Z",
        symbol="SPY",
        calendar_name=MarketCalendarName.US_EQUITIES if hasattr(MarketCalendarName, "US_EQUITIES") else "US_EQUITIES",
        status=SessionValidationStatus.VALID,
        row_count=100,
        trading_day_count=100,
        non_trading_day_rows=0,
        missing_trading_days=0,
        early_close_rows=0
    )

    output = session_validation_summary_to_text(res)

    assert "Session Validation for SPY: VALID" in output
    assert "Total Rows: 100" in output
    assert "Expected Trading Days: 100" in output
    assert "Missing Days: 0" in output
    assert "Non-trading Rows: 0" in output
    assert "Early Close Rows: 0" in output
    assert "Warnings:" not in output
    assert "Errors:" not in output

def test_session_validation_summary_to_text_with_issues():
    # Path with warnings and errors
    res = SessionValidationResult(
        validation_id="val_456",
        created_at_utc="2024-01-01T00:00:00Z",
        symbol="AAPL",
        calendar_name=MarketCalendarName.US_EQUITIES if hasattr(MarketCalendarName, "US_EQUITIES") else "US_EQUITIES",
        status=SessionValidationStatus.INVALID,
        row_count=90,
        trading_day_count=100,
        non_trading_day_rows=2,
        missing_trading_days=10,
        early_close_rows=1,
        warnings=["Missing 10 trading days.", "Found 1 early close days."],
        errors=["Found 2 rows on non-trading days.", "Too many missing trading days."]
    )

    output = session_validation_summary_to_text(res)

    assert "Session Validation for AAPL: INVALID" in output
    assert "Total Rows: 90" in output
    assert "Expected Trading Days: 100" in output
    assert "Missing Days: 10" in output
    assert "Non-trading Rows: 2" in output
    assert "Early Close Rows: 1" in output

    assert "  Warnings:" in output
    assert "    - Missing 10 trading days." in output
    assert "    - Found 1 early close days." in output

    assert "  Errors:" in output
    assert "    - Found 2 rows on non-trading days." in output
    assert "    - Too many missing trading days." in output
