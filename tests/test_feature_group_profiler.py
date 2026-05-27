import pytest
import pandas as pd
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import build_default_feature_group_definitions
from usa_signal_bot.feature_engine.factor_composition.feature_group_profiler import profile_feature_groups

def test_profile_feature_groups():
    df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02"],
        "returns_1d": [0.01, None],
        "volatility_14d": [0.02, 0.03]
    })
    groups = build_default_feature_group_definitions(["returns_1d", "volatility_14d"])
    profiles = profile_feature_groups(df, groups)

    ret_prof = next(p for p in profiles if p.group_name == "returns")
    # 1 null out of 2 = 0.5 missingness
    assert ret_prof.average_missingness == 0.5
    assert ret_prof.coverage_ratio == 0.5

    vol_prof = next(p for p in profiles if p.group_name == "volatility")
    assert vol_prof.average_missingness == 0.0
    assert vol_prof.coverage_ratio == 1.0
