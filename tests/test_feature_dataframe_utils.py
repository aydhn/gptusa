import pytest
import pandas as pd
import numpy as np

from usa_signal_bot.features.dataframe_utils import (
    bars_to_dataframe, dataframe_to_feature_rows,
    ensure_ohlcv_dataframe_columns, sort_ohlcv_dataframe,
    add_symbol_timeframe_columns, normalize_feature_dataframe
)
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.exceptions import FeatureComputationError

@pytest.fixture
def fake_bars():
    return [
        OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc="2023-01-02T00:00:00+00:00", open=1.5, high=2.5, low=1.5, close=2, volume=20),
        OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc="2023-01-01T00:00:00+00:00", open=1, high=2, low=1, close=1.5, volume=10)
    ]

def test_bars_to_dataframe(fake_bars):
    df = bars_to_dataframe(fake_bars)
    assert not df.empty
    assert "timestamp_utc" in df.columns
    assert "close" in df.columns
    assert df["timestamp_utc"].iloc[0] == "2023-01-01T00:00:00+00:00"

def test_ensure_ohlcv_dataframe_columns():
    df = pd.DataFrame({"close": [1, 2, 3]})
    with pytest.raises(FeatureComputationError, match="missing required OHLCV columns"):
        ensure_ohlcv_dataframe_columns(df)

    df2 = pd.DataFrame({
        "timestamp_utc": ["2023-01-01"], "open": [1], "high": [2],
        "low": [1], "close": [1.5], "volume": [100]
    })
    ensure_ohlcv_dataframe_columns(df2)

def test_dataframe_to_feature_rows():
    df = pd.DataFrame({
        "timestamp_utc": ["2023-01-01"],
        "close_sma_10": [10.5],
        "close_return": [np.nan]
    })

    rows = dataframe_to_feature_rows(df, "AAPL", "1d")
    assert len(rows) == 1
    assert rows[0].symbol == "AAPL"
    assert rows[0].features["close_sma_10"] == 10.5
    assert rows[0].features["close_return"] is None

def test_normalize_feature_dataframe():
    df = pd.DataFrame({
        "timestamp_utc": ["2023-01-01"],
        "symbol": ["AAPL"],
        "timeframe": ["1d"],
        "feat1": ["10.5"],
        "feat2": ["invalid"]
    })

    df_norm = normalize_feature_dataframe(df)
    assert pd.api.types.is_numeric_dtype(df_norm["feat1"])
    assert df_norm["feat1"].iloc[0] == 10.5
    assert pd.isna(df_norm["feat2"].iloc[0])
