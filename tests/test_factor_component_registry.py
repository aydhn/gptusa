import pytest
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import build_default_feature_group_definitions
from usa_signal_bot.feature_engine.factor_composition.factor_component_registry import build_factor_components

def test_build_factor_components():
    groups = build_default_feature_group_definitions(["returns_1d", "volatility_14d"])
    comps = build_factor_components(groups)

    assert len(comps) >= 10
    vol_comp = next(c for c in comps if c.component_name == "volatility_component")
    assert "volatility_14d" in vol_comp.source_feature_columns
    assert vol_comp.produces_trade_signal is False
