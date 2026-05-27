import pytest
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import (
    build_default_feature_group_definitions,
    infer_feature_group_kind
)
from usa_signal_bot.core.enums import FeatureGroupKind

def test_build_default_feature_group_definitions():
    groups = build_default_feature_group_definitions(["returns_1d", "volatility_14d"])
    assert len(groups) >= 13

    returns_group = next(g for g in groups if g.group_kind == FeatureGroupKind.RETURNS)
    assert "returns_1d" in returns_group.feature_columns

def test_infer_feature_group_kind():
    assert infer_feature_group_kind("log_return_5d") == FeatureGroupKind.RETURNS
    assert infer_feature_group_kind("rsi_14") == FeatureGroupKind.MOMENTUM
    assert infer_feature_group_kind("event_earnings_active") == FeatureGroupKind.EVENT_CONTEXT
