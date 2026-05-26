import pytest
import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.advanced_features.advanced_volatility_features import add_advanced_volatility_features, validate_advanced_volatility_features

def test_add_advanced_volatility_features():
    df = pd.DataFrame({
        "close": np.linspace(100, 150, 100),
        "high": np.linspace(102, 152, 100),
        "low": np.linspace(98, 148, 100)
    })

    df_out = add_advanced_volatility_features(df)

    assert "realized_vol_10" in df_out.columns
    assert "realized_vol_20" in df_out.columns
    assert "downside_vol_20" in df_out.columns
    assert "vol_of_vol_20" in df_out.columns
    assert "atr_percentile_60" in df_out.columns

    errors = validate_advanced_volatility_features(df_out)
    assert len(errors) == 0
