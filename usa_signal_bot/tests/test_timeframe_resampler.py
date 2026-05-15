import pytest
from usa_signal_bot.regime_map.timeframe_resampler import normalize_ohlcv_rows, resample_daily_to_weekly

def test_normalize_rows():
    rows = [
        {"date": "2023-01-02", "open": 10},
        {"date": "2023-01-01", "open": 9}
    ]
    norm = normalize_ohlcv_rows(rows)
    assert norm[0]["date"] == "2023-01-01"

def test_resample_daily_to_weekly():
    rows = [
        {"date": "2023-01-02", "open": 10, "high": 12, "low": 9, "close": 11, "volume": 100}, # Monday
        {"date": "2023-01-03", "open": 11, "high": 13, "low": 10, "close": 12, "volume": 200}, # Tuesday
    ]
    weekly = resample_daily_to_weekly(rows)
    assert len(weekly) == 1
    assert weekly[0]["open"] == 10
    assert weekly[0]["high"] == 13
    assert weekly[0]["low"] == 9
    assert weekly[0]["close"] == 12
    assert weekly[0]["volume"] == 300
