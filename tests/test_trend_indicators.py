import pytest
import pandas as pd
from usa_signal_bot.features.trend_indicators import (
    SMAIndicator, EMAIndicator, WMAIndicator, DEMAIndicator, TEMAIndicator,
    MACDIndicator, PriceDistanceToMAIndicator, MASlopeIndicator,
    MAAlignmentIndicator, TrendStrengthBasicIndicator
)
from usa_signal_bot.core.exceptions import IndicatorParameterError, FeatureComputationError

@pytest.fixture
def df():
    return pd.DataFrame({
        "symbol": ["AAPL"]*10,
        "timeframe": ["1d"]*10,
        "timestamp_utc": pd.date_range("2023-01-01", periods=10, tz="UTC"),
        "open": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "high": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "low": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "close": [10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5],
        "volume": [100]*10
    })

def test_sma_indicator(df):
    ind = SMAIndicator()
    res = ind.compute(df, {"window": 3, "column": "close"})
    assert "close_sma_3" in res.columns
    assert "symbol" in res.columns

def test_ema_indicator(df):
    ind = EMAIndicator()
    res = ind.compute(df, {"span": 3, "column": "close"})
    assert "close_ema_3" in res.columns

def test_wma_indicator(df):
    ind = WMAIndicator()
    res = ind.compute(df, {"window": 3, "column": "close"})
    assert "close_wma_3" in res.columns

def test_dema_indicator(df):
    ind = DEMAIndicator()
    res = ind.compute(df, {"span": 3, "column": "close"})
    assert "close_dema_3" in res.columns

def test_tema_indicator(df):
    ind = TEMAIndicator()
    res = ind.compute(df, {"span": 3, "column": "close"})
    assert "close_tema_3" in res.columns

def test_macd_indicator(df):
    ind = MACDIndicator()
    res = ind.compute(df, {"fast": 3, "slow": 6, "signal": 2})
    assert "macd_3_6_2" in res.columns
    assert "macd_signal_3_6_2" in res.columns
    assert "macd_hist_3_6_2" in res.columns

def test_macd_invalid_params(df):
    ind = MACDIndicator()
    with pytest.raises(IndicatorParameterError):
        ind.compute(df, {"fast": 6, "slow": 3, "signal": 2})

def test_price_distance_indicator(df):
    ind = PriceDistanceToMAIndicator()
    res = ind.compute(df, {"ma_type": "ema", "window": 3, "price_column": "close"})
    assert "close_distance_pct_ema_3" in res.columns

def test_ma_slope_indicator(df):
    ind = MASlopeIndicator()
    res = ind.compute(df, {"ma_type": "sma", "window": 3, "slope_window": 2, "column": "close"})
    assert "close_sma_3_slope_2" in res.columns

def test_ma_alignment_indicator(df):
    ind = MAAlignmentIndicator()
    res = ind.compute(df, {"ma_type": "sma", "short_window": 2, "medium_window": 4, "long_window": 6, "column": "close"})
    assert "close_sma_alignment_2_4_6" in res.columns

def test_trend_strength_basic_indicator(df):
    ind = TrendStrengthBasicIndicator()
    res = ind.compute(df, {"fast_window": 3, "slow_window": 6, "slope_window": 2, "column": "close"})
    assert "trend_strength_basic_3_6_2" in res.columns

def test_missing_column(df):
    ind = SMAIndicator()
    with pytest.raises(IndicatorParameterError):
        ind.compute(df, {"window": 3, "column": "non_existent"})
