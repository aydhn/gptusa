from usa_signal_bot.regime_map.timeframe_resampler import resample_daily_to_weekly, normalize_ohlcv_rows
import pytest

def test_normalize_rows_sorts():
    rows = [
        {"date": "2024-01-02", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1},
        {"date": "2024-01-01", "open": 2, "high": 2, "low": 2, "close": 2, "volume": 2}
    ]
    res = normalize_ohlcv_rows(rows)
    assert res[0]["date"] == "2024-01-01"

def test_daily_to_weekly():
    rows = [
        {"date": "2024-01-01", "open": 10, "high": 12, "low": 9, "close": 11, "volume": 100},
        {"date": "2024-01-02", "open": 11, "high": 15, "low": 10, "close": 14, "volume": 200},
        {"date": "2024-01-03", "open": 14, "high": 14, "low": 8, "close": 9, "volume": 150},
    ] # Note: Dates are Mon, Tue, Wed of same week roughly.
    res = resample_daily_to_weekly(rows)
    assert len(res) == 1
    assert res[0]["open"] == 10
    assert res[0]["high"] == 15
    assert res[0]["low"] == 8
    assert res[0]["close"] == 9
    assert res[0]["volume"] == 450
