"""Test session validation."""
from usa_signal_bot.calendar.session_validation import validate_rows_against_calendar, validate_non_trading_rows, validate_missing_sessions
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar
from usa_signal_bot.core.enums import SessionValidationStatus

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

def test_validate_missing_sessions():
    cal = LocalMarketCalendar()

    # 1. Happy path: no missing sessions
    rows_valid = [
        {"date": "2024-01-02"}, # Tuesday
        {"date": "2024-01-03"}, # Wednesday
        {"date": "2024-01-04"}  # Thursday
    ]
    missing_valid, warnings_valid = validate_missing_sessions("SPY", rows_valid, cal)
    assert len(missing_valid) == 0
    assert len(warnings_valid) == 0

    # 2. Warning path: missing session (2024-01-03 is missing)
    rows_invalid = [
        {"date": "2024-01-02"}, # Tuesday
        {"date": "2024-01-04"}  # Thursday
    ]
    missing_invalid, warnings_invalid = validate_missing_sessions("SPY", rows_invalid, cal)
    assert len(missing_invalid) == 1
    assert "2024-01-03" in missing_invalid
    assert len(warnings_invalid) == 1
    assert "Symbol SPY is missing 1 trading sessions." in warnings_invalid[0]

    # 3. Edge case: empty rows
    missing_empty, warnings_empty = validate_missing_sessions("SPY", [], cal)
    assert len(missing_empty) == 0
    assert len(warnings_empty) == 0
