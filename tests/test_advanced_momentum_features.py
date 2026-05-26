import pytest
import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.advanced_features.advanced_momentum_features import add_advanced_momentum_features, validate_advanced_momentum_features

def test_momentum():
    df = pd.DataFrame({
        "close": np.linspace(100, 150, 150)
    })
    df_out = add_advanced_momentum_features(df)
    assert "momentum_20" in df_out.columns
    assert "momentum_accel_20_60" in df_out.columns
    assert len(validate_advanced_momentum_features(df_out)) == 0
