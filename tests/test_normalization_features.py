import pytest
import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.advanced_features.normalization_features import add_normalization_features

def test_normalization():
    df = pd.DataFrame({
        "close": np.linspace(100, 150, 100)
    })
    df_out, res = add_normalization_features(df, ["close"])
    assert "close_zscore_60" in df_out.columns
    assert "close_percentile_60" in df_out.columns
    assert len(res) == 2
