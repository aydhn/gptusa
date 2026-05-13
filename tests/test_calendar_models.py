"""Test calendar models."""
import pytest
from usa_signal_bot.calendar.calendar_models import (
    MarketHoliday, MarketEarlyClose, MarketSession,
    validate_market_holiday, validate_market_early_close, validate_market_session,
    create_market_session_id
)
from usa_signal_bot.core.enums import MarketCalendarName, CalendarDataSource, MarketSessionType
from usa_signal_bot.core.exceptions import MarketCalendarError

def test_market_holiday_valid():
    h = MarketHoliday("2024-01-01", "New Year", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT)
    validate_market_holiday(h)

def test_market_holiday_invalid():
    h = MarketHoliday("2024-13-45", "Invalid", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT)
    with pytest.raises(MarketCalendarError):
        validate_market_holiday(h)

def test_market_early_close_valid():
    c = MarketEarlyClose("2024-07-03", "13:00", "Early Close", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT)
    validate_market_early_close(c)

def test_market_session_valid():
    s = MarketSession("id", MarketCalendarName.US_EQUITIES, "2024-01-02", MarketSessionType.REGULAR, "09:30", "16:00", "America/New_York", True, False, CalendarDataSource.STATIC_DEFAULT)
    validate_market_session(s)

def test_market_session_invalid_time():
    s = MarketSession("id", MarketCalendarName.US_EQUITIES, "2024-01-02", MarketSessionType.REGULAR, "16:00", "09:30", "America/New_York", True, False, CalendarDataSource.STATIC_DEFAULT)
    with pytest.raises(MarketCalendarError):
        validate_market_session(s)

def test_market_session_id_factory():
    sid = create_market_session_id(MarketCalendarName.US_EQUITIES, "2024-01-02")
    assert "US_EQUITIES" in sid
    assert "2024-01-02" in sid
