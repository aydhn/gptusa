import pytest
from usa_signal_bot.core.enums import StrategyFamily, StrategyRegimeCompatibility, StrategyGateDecision, StrategyConflictType, StrategyEnsembleDecision, AdaptiveWeightStatus, StrategyAdaptationRisk
from usa_signal_bot.strategy_adaptation.adaptation_models import (
    StrategyRegimeProfile, StrategyCompatibilityScore, StrategyGateResult,
    StrategyConflictResult, StrategyEnsembleMember, StrategyEnsembleResult,
    StrategyAdaptationReview, validate_strategy_regime_profile,
    validate_strategy_compatibility_score, validate_strategy_gate_result,
    validate_strategy_ensemble_result, create_strategy_regime_profile_id
)
from usa_signal_bot.core.exceptions import StrategyAdaptationValidationError

def test_strategy_regime_profile_valid():
    prof = StrategyRegimeProfile(
        profile_id="p1", strategy_name="s1", strategy_family=StrategyFamily.TREND_FOLLOWING,
        preferred_trend_regimes=[], preferred_volatility_regimes=[], preferred_momentum_regimes=[],
        preferred_liquidity_regimes=[], preferred_cross_sectional_regimes=[],
        avoided_regimes=[], blocked_regimes=[], base_weight=1.0, min_required_confidence=50.0
    )
    validate_strategy_regime_profile(prof)

def test_negative_weight_validation_error():
    prof = StrategyRegimeProfile(
        profile_id="p1", strategy_name="s1", strategy_family=StrategyFamily.TREND_FOLLOWING,
        preferred_trend_regimes=[], preferred_volatility_regimes=[], preferred_momentum_regimes=[],
        preferred_liquidity_regimes=[], preferred_cross_sectional_regimes=[],
        avoided_regimes=[], blocked_regimes=[], base_weight=-1.0, min_required_confidence=50.0
    )
    with pytest.raises(StrategyAdaptationValidationError):
        validate_strategy_regime_profile(prof)

def test_id_factory_works():
    id_val = create_strategy_regime_profile_id("test")
    assert id_val.startswith("prof_test_")
