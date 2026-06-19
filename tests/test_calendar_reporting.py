"""Test calendar reporting."""

from usa_signal_bot.calendar.calendar_reporting import (
    calendar_limitations_text,
    market_session_to_text,
)
from usa_signal_bot.calendar.calendar_models import MarketSession


def test_calendar_reporting():
    txt = calendar_limitations_text()
    assert (
        "NOT an official exchange calendar" in txt
        or "DOES NOT guarantee exact official exchange calendar dates" in txt
    )


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
        source=DummyEnum("CalendarDataSource"),
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
        source=DummyEnum("CalendarDataSource"),
    )

    text = market_session_to_text(session)
    assert "Session: 2023-10-28" in text
    assert "Trading: False" in text
    assert "Times:" not in text


def test_session_validation_result_to_text():
    from usa_signal_bot.calendar.calendar_models import SessionValidationResult
    from usa_signal_bot.calendar.calendar_reporting import (
        session_validation_result_to_text,
    )

    class DummyEnum:
        def __init__(self, value):
            self.value = value

    result = SessionValidationResult(
        validation_id="val123",
        created_at_utc="2023-10-27T00:00:00Z",
        symbol="AAPL",
        calendar_name=DummyEnum("NYSE"),
        status=DummyEnum("VALID"),
        row_count=100,
        trading_day_count=100,
        non_trading_day_rows=0,
        missing_trading_days=0,
        early_close_rows=0,
        warnings=[],
        errors=[],
        metadata={},
    )

    text = session_validation_result_to_text(result)
    assert "Session Validation for AAPL: VALID" in text
    assert "Total Rows: 100" in text
    assert "Expected Trading Days: 100" in text
    assert "Missing Days: 0" in text
    assert "Non-trading Rows: 0" in text
    assert "Early Close Rows: 0" in text
