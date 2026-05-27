import pytest
import pandas as pd
from usa_signal_bot.feature_engine.factor_composition.feature_redundancy_analyzer import build_feature_redundancy_profile

def test_build_feature_redundancy_profile():
    df = pd.DataFrame({
        "symbol": ["AAPL"] * 4,
        "timestamp": [f"2023-01-{i:02d}" for i in range(1, 5)],
        "feature_1": [1.0, 2.0, 3.0, 4.0],
        "feature_2": [1.01, 2.01, 3.02, 4.03], # Highly correlated
        "feature_3": [1.0, -1.0, 1.0, -1.0] # Not correlated
    })

    prof = build_feature_redundancy_profile("AAPL", df, ["feature_1", "feature_2", "feature_3"])
    assert prof.redundancy_score > 0
    assert len(prof.high_redundancy_pairs) == 1
    assert "feature_1" in prof.high_redundancy_pairs[0].values()
