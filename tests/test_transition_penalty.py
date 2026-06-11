import pytest
from typing import Any, Dict, List
from usa_signal_bot.core.enums import StrategyFamily
from usa_signal_bot.strategy_adaptation.adaptation_models import StrategyRegimeProfile
from usa_signal_bot.strategy_adaptation.transition_penalty import transition_penalty_for_strategy

def test_transition_penalty_for_strategy_no_signals():
    profile = StrategyRegimeProfile(
        profile_id="p_test",
        strategy_name="test_strat",
        strategy_family=StrategyFamily.TREND_FOLLOWING,
        preferred_trend_regimes=[],
        preferred_volatility_regimes=[],
        preferred_momentum_regimes=[],
        preferred_liquidity_regimes=[],
        preferred_cross_sectional_regimes=[],
        avoided_regimes=[],
        blocked_regimes=[],
        base_weight=1.0,
        min_required_confidence=50.0
    )

    result = transition_penalty_for_strategy(profile)
    assert result == 0.0

def test_transition_penalty_for_strategy_with_signals():
    profile = StrategyRegimeProfile(
        profile_id="p_test_2",
        strategy_name="test_strat_2",
        strategy_family=StrategyFamily.MEAN_REVERSION,
        preferred_trend_regimes=[],
        preferred_volatility_regimes=[],
        preferred_momentum_regimes=[],
        preferred_liquidity_regimes=[],
        preferred_cross_sectional_regimes=[],
        avoided_regimes=[],
        blocked_regimes=[],
        base_weight=1.0,
        min_required_confidence=50.0
    )

    signals: List[Dict[str, Any]] = [
        {"type": "regime_shift", "severity": 0.8},
        {"type": "volatility_spike", "severity": 0.5}
    ]

    result = transition_penalty_for_strategy(profile, transition_signals=signals)
    assert result == 0.0
