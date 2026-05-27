import pytest
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import build_default_feature_group_definitions
from usa_signal_bot.feature_engine.factor_composition.factor_component_registry import build_factor_components
from usa_signal_bot.feature_engine.factor_composition.factor_candidate_registry import build_factor_candidate_definitions
from usa_signal_bot.feature_engine.factor_composition.feature_selection_metadata import FeatureSelectionMetadata
from usa_signal_bot.core.enums import FeatureSelectionStatus
from usa_signal_bot.feature_engine.factor_composition.factor_readiness_gate import build_factor_readiness_gate

def test_build_factor_readiness_gate():
    groups = build_default_feature_group_definitions(["returns_1d"])
    comps = build_factor_components(groups)
    cands = build_factor_candidate_definitions(comps)

    meta = [FeatureSelectionMetadata(
        selection_id="test",
        created_at_utc="test",
        symbol="AAPL",
        feature_column="returns_1d",
        group_name="returns",
        selection_status=FeatureSelectionStatus.SELECTED_FOR_RESEARCH
    )]

    gate = build_factor_readiness_gate(groups, cands, meta)
    assert gate.ready_for_phase121 is True
    assert gate.activation_allowed is False
