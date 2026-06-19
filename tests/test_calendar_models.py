"""Test calendar models."""

import pytest
from usa_signal_bot.calendar.calendar_models import (
    CalendarReviewResult,
    calendar_review_result_to_dict,
    TradingDayResult,
    trading_day_result_to_dict,
    MarketHoliday,
    MarketEarlyClose,
    MarketSession,
    SessionValidationResult,
    session_validation_result_to_dict,
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



def test_market_early_close_invalid_date():
    c = MarketEarlyClose(
        "2024-13-45",
        "13:00",
        "Early Close",
        MarketCalendarName.US_EQUITIES,
        CalendarDataSource.STATIC_DEFAULT,
    )
    with pytest.raises(MarketCalendarError):
        validate_market_early_close(c)


def test_market_early_close_invalid_time():
    c = MarketEarlyClose(
        "2024-07-03",
        "13:00:00",
        "Early Close",
        MarketCalendarName.US_EQUITIES,
        CalendarDataSource.STATIC_DEFAULT,
    )
    with pytest.raises(MarketCalendarError):
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


def test_trading_day_result_to_dict_with_session():
    from unittest.mock import MagicMock

    cal_mock = MagicMock()
    cal_mock.value = "US_EQUITIES"
    day_type_mock = MagicMock()
    day_type_mock.value = "TRADING_DAY"
    session_type_mock = MagicMock()
    session_type_mock.value = "REGULAR"
    source_mock = MagicMock()
    source_mock.value = "STATIC_DEFAULT"

    session_mock = MarketSession(
        session_id="session_1",
        calendar_name=cal_mock,
        date="2024-01-02",
        session_type=session_type_mock,
        open_time_local="09:30",
        close_time_local="16:00",
        timezone="America/New_York",
        is_trading_session=True,
        is_early_close=False,
        source=source_mock,
        warnings=["session_warn"],
        errors=["session_err"],
    )

    result = TradingDayResult(
        result_id="res_1",
        calendar_name=cal_mock,
        date="2024-01-02",
        day_type=day_type_mock,
        is_trading_day=True,
        previous_trading_day="2023-12-29",
        next_trading_day="2024-01-03",
        session=session_mock,
        warnings=["warn_1"],
        errors=["err_1"],
    )

    d = trading_day_result_to_dict(result)

    assert d["result_id"] == "res_1"
    assert d["calendar_name"] == "US_EQUITIES"
    assert d["date"] == "2024-01-02"
    assert d["day_type"] == "TRADING_DAY"
    assert d["is_trading_day"] is True
    assert d["previous_trading_day"] == "2023-12-29"
    assert d["next_trading_day"] == "2024-01-03"
    assert d["warnings"] == ["warn_1"]
    assert d["errors"] == ["err_1"]
    assert d["session"] is not None
    assert d["session"]["session_id"] == "session_1"
    assert d["session"]["calendar_name"] == "US_EQUITIES"
    assert d["session"]["warnings"] == ["session_warn"]
    assert d["session"]["errors"] == ["session_err"]


def test_trading_day_result_to_dict_without_session():
    from unittest.mock import MagicMock

    cal_mock = MagicMock()
    cal_mock.value = "US_EQUITIES"
    day_type_mock = MagicMock()
    day_type_mock.value = "HOLIDAY"

    result = TradingDayResult(
        result_id="res_2",
        calendar_name=cal_mock,
        date="2024-01-01",
        day_type=day_type_mock,
        is_trading_day=False,
        previous_trading_day="2023-12-29",
        next_trading_day="2024-01-02",
        session=None,
        warnings=[],
        errors=[],
    )

    d = trading_day_result_to_dict(result)

    assert d["result_id"] == "res_2"
    assert d["calendar_name"] == "US_EQUITIES"
    assert d["date"] == "2024-01-01"
    assert d["day_type"] == "HOLIDAY"
    assert d["is_trading_day"] is False
    assert d["session"] is None


def test_market_holiday_to_dict():
    from unittest.mock import MagicMock
    from usa_signal_bot.calendar.calendar_models import (
        market_holiday_to_dict,
        MarketHoliday,
    )

    cal_mock = MagicMock()
    cal_mock.value = "US_EQUITIES"
    source_mock = MagicMock()
    source_mock.value = "STATIC_DEFAULT"

    h = MarketHoliday(
        date="2024-01-01",
        name="New Year",
        calendar_name=cal_mock,
        source=source_mock,
        metadata={"key": "value"},
    )
    d = market_holiday_to_dict(h)
    assert d["date"] == "2024-01-01"
    assert d["name"] == "New Year"
    assert d["calendar_name"] == "US_EQUITIES"
    assert d["source"] == "STATIC_DEFAULT"
    assert d["metadata"] == {"key": "value"}


def test_market_early_close_to_dict():
    from unittest.mock import MagicMock
    from usa_signal_bot.calendar.calendar_models import (
        market_early_close_to_dict,
        MarketEarlyClose,
    )

    cal_mock = MagicMock()
    cal_mock.value = "US_EQUITIES"
    source_mock = MagicMock()
    source_mock.value = "STATIC_DEFAULT"

    c = MarketEarlyClose(
        date="2024-07-03",
        close_time_local="13:00",
        name="Early Close",
        calendar_name=cal_mock,
        source=source_mock,
        metadata={"reason": "half day"},
    )
    d = market_early_close_to_dict(c)
    assert d["date"] == "2024-07-03"
    assert d["close_time_local"] == "13:00"
    assert d["name"] == "Early Close"
    assert d["calendar_name"] == "US_EQUITIES"
    assert d["source"] == "STATIC_DEFAULT"
    assert d["metadata"] == {"reason": "half day"}


def test_session_validation_result_to_dict():
    from unittest.mock import MagicMock

    cal_mock = MagicMock()
    cal_mock.value = "US_EQUITIES"
    status_mock = MagicMock()
    status_mock.value = "VALID"

    result = SessionValidationResult(
        validation_id="val_1",
        created_at_utc="2024-01-01T00:00:00Z",
        symbol="AAPL",
        calendar_name=cal_mock,
        status=status_mock,
        row_count=252,
        trading_day_count=252,
        non_trading_day_rows=0,
        missing_trading_days=0,
        early_close_rows=2,
        warnings=["val_warn"],
        errors=["val_err"],
        metadata={"source": "api"}
    )

    d = session_validation_result_to_dict(result)

    assert d["validation_id"] == "val_1"
    assert d["created_at_utc"] == "2024-01-01T00:00:00Z"
    assert d["symbol"] == "AAPL"
    assert d["calendar_name"] == "US_EQUITIES"
    assert d["status"] == "VALID"
    assert d["row_count"] == 252
    assert d["trading_day_count"] == 252
    assert d["non_trading_day_rows"] == 0
    assert d["missing_trading_days"] == 0
    assert d["early_close_rows"] == 2
    assert d["warnings"] == ["val_warn"]
    assert d["errors"] == ["val_err"]
    assert d["metadata"] == {"source": "api"}
