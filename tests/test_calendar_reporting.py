"""Test calendar reporting."""
from usa_signal_bot.calendar.calendar_reporting import calendar_limitations_text, market_session_to_text
from usa_signal_bot.calendar.calendar_models import MarketSession

def test_calendar_reporting():
    txt = calendar_limitations_text()
    assert "NOT an official exchange calendar" in txt or "DOES NOT guarantee exact official exchange calendar dates" in txt

def test_market_session_to_text():
    class DummyEnum:
        def __init__(self, value):
            self.value = value

    session = MarketSession(
        session_id="id1",
        calendar_name=DummyEnum("MarketCalendarName"),
        date="2023-10-27",
        session_type=DummyEnum("MarketSessionType"),
        open_time_local="09:30",
        close_time_local="16:00",
        timezone="America/New_York",
        is_trading_session=True,
        is_early_close=False,
        source=DummyEnum("CalendarDataSource")
    )

    text = market_session_to_text(session)
    assert "Session: 2023-10-27" in text
    assert "Type: MarketSessionType" in text
    assert "Trading: True" in text
    assert "Early Close: False" in text
    assert "Times: 09:30 - 16:00 America/New_York" in text

def test_market_session_to_text_no_times():
    class DummyEnum:
        def __init__(self, value):
            self.value = value

    session = MarketSession(
        session_id="id2",
        calendar_name=DummyEnum("MarketCalendarName"),
        date="2023-10-28",
        session_type=DummyEnum("MarketSessionType"),
        open_time_local=None,
        close_time_local=None,
        timezone="America/New_York",
        is_trading_session=False,
        is_early_close=False,
        source=DummyEnum("CalendarDataSource")
    )

    text = market_session_to_text(session)
    assert "Session: 2023-10-28" in text
    assert "Trading: False" in text
    assert "Times:" not in text
