import pytest
import pandas as pd
from usa_signal_bot.features.divergence_indicators import (
    RSIDivergenceIndicator, MACDHistogramDivergenceIndicator,
    ROCDivergenceIndicator, MFIDivergenceIndicator, OBVDivergenceIndicator
)

@pytest.fixture
def sample_df():
    # Enough bars for MACD (min_bars=35)
    df = pd.DataFrame({
        "open": range(10, 60),
        "high": range(12, 62),
        "low": range(8, 58),
        "close": range(11, 61),
        "volume": [1000] * 50
    })
    # Create some pivots manually for tests
    df.loc[10, "close"] = 20
    df.loc[15, "close"] = 15
    df.loc[25, "close"] = 25
    df.loc[30, "close"] = 12
    return df

def test_rsi_divergence_indicator(sample_df):
    ind = RSIDivergenceIndicator()
    res = ind.compute(sample_df)

    expected_cols = [
        "rsi_regular_bullish_divergence", "rsi_regular_bearish_divergence",
        "rsi_hidden_bullish_divergence", "rsi_hidden_bearish_divergence",
        "rsi_divergence_strength", "rsi_latest_divergence_code"
    ]
    for c in expected_cols:
        assert c in res.columns

def test_macd_hist_divergence_indicator(sample_df):
    ind = MACDHistogramDivergenceIndicator()
    res = ind.compute(sample_df)
    assert "macd_hist_latest_divergence_code" in res.columns

def test_mfi_divergence_indicator(sample_df):
    ind = MFIDivergenceIndicator()
    res = ind.compute(sample_df)
    assert "mfi_latest_divergence_code" in res.columns
