"""Test session classifier."""
from usa_signal_bot.calendar.session_classifier import classify_timestamp_session, classify_rows_by_session, session_type_to_signal_guard
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar
from usa_signal_bot.core.enums import MarketSessionType

def test_session_classifier():
    cal = LocalMarketCalendar()

    assert classify_timestamp_session("2024-01-02", cal) == MarketSessionType.REGULAR
    assert classify_timestamp_session("2024-01-02 08:00", cal) == MarketSessionType.PREMARKET
    assert classify_timestamp_session("2024-01-02 16:30", cal) == MarketSessionType.AFTER_HOURS
    assert classify_timestamp_session("2024-01-06", cal) == MarketSessionType.WEEKEND

    rows = [{"date": "2024-01-02"}, {"date": "2024-01-06"}]
    summary = classify_rows_by_session(rows, cal)
    assert summary[MarketSessionType.REGULAR.value] == 1
    assert summary[MarketSessionType.WEEKEND.value] == 1

    guard = session_type_to_signal_guard(MarketSessionType.CLOSED)
    assert guard["is_trading_allowed"] is False
    assert guard["warning"] is not None
