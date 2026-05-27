import pytest
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import build_default_feature_group_definitions
from usa_signal_bot.feature_engine.factor_composition.factor_component_registry import build_factor_components
from usa_signal_bot.feature_engine.factor_composition.factor_candidate_registry import build_factor_candidate_definitions
from usa_signal_bot.feature_engine.factor_composition.factor_composition_specs import build_factor_composition_spec

def test_build_factor_composition_spec():
    groups = build_default_feature_group_definitions(["returns_1d", "volatility_14d"])
    comps = build_factor_components(groups)
    cands = build_factor_candidate_definitions(comps)

    spec = build_factor_composition_spec(groups, cands)
    assert len(spec.factor_candidates) == len(cands)
    assert len(spec.feature_groups) == len(groups)
    assert spec.produces_trade_signal is False
