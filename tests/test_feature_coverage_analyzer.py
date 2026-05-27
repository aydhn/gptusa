import pytest
import pandas as pd
from usa_signal_bot.feature_engine.factor_composition.feature_coverage_analyzer import build_feature_coverage_profile

def test_build_feature_coverage_profile():
    df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02"],
        "returns_1d": [0.01, None],
        "volatility_14d": [0.02, 0.03]
    })

    prof = build_feature_coverage_profile("AAPL", df, ["returns_1d", "volatility_14d"])
    assert prof.average_coverage_ratio == 0.75
    assert "returns_1d" in prof.low_coverage_features
