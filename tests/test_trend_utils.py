import pytest
import pandas as pd
import numpy as np
from usa_signal_bot.features.trend_utils import (
    calculate_sma, calculate_ema, calculate_wma, calculate_dema, calculate_tema,
    calculate_macd, calculate_series_slope, calculate_price_distance_pct,
    calculate_ma_alignment_score, validate_window, validate_macd_params
)
from usa_signal_bot.core.exceptions import IndicatorParameterError

@pytest.fixture
def sample_series():
    return pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], dtype=float)

def test_calculate_sma(sample_series):
    sma = calculate_sma(sample_series, window=3)
    assert pd.isna(sma.iloc[0])
    assert pd.isna(sma.iloc[1])
    assert np.isclose(sma.iloc[2], 11.0) # (10+11+12)/3

def test_calculate_ema(sample_series):
    ema = calculate_ema(sample_series, span=3)
    assert not pd.isna(ema.iloc[0])
    assert len(ema) == len(sample_series)

def test_calculate_wma(sample_series):
    wma = calculate_wma(sample_series, window=3)
    assert pd.isna(wma.iloc[0])
    assert pd.isna(wma.iloc[1])
    # weights: 1, 2, 3
    # values: 10, 11, 12 -> (10*1 + 11*2 + 12*3) / 6 = 11.333
    assert np.isclose(wma.iloc[2], (10*1 + 11*2 + 12*3)/6)

def test_calculate_dema(sample_series):
    dema = calculate_dema(sample_series, span=3)
    assert len(dema) == len(sample_series)

def test_calculate_tema(sample_series):
    tema = calculate_tema(sample_series, span=3)
    assert len(tema) == len(sample_series)

def test_calculate_macd(sample_series):
    df = calculate_macd(sample_series, fast=3, slow=5, signal=2)
    assert "macd_3_5_2" in df.columns
    assert "macd_signal_3_5_2" in df.columns
    assert "macd_hist_3_5_2" in df.columns

def test_calculate_series_slope(sample_series):
    slope = calculate_series_slope(sample_series, window=2)
    assert pd.isna(slope.iloc[0])
    # slope at index 2 (val 12) from index 0 (val 10) = (12 - 10)/2 = 1.0
    assert np.isclose(slope.iloc[2], 1.0)

def test_calculate_price_distance_pct(sample_series):
    ref = pd.Series([10]*len(sample_series))
    dist = calculate_price_distance_pct(sample_series, ref)
    # index 1: (11-10)/10 = 0.1
    assert np.isclose(dist.iloc[1], 0.1)

def test_calculate_ma_alignment_score():
    short = pd.Series([12, 10, 15])
    medium = pd.Series([11, 11, 14])
    long = pd.Series([10, 12, 13])

    score = calculate_ma_alignment_score({"short": short, "medium": medium, "long": long})
    assert score.iloc[0] == 1  # 12 > 11 > 10
    assert score.iloc[1] == -1 # 10 < 11 < 12
    assert score.iloc[2] == 1  # 15 > 14 > 13

def test_validate_window():
    validate_window(10, "test")
    with pytest.raises(IndicatorParameterError):
        validate_window("10", "test")
    with pytest.raises(IndicatorParameterError):
        validate_window(-1, "test")

def test_validate_macd_params():
    validate_macd_params(12, 26, 9)
    with pytest.raises(IndicatorParameterError):
        validate_macd_params(26, 12, 9)
