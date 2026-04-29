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

from usa_signal_bot.data.cache import list_market_data_cache_files, cache_file_age_seconds, cache_file_size, validate_cache_file, write_repaired_cache, cache_summary
from usa_signal_bot.core.enums import DataQualityStatus
import os

def test_list_market_data_cache_files(tmp_path):
    path = tmp_path / "cache" / "market_data"
    path.mkdir(parents=True)
    (path / "file1.jsonl").write_text("{}")
    (path / "file2.jsonl").write_text("{}")

    files = list_market_data_cache_files(tmp_path)
    assert len(files) == 2

def test_cache_file_age_size(tmp_path):
    f = tmp_path / "test.jsonl"
    f.write_text("hello")

    age = cache_file_age_seconds(f)
    assert age is not None
    assert age >= 0

    size = cache_file_size(f)
    assert size == 5

def test_validate_cache_file(tmp_path):
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10, high=10, low=10, close=10, volume=10)
    path = build_market_data_cache_path(tmp_path, "mock", "AAPL", "1d", None, None)
    write_ohlcv_bars_cache(path, [bar])

    report = validate_cache_file(path)
    assert report.status == DataQualityStatus.OK

def test_write_repaired_cache(tmp_path):
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10, high=10, low=10, close=10, volume=10)
    path = tmp_path / "repaired.jsonl"
    write_repaired_cache(path, [bar])
    assert path.exists()

def test_cache_summary(tmp_path):
    path = tmp_path / "cache" / "market_data"
    path.mkdir(parents=True)
    f1 = path / "a.jsonl"
    f1.write_text("hello")
    f2 = path / "b.jsonl"
    f2.write_text("world!")

    # ensure f2 is newer
    mtime = f1.stat().st_mtime
    os.utime(f2, (mtime, mtime + 10))

    summary = cache_summary(tmp_path)
    assert summary["file_count"] == 2
    assert summary["total_size_bytes"] == 11
    assert summary["newest_file"] == "b.jsonl"

def test_list_cache_files_for_timeframe(tmp_path):
    from usa_signal_bot.data.cache import list_cache_files_for_timeframe, market_data_cache_dir
    d = market_data_cache_dir(tmp_path)
    d.mkdir(parents=True, exist_ok=True)
    (d / "yfinance_AAPL_1d.jsonl").touch()
    (d / "yfinance_MSFT_1h.jsonl").touch()

    files = list_cache_files_for_timeframe(tmp_path, "1d")
    assert len(files) == 1
    assert "AAPL" in files[0].name

def test_market_data_cache_summary_by_timeframe(tmp_path):
    from usa_signal_bot.data.cache import market_data_cache_summary_by_timeframe, market_data_cache_dir
    d = market_data_cache_dir(tmp_path)
    d.mkdir(parents=True, exist_ok=True)
    (d / "yfinance_AAPL_1d.jsonl").touch()
    (d / "yfinance_MSFT_1d.jsonl").touch()
    (d / "yfinance_MSFT_1h.jsonl").touch()

    summary = market_data_cache_summary_by_timeframe(tmp_path)
    assert "1d" in summary
    assert summary["1d"]["count"] == 2
    assert "1h" in summary
    assert summary["1h"]["count"] == 1
