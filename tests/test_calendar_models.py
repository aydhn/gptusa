"""Test calendar models."""

import pytest
from usa_signal_bot.calendar.calendar_models import (
    CalendarReviewResult,
    calendar_review_result_to_dict,
    MarketHoliday,
    MarketEarlyClose,
    MarketSession,
    validate_market_holiday,
    validate_market_early_close,
    validate_market_session,
    create_market_session_id,
)
from usa_signal_bot.core.enums import (
    MarketCalendarName,
    CalendarDataSource,
    MarketSessionType,
)
from usa_signal_bot.core.exceptions import MarketCalendarError


def test_market_holiday_valid():
    h = MarketHoliday(
        "2024-01-01",
        "New Year",
        MarketCalendarName.US_EQUITIES,
        CalendarDataSource.STATIC_DEFAULT,
    )
    validate_market_holiday(h)


def test_market_holiday_invalid():
    h = MarketHoliday(
        "2024-13-45",
        "Invalid",
        MarketCalendarName.US_EQUITIES,
        CalendarDataSource.STATIC_DEFAULT,
    )
    with pytest.raises(MarketCalendarError):
        validate_market_holiday(h)


def test_market_early_close_valid():
    c = MarketEarlyClose(
        "2024-07-03",
        "13:00",
        "Early Close",
        MarketCalendarName.US_EQUITIES,
        CalendarDataSource.STATIC_DEFAULT,
    )
    validate_market_early_close(c)


def test_market_session_valid():
    s = MarketSession(
        "id",
        MarketCalendarName.US_EQUITIES,
        "2024-01-02",
        MarketSessionType.REGULAR,
        "09:30",
        "16:00",
        "America/New_York",
        True,
        False,
        CalendarDataSource.STATIC_DEFAULT,
    )
    validate_market_session(s)


def test_market_session_invalid_time():
    s = MarketSession(
        "id",
        MarketCalendarName.US_EQUITIES,
        "2024-01-02",
        MarketSessionType.REGULAR,
        "16:00",
        "09:30",
        "America/New_York",
        True,
        False,
        CalendarDataSource.STATIC_DEFAULT,
    )
    with pytest.raises(MarketCalendarError):
        validate_market_session(s)


def test_market_session_id_factory():
    sid = create_market_session_id(MarketCalendarName.US_EQUITIES, "2024-01-02")
    assert "US_EQUITIES" in sid
    assert "2024-01-02" in sid


def test_calendar_review_result_to_dict():
    from unittest.mock import MagicMock

    report_mock = MagicMock()
    report_mock.value = "ANNUAL"
    cal_mock = MagicMock()
    cal_mock.value = "US_EQUITIES"

    result = CalendarReviewResult(
        review_id="rev_1",
        created_at_utc="2024-01-01T00:00:00Z",
        report_type=report_mock,
        calendar_name=cal_mock,
        sessions=[],
        trading_day_results=[],
        session_validations=[],
        output_paths={"path": "/output"},
        warnings=["warning 1"],
        errors=["error 1"],
    )
    d = calendar_review_result_to_dict(result)
    assert d["review_id"] == "rev_1"
    assert d["created_at_utc"] == "2024-01-01T00:00:00Z"
    assert d["report_type"] == "ANNUAL"
    assert d["calendar_name"] == "US_EQUITIES"
    assert d["sessions"] == []
    assert d["trading_day_results"] == []
    assert d["session_validations"] == []
    assert d["output_paths"] == {"path": "/output"}
    assert d["warnings"] == ["warning 1"]
    assert d["errors"] == ["error 1"]
