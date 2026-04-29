import pytest
from pathlib import Path
from usa_signal_bot.data.cache import (
    market_data_cache_dir, build_market_data_cache_filename,
    build_market_data_cache_path, write_ohlcv_bars_cache,
    read_ohlcv_bars_cache, cache_exists, is_cache_fresh, split_bars_by_symbol
)
from usa_signal_bot.data.models import OHLCVBar
import time

def test_market_data_cache_dir(tmp_path):
    cache_dir = market_data_cache_dir(tmp_path)
    assert cache_dir.exists()
    assert cache_dir.name == "market_data"

def test_build_market_data_cache_filename():
    filename = build_market_data_cache_filename("yfinance", "AAPL", "1d", "2023-01-01", "2023-01-31")
    assert filename == "yfinance_AAPL_1d_20230101_20230131.jsonl"

    filename_none = build_market_data_cache_filename("mock", "SPY", "1h", None, None)
    assert filename_none == "mock_SPY_1h_start_end.jsonl"

def test_build_market_data_cache_path(tmp_path):
    path = build_market_data_cache_path(tmp_path, "yf", "AAPL", "1d", None, None)
    assert path.parent.name == "market_data"
    assert path.name == "yf_AAPL_1d_start_end.jsonl"

def test_write_read_ohlcv_bars_cache(tmp_path):
    bars = [
        OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=101.0, volume=1000.0)
    ]
    path = tmp_path / "cache.jsonl"
    write_ohlcv_bars_cache(path, bars)

    assert cache_exists(path)

    data = read_ohlcv_bars_cache(path)
    assert len(data) == 1
    assert data[0]["symbol"] == "AAPL"

def test_is_cache_fresh(tmp_path):
    path = tmp_path / "test.txt"
    path.write_text("test")

    assert is_cache_fresh(path, 3600) is True
    # Sleep is annoying in tests, let's just test the logic that passing small ttl returns false
    # if we fake mtime or just use a 0 ttl
    assert is_cache_fresh(path, 0) is False

def test_split_bars_by_symbol():
    bars = [
        OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10, high=10, low=10, close=10, volume=10),
        OHLCVBar(symbol="MSFT", timestamp_utc="1", timeframe="1d", open=10, high=10, low=10, close=10, volume=10),
        OHLCVBar(symbol="AAPL", timestamp_utc="2", timeframe="1d", open=10, high=10, low=10, close=10, volume=10)
    ]
    grouped = split_bars_by_symbol(bars)
    assert len(grouped) == 2
    assert len(grouped["AAPL"]) == 2
    assert len(grouped["MSFT"]) == 1
