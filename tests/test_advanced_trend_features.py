import pytest
import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.advanced_features.advanced_trend_features import add_advanced_trend_features, validate_advanced_trend_features

def test_trend():
    df = pd.DataFrame({
        "close": np.linspace(100, 150, 100)
    })
    df_out = add_advanced_trend_features(df)
    assert "trend_slope_20" in df_out.columns
    assert "close_to_sma20_zscore_60" in df_out.columns
    assert len(validate_advanced_trend_features(df_out)) == 0
