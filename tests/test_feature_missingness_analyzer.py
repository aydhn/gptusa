import pytest
import pandas as pd
from usa_signal_bot.feature_engine.factor_composition.feature_missingness_analyzer import feature_missingness_summary

def test_feature_missingness_summary():
    df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02"],
        "returns_1d": [0.01, None],
        "volatility_14d": [0.02, 0.03]
    })

    summary = feature_missingness_summary(df, ["returns_1d", "volatility_14d"])
    assert summary["average_missingness"] == 0.25
    assert summary["high_missing_count"] == 1
