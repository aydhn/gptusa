"""Test calendar store."""
from usa_signal_bot.calendar.calendar_store import write_market_sessions_jsonl
from usa_signal_bot.calendar.calendar_models import MarketSession
from usa_signal_bot.core.exceptions import CalendarStorageError
from usa_signal_bot.core.enums import MarketSessionType, CalendarDataSource
import json
from unittest.mock import patch
import pytest
from usa_signal_bot.calendar.calendar_store import calendar_store_dir, write_calendar_review_result_json, list_calendar_reviews
from usa_signal_bot.calendar.calendar_models import CalendarReviewResult
from usa_signal_bot.core.enums import CalendarReportType, MarketCalendarName

def test_calendar_store(tmp_path):
    res = CalendarReviewResult("id", "2024", CalendarReportType.CALENDAR_SUMMARY, MarketCalendarName.US_EQUITIES, [], [], [])
    p = write_calendar_review_result_json(tmp_path / "calendar" / "reviews" / "rev.json", res)
    assert p.exists()
    assert len(list_calendar_reviews(tmp_path)) == 1



def test_write_market_sessions_jsonl(tmp_path):

    sessions = [
        MarketSession(
            session_id="session_1",
            calendar_name=MarketCalendarName.US_EQUITIES,
            date="2024-01-01",
            session_type=MarketSessionType.REGULAR_TRADING,
            open_time_local="09:30",
            close_time_local="16:00",
            timezone="America/New_York",
            is_trading_session=True,
            is_early_close=False,
            source=CalendarDataSource.FILE,
            warnings=[],
            errors=[]
        ),
        MarketSession(
            session_id="session_2",
            calendar_name=MarketCalendarName.US_EQUITIES,
            date="2024-01-02",
            session_type=MarketSessionType.REGULAR_TRADING,
            open_time_local="09:30",
            close_time_local="16:00",
            timezone="America/New_York",
            is_trading_session=True,
            is_early_close=False,
            source=CalendarDataSource.FILE,
            warnings=[],
            errors=[]
        )
    ]

    out_file = tmp_path / "sessions.jsonl"
    result_path = write_market_sessions_jsonl(out_file, sessions)

    assert result_path.exists()
    assert result_path == out_file

    with open(result_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 2

        data1 = json.loads(lines[0])
        assert data1["session_id"] == "session_1"
        assert data1["date"] == "2024-01-01"

def test_write_market_sessions_jsonl_error(tmp_path):

    sessions = [
        MarketSession(
            session_id="session_1",
            calendar_name=MarketCalendarName.US_EQUITIES,
            date="2024-01-01",
            session_type=MarketSessionType.REGULAR_TRADING,
            open_time_local="09:30",
            close_time_local="16:00",
            timezone="America/New_York",
            is_trading_session=True,
            is_early_close=False,
            source=CalendarDataSource.FILE,
            warnings=[],
            errors=[]
        )
    ]

    out_file = tmp_path / "sessions.jsonl"

    # Force an error by patching open
    with patch("builtins.open", side_effect=PermissionError("Mocked PermissionError")):
        with pytest.raises(CalendarStorageError, match="Failed to write sessions to"):
            write_market_sessions_jsonl(out_file, sessions)
