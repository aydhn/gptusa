"""Test session classifier."""

from usa_signal_bot.calendar.session_classifier import (
    classify_timestamp_session,
    classify_rows_by_session,
    session_type_to_signal_guard,
)
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar
from usa_signal_bot.core.enums import MarketSessionType, MarketCalendarName


def test_session_classifier():
    cal = LocalMarketCalendar()

    assert classify_timestamp_session("2024-01-02", cal) == MarketSessionType.REGULAR
    assert (
        classify_timestamp_session("2024-01-02 08:00", cal)
        == MarketSessionType.PREMARKET
    )
    assert (
        classify_timestamp_session("2024-01-02 16:30", cal)
        == MarketSessionType.AFTER_HOURS
    )
    assert classify_timestamp_session("2024-01-06", cal) == MarketSessionType.WEEKEND

    rows = [{"date": "2024-01-02"}, {"date": "2024-01-06"}]
    summary = classify_rows_by_session(rows, cal)
    assert summary[MarketSessionType.REGULAR.value] == 1
    assert summary[MarketSessionType.WEEKEND.value] == 1

    guard = session_type_to_signal_guard(MarketSessionType.CLOSED)
    assert guard["is_trading_allowed"] is False
    assert guard["warning"] is not None


def test_classify_rows_by_session():
    from usa_signal_bot.calendar.calendar_models import MarketEarlyClose

    # Set up a calendar with an early close date
    early_close_date = MarketEarlyClose(
        name="Black Friday",
        calendar_name=MarketCalendarName.US_EQUITIES,
        date="2024-11-29",
        close_time_local="13:00",
        source="test",
    )
    cal = LocalMarketCalendar(early_closes=[early_close_date])

    # Rows covering different session types
    rows = [
        {"timestamp": "2024-01-02 08:30"},  # PREMARKET
        {"timestamp": "2024-01-02 12:00"},  # REGULAR
        {"timestamp": "2024-01-02 16:30"},  # AFTER_HOURS
        {"timestamp": "2024-01-06 12:00"},  # WEEKEND
        {
            "timestamp": "2024-11-29 12:00"
        },  # EARLY_CLOSE (regular time, but early close date)
        {"date": ""},  # UNKNOWN
    ]

    summary = classify_rows_by_session(rows, cal)

    assert summary[MarketSessionType.PREMARKET.value] == 1
    assert summary[MarketSessionType.AFTER_HOURS.value] == 1
    assert summary[MarketSessionType.WEEKEND.value] == 1
    assert summary[MarketSessionType.EARLY_CLOSE.value] == 1
    assert summary[MarketSessionType.UNKNOWN.value] == 1

    # The 'invalid_date' evaluates to REGULAR in classify_timestamp_session if it reaches the end and time logic fails/returns default
    # Actually, timestamp length < 10 returns UNKNOWN in classify_timestamp_session:
    # "invalid_d" (9 chars) -> UNKNOWN. "invalid_date" (12 chars) -> date="invalid_da", time="t" -> REGULAR fallback since len(time_part)<5
    assert summary[MarketSessionType.REGULAR.value] == 1


def test_classify_rows_by_session_fallback():
    from unittest.mock import patch
    import usa_signal_bot.calendar.session_classifier as sc

    cal = LocalMarketCalendar()

    # We return the string value of REGULAR to avoid KeyError and test the `else str(session)` branch
    def mock_classify(row, calendar):
        return MarketSessionType.REGULAR.value

    with patch.object(sc, "classify_bar_session", side_effect=mock_classify):
        rows = [{"timestamp": "2024-01-02 12:00"}]
        summary = sc.classify_rows_by_session(rows, cal)
        assert summary[MarketSessionType.REGULAR.value] == 1


def test_classify_bar_session():
    from usa_signal_bot.calendar.session_classifier import classify_bar_session

    cal = LocalMarketCalendar()

    # Test timestamp presence
    row_timestamp = {"timestamp": "2024-01-02 08:00"}
    assert classify_bar_session(row_timestamp, cal) == MarketSessionType.PREMARKET

    # Test date fallback
    row_date = {"date": "2024-01-02 16:30"}
    assert classify_bar_session(row_date, cal) == MarketSessionType.AFTER_HOURS

    # Test both missing
    row_empty = {}
    assert classify_bar_session(row_empty, cal) == MarketSessionType.UNKNOWN

    # Test both present (timestamp should take precedence)
    row_both = {"timestamp": "2024-01-02 12:00", "date": "2024-01-02 16:30"}
    assert classify_bar_session(row_both, cal) == MarketSessionType.REGULAR


def test_session_type_to_signal_guard():
    from usa_signal_bot.calendar.session_classifier import session_type_to_signal_guard
    from usa_signal_bot.core.enums import MarketSessionType

    guard_regular = session_type_to_signal_guard(MarketSessionType.REGULAR)
    assert guard_regular["is_trading_allowed"] is True
    assert guard_regular["warning"] is None
    assert guard_regular["metadata_flag"] == str(MarketSessionType.REGULAR)

    guard_early = session_type_to_signal_guard(MarketSessionType.EARLY_CLOSE)
    assert guard_early["is_trading_allowed"] is True
    assert guard_early["warning"] == "Session is early close."

    guard_premarket = session_type_to_signal_guard(MarketSessionType.PREMARKET)
    assert guard_premarket["is_trading_allowed"] is False
    assert guard_premarket["warning"] == "Premarket session. Proceed with caution."

    guard_after_hours = session_type_to_signal_guard(MarketSessionType.AFTER_HOURS)
    assert guard_after_hours["is_trading_allowed"] is False
    assert guard_after_hours["warning"] == "After-hours session. Proceed with caution."

    guard_weekend = session_type_to_signal_guard(MarketSessionType.WEEKEND)
    assert guard_weekend["is_trading_allowed"] is False
    assert guard_weekend["warning"] == "Weekend. Market closed."

    guard_holiday = session_type_to_signal_guard(MarketSessionType.HOLIDAY)
    assert guard_holiday["is_trading_allowed"] is False
    assert guard_holiday["warning"] == "Holiday. Market closed."

    guard_closed = session_type_to_signal_guard(MarketSessionType.CLOSED)
    assert guard_closed["is_trading_allowed"] is False
    assert guard_closed["warning"] == "Market closed."

    guard_unknown = session_type_to_signal_guard(MarketSessionType.UNKNOWN)
    assert guard_unknown["is_trading_allowed"] is False
    assert guard_unknown["warning"] == "Unknown session type."


def test_classify_timestamp_session_edge_cases():
    cal = LocalMarketCalendar()

    # Empty or short string
    assert classify_timestamp_session("", cal) == MarketSessionType.UNKNOWN
    assert classify_timestamp_session("2024", cal) == MarketSessionType.UNKNOWN

    # Missing " " and "T" separator (assumes REGULAR for daily)
    assert classify_timestamp_session("2024-01-02_08:00", cal) == MarketSessionType.REGULAR

    # Malformed time part (len < 5)
    assert classify_timestamp_session("2024-01-02 12", cal) == MarketSessionType.REGULAR

    # T separator usage
    assert classify_timestamp_session("2024-01-02T08:00", cal) == MarketSessionType.PREMARKET
    assert classify_timestamp_session("2024-01-02T12:00", cal) == MarketSessionType.REGULAR
    assert classify_timestamp_session("2024-01-02T16:30", cal) == MarketSessionType.AFTER_HOURS

def test_classify_timestamp_session_holiday():
    from unittest.mock import patch
    cal = LocalMarketCalendar()
    with patch.object(cal, "is_holiday", return_value=True):
        assert classify_timestamp_session("2024-01-01", cal) == MarketSessionType.HOLIDAY
