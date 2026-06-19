"""Test calendar reporting."""

from usa_signal_bot.calendar.calendar_reporting import (
    calendar_limitations_text,
    market_session_to_text,
    calendar_store_summary_to_text,
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


def test_calendar_review_result_to_text():
    from usa_signal_bot.calendar.calendar_models import (
        CalendarReviewResult,
        SessionValidationResult,
        TradingDayResult,
    )
    from usa_signal_bot.calendar.calendar_reporting import (
        calendar_review_result_to_text,
    )

    class DummyEnum:
        def __init__(self, value):
            self.value = value

    session_validation = SessionValidationResult(
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

    trading_day_result = TradingDayResult(
        result_id="td1",
        calendar_name=DummyEnum("NYSE"),
        date="2023-10-27",
        day_type=DummyEnum("STANDARD"),
        is_trading_day=True,
        previous_trading_day="2023-10-26",
        next_trading_day="2023-10-30",
        session=None,
        warnings=[],
        errors=[],
    )

    result = CalendarReviewResult(
        review_id="rev123",
        created_at_utc="2023-10-27T10:00:00Z",
        report_type=DummyEnum("FULL"),
        calendar_name=DummyEnum("NYSE"),
        sessions=[],
        trading_day_results=[trading_day_result],
        session_validations=[session_validation],
        output_paths={},
        warnings=[],
        errors=["Error 1", "Error 2"],
    )

    text = calendar_review_result_to_text(result)
    assert "=== Calendar Review: rev123 ===" in text
    assert "Report Type: FULL" in text
    assert "Calendar: NYSE" in text
    assert "Created: 2023-10-27T10:00:00Z" in text
    assert "Total Trading Days Checked: 1" in text
    assert "Total Validations: 1" in text
    assert "Errors:" in text
    assert "  - Error 1" in text
    assert "  - Error 2" in text
    assert "Session Validation Highlights:" in text
    assert "  AAPL: VALID (Missing: 0, Non-trading: 0)" in text
    assert "... and" not in text


def test_calendar_review_result_to_text_with_limit():
    from usa_signal_bot.calendar.calendar_models import (
        CalendarReviewResult,
        SessionValidationResult,
    )
    from usa_signal_bot.calendar.calendar_reporting import (
        calendar_review_result_to_text,
    )

    class DummyEnum:
        def __init__(self, value):
            self.value = value

    session_validation_1 = SessionValidationResult(
        validation_id="val1",
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

    session_validation_2 = SessionValidationResult(
        validation_id="val2",
        created_at_utc="2023-10-27T00:00:00Z",
        symbol="MSFT",
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

    result = CalendarReviewResult(
        review_id="rev123",
        created_at_utc="2023-10-27T10:00:00Z",
        report_type=DummyEnum("FULL"),
        calendar_name=DummyEnum("NYSE"),
        sessions=[],
        trading_day_results=[],
        session_validations=[session_validation_1, session_validation_2],
        output_paths={},
        warnings=[],
        errors=[],
    )

    text = calendar_review_result_to_text(result, limit=1)
    assert "Total Validations: 2" in text
    assert "  AAPL: VALID" in text
    assert "  MSFT: VALID" not in text
    assert "  ... and 1 more." in text

def test_calendar_store_summary_to_text():
    # Test with empty summary to verify defaults
    empty_summary = {}
    text_empty = calendar_store_summary_to_text(empty_summary)
    assert "=== Calendar Store Summary ===" in text_empty
    assert "Reviews count: 0" in text_empty
    assert "Latest review: None" in text_empty
    assert "Validations count: 0" in text_empty
    assert "Session files count: 0" in text_empty

    # Test with populated summary
    populated_summary = {
        'reviews_count': 5,
        'latest_review': '2023-10-27T10:00:00Z',
        'validations_count': 500,
        'sessions_files_count': 10
    }
    text_populated = calendar_store_summary_to_text(populated_summary)
    assert "=== Calendar Store Summary ===" in text_populated
    assert "Reviews count: 5" in text_populated
    assert "Latest review: 2023-10-27T10:00:00Z" in text_populated
    assert "Validations count: 500" in text_populated
    assert "Session files count: 10" in text_populated
