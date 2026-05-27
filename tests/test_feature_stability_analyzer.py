import pytest
import pandas as pd
from usa_signal_bot.feature_engine.factor_composition.feature_stability_analyzer import build_feature_stability_profile

def test_build_feature_stability_profile():
    # Need 10 rows to not be 0.0
    df = pd.DataFrame({
        "symbol": ["AAPL"] * 10,
        "timestamp": [f"2023-01-{i:02d}" for i in range(1, 11)],
        "returns_1d": [0.01, 0.02, -0.01, 0.05, 0.0, 0.01, -0.02, 0.03, 0.01, 0.0],
        "volatility_14d": [0.02] * 10 # very stable (constant)
    })

    prof = build_feature_stability_profile("AAPL", df, ["returns_1d", "volatility_14d"])
    assert "volatility_14d" in prof.low_stability_features
    assert "returns_1d" not in prof.low_stability_features
