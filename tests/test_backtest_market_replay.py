import pytest
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.market_replay import (
    filter_bars_by_date, build_market_bar_events, get_bar_by_symbol_time, get_next_bar_for_symbol,
    MarketReplayData, MarketReplayRequest
)

def test_filter_bars():
    b1 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=100.0, volume=1000)
    b2 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-02T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=100.0, volume=1000)
    b3 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-03T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=100.0, volume=1000)

    filtered = filter_bars_by_date([b1, b2, b3], "2023-01-02T00:00:00Z", "2023-01-02T23:59:59Z")
    assert len(filtered) == 1
    assert filtered[0] == b2

def test_build_market_events():
    req = MarketReplayRequest(["AAPL"], "1d")
    data = MarketReplayData(req, {"AAPL": [OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=100.0, volume=1000)]}, ["2023-01-01T00:00:00Z"])
    events = build_market_bar_events(data)
    assert len(events) == 1
    assert events[0].symbol == "AAPL"

def test_get_bars():
    req = MarketReplayRequest(["AAPL"], "1d")
    b1 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=100.0, volume=1000)
    b2 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-02T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=100.0, volume=1000)
    data = MarketReplayData(req, {"AAPL": [b1, b2]}, [])

    assert get_bar_by_symbol_time(data, "AAPL", "2023-01-01T00:00:00Z") == b1
    assert get_next_bar_for_symbol(data, "AAPL", "2023-01-01T00:00:00Z") == b2
