import pytest
from usa_signal_bot.feature_engine.phase116_models import (
    FeatureFactorKickoffIngestionResult, IndicatorDefinition, FeatureDefinition,
    FactorDefinition, FeatureInputContract, FeatureOutputSchema, FeatureComputationRequest,
    FeatureComputationResult, FeatureRegistry, FeatureFoundationContext, FeatureFoundationFullReview
)
from usa_signal_bot.feature_engine.indicator_registry import build_default_indicator_definitions
from usa_signal_bot.feature_engine.feature_registry import build_default_feature_definitions
from usa_signal_bot.feature_engine.factor_registry import build_default_factor_definitions
from usa_signal_bot.feature_engine.feature_input_contract import build_feature_input_contract
from usa_signal_bot.feature_engine.feature_schema import build_feature_output_schema

def test_models_creation():
    inds = build_default_indicator_definitions()
    assert len(inds) > 0
    assert inds[0].produces_trade_signal is False

    feats = build_default_feature_definitions(inds)
    assert len(feats) > 0
    assert feats[0].produces_trade_signal is False

    facs = build_default_factor_definitions(feats)
    assert len(facs) > 0
    assert facs[0].produces_trade_signal is False

    contract = build_feature_input_contract()
    assert contract.network_allowed is False

    schema = build_feature_output_schema(feats, facs)
    assert schema.trade_signal_blocked is True
