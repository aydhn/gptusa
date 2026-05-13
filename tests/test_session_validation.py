"""Test session validation."""
from usa_signal_bot.calendar.session_validation import validate_rows_against_calendar
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
