import pytest
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import build_default_feature_group_definitions
from usa_signal_bot.feature_engine.factor_composition.factor_component_registry import build_factor_components
from usa_signal_bot.feature_engine.factor_composition.factor_candidate_registry import build_factor_candidate_definitions

def test_build_factor_candidate_definitions():
    groups = build_default_feature_group_definitions(["returns_1d", "volatility_14d"])
    comps = build_factor_components(groups)
    cands = build_factor_candidate_definitions(comps)

    assert len(cands) >= 10
    vol_cand = next(c for c in cands if c.factor_name == "volatility_research_factor")
    assert "volatility_14d" in vol_cand.input_feature_columns
    assert vol_cand.produces_trade_signal is False
