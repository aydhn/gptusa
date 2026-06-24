import pytest
from usa_signal_bot.provider_quality.outlier_penalty_scorer import (
    detect_basic_ohlcv_outliers,
)


def test_detect_basic_ohlcv_outliers_happy_path():
    records = [
        {"open": 100, "high": 110, "low": 90, "close": 105, "volume": 1000},
        {"open": 105, "high": 115, "low": 95, "close": 110, "volume": 1500},
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    assert len(outliers) == 0


def test_detect_basic_ohlcv_outliers_close_zero_or_negative():
    records = [
        {"open": 100, "high": 110, "low": 90, "close": 0, "volume": 1000},
        {"open": 100, "high": 110, "low": 90, "close": -5, "volume": 1000},
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    # Row 0: close <= 0, close outside high/low range
    # Row 1: close <= 0, close outside high/low range
    assert len(outliers) == 4
    assert any("close <= 0 (0.0)" in o for o in outliers)
    assert any("close <= 0 (-5.0)" in o for o in outliers)


def test_detect_basic_ohlcv_outliers_high_lt_low():
    records = [
        {"open": 100, "high": 90, "low": 110, "close": 105, "volume": 1000},
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    # This row trips multiple conditions because of the swapped high/low:
    # 1. high < low
    # 2. open (100) outside high(90)/low(110) range  [100 > 90]
    # 3. close (105) outside high/low range         [105 > 90]
    assert len(outliers) == 3
    assert any("high < low (90.0 < 110.0)" in o for o in outliers)


def test_detect_basic_ohlcv_outliers_open_outside_range():
    records = [
        {"open": 120, "high": 110, "low": 90, "close": 105, "volume": 1000},
        {"open": 80, "high": 110, "low": 90, "close": 105, "volume": 1000},
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    assert len(outliers) == 2
    assert all("open outside high/low range" in o for o in outliers)


def test_detect_basic_ohlcv_outliers_close_outside_range():
    records = [
        {"open": 100, "high": 110, "low": 90, "close": 120, "volume": 1000},
        {"open": 100, "high": 110, "low": 90, "close": 80, "volume": 1000},
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    assert len(outliers) == 2
    assert all("close outside high/low range" in o for o in outliers)


def test_detect_basic_ohlcv_outliers_negative_volume():
    records = [
        {"open": 100, "high": 110, "low": 90, "close": 105, "volume": -100},
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    assert len(outliers) == 1
    assert "volume < 0 (-100.0)" in outliers[0]


def test_detect_basic_ohlcv_outliers_type_value_errors():
    records = [
        {
            "open": "invalid",
            "high": 110,
            "low": 90,
            "close": 105,
            "volume": 1000,
        },  # ValueError
        {
            "open": 100,
            "high": None,
            "low": 90,
            "close": 105,
            "volume": 1000,
        },  # TypeError
        {
            "open": 100,
            "high": 110,
            "low": 90,
            "close": 105,
            "volume": 1000,
        },  # Good record
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    assert len(outliers) == 0


def test_detect_basic_ohlcv_outliers_missing_keys():
    records = [
        {
            "open": 100,
            "high": 110,
            "low": 90,
            "close": 105,
        },  # missing volume, defaults to 0
        {
            "high": 110,
            "low": 90,
            "volume": 1000,
        },  # missing open, close (0) -> close <= 0 outlier
    ]
    outliers = detect_basic_ohlcv_outliers(records)
    # second record misses open (defaults 0, below low 90), close (defaults 0, below 0, below low 90)
    assert len(outliers) == 3
    assert any("close <= 0 (0.0)" in o for o in outliers)
    assert any("open outside high/low range" in o for o in outliers)
    assert any("close outside high/low range" in o for o in outliers)
