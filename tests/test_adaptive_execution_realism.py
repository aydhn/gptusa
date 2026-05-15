import pytest
from usa_signal_bot.core.enums import CombinedCostRegime, AdaptiveExecutionDecision
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.regime_costs.adaptive_execution_realism import AdaptiveExecutionRealismEngine

def test_adaptive_decision_engine():
    engine = AdaptiveExecutionRealismEngine()

    s_normal = build_cost_regime_snapshot("SPY")
    s_normal.combined_regime = CombinedCostRegime.NORMAL
    d1 = engine.decide("SPY", s_normal)
    assert d1.decision == AdaptiveExecutionDecision.USE_BASELINE_COSTS

    s_blocked = build_cost_regime_snapshot("SPY")
    s_blocked.combined_regime = CombinedCostRegime.BLOCKED
    d2 = engine.decide("SPY", s_blocked)
    assert d2.decision == AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION
    assert engine.should_block_fill_simulation(s_blocked)

    s_hr = build_cost_regime_snapshot("SPY")
    s_hr.combined_regime = CombinedCostRegime.HIGH_RISK
    d3 = engine.decide("SPY", s_hr)
    assert d3.decision == AdaptiveExecutionDecision.REQUIRE_REVIEW

    s_stress = build_cost_regime_snapshot("SPY")
    s_stress.combined_regime = CombinedCostRegime.STRESSED
    d4 = engine.decide("SPY", s_stress)
    assert d4.decision == AdaptiveExecutionDecision.USE_STRESSED_COSTS
