import pytest
from usa_signal_bot.regime_costs.walk_forward_adapter import (
    attach_regime_costs_to_walk_forward_result, walk_forward_regime_shift_warnings,
    classify_walk_forward_regime_cost_stability
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.core.enums import CombinedCostRegime

def test_walk_forward_adapter():
    s = build_cost_regime_snapshot("SPY")
    s.combined_regime = CombinedCostRegime.HIGH_RISK
    res = attach_regime_costs_to_walk_forward_result({}, {"win1": [s]})

    assert "HIGH_RISK" in walk_forward_regime_shift_warnings(res)[0]
    assert classify_walk_forward_regime_cost_stability(res) == CombinedCostRegime.HIGH_RISK
