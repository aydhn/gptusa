import pytest
from usa_signal_bot.data.timeframes import (
    timeframe_to_yfinance_interval, normalize_timeframe, validate_timeframe_for_yfinance,
    is_intraday_timeframe, is_daily_or_higher_timeframe
)
from usa_signal_bot.core.enums import TimeFrame
from usa_signal_bot.core.exceptions import DataProviderError

def test_timeframe_to_yfinance_interval_enum():
    assert timeframe_to_yfinance_interval(TimeFrame.ONE_DAY.value) == "1d"
    assert timeframe_to_yfinance_interval(TimeFrame.ONE_WEEK.value) == "1wk"
    assert timeframe_to_yfinance_interval(TimeFrame.ONE_HOUR.value) == "1h"
    assert timeframe_to_yfinance_interval(TimeFrame.FIFTEEN_MINUTES.value) == "15m"

def test_timeframe_to_yfinance_interval_str():
    assert timeframe_to_yfinance_interval("1d") == "1d"
    assert timeframe_to_yfinance_interval("1wk") == "1wk"
    assert timeframe_to_yfinance_interval("15m") == "15m"

def test_timeframe_to_yfinance_interval_invalid():
    with pytest.raises(DataProviderError):
        timeframe_to_yfinance_interval("1y")
    with pytest.raises(DataProviderError):
        timeframe_to_yfinance_interval("invalid")

def test_normalize_timeframe():
    assert normalize_timeframe("1d") == "1d"
    assert normalize_timeframe(TimeFrame.ONE_HOUR.value) == "1h"

def test_validate_timeframe_for_yfinance():
    validate_timeframe_for_yfinance("1d") # Should not raise
    with pytest.raises(DataProviderError):
        validate_timeframe_for_yfinance("1y")

def test_is_intraday_timeframe():
    assert is_intraday_timeframe("1m") is True
    assert is_intraday_timeframe("15m") is True
    assert is_intraday_timeframe("1h") is True
    assert is_intraday_timeframe("1d") is False
    assert is_intraday_timeframe("1wk") is False

def test_is_daily_or_higher_timeframe():
    assert is_daily_or_higher_timeframe("1m") is False
    assert is_daily_or_higher_timeframe("1h") is False
    assert is_daily_or_higher_timeframe("1d") is True
    assert is_daily_or_higher_timeframe("1wk") is True
