import pytest
from usa_signal_bot.regime_costs.robustness_adapter import (
    cost_robustness_scenarios_from_regime_snapshot, regime_cost_robustness_warning
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.core.enums import CombinedCostRegime

def test_robustness_adapter():
    s = build_cost_regime_snapshot("SPY")
    s.combined_regime = CombinedCostRegime.HIGH_RISK

    scen = cost_robustness_scenarios_from_regime_snapshot(s)
    assert "EXTREME_STRESS_SCENARIO" in scen

    w = regime_cost_robustness_warning(s)
    assert len(w) == 1
