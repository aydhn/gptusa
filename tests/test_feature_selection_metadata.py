import pytest
import pandas as pd
from usa_signal_bot.core.enums import FeatureSelectionStatus
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import build_default_feature_group_definitions
from usa_signal_bot.feature_engine.factor_composition.feature_coverage_analyzer import build_feature_coverage_profile
from usa_signal_bot.feature_engine.factor_composition.feature_stability_analyzer import build_feature_stability_profile
from usa_signal_bot.feature_engine.factor_composition.feature_redundancy_analyzer import build_feature_redundancy_profile
from usa_signal_bot.feature_engine.factor_composition.feature_selection_metadata import build_feature_selection_metadata_for_symbol

def test_build_feature_selection_metadata():
    df = pd.DataFrame({
        "symbol": ["AAPL"] * 10,
        "timestamp": [f"2023-01-{i:02d}" for i in range(1, 11)],
        "returns_1d": [0.01, 0.02, -0.01, 0.05, 0.0, 0.01, -0.02, 0.03, 0.01, 0.0],
        "volatility_14d": [0.02] * 10
    })

    groups = build_default_feature_group_definitions(["returns_1d", "volatility_14d"])
    cov = build_feature_coverage_profile("AAPL", df)
    stab = build_feature_stability_profile("AAPL", df)
    red = build_feature_redundancy_profile("AAPL", df)

    meta = build_feature_selection_metadata_for_symbol("AAPL", df, groups, cov, stab, red)

    ret_meta = next(m for m in meta if m.feature_column == "returns_1d")
    assert ret_meta.selection_status == FeatureSelectionStatus.SELECTED_FOR_RESEARCH

    vol_meta = next(m for m in meta if m.feature_column == "volatility_14d")
    assert vol_meta.selection_status == FeatureSelectionStatus.EXCLUDED_LOW_STABILITY
