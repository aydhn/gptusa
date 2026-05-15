import pytest
from usa_signal_bot.regime_costs.regime_cost_breakdown import (
    build_regime_aware_cost_breakdown, apply_regime_multiplier_to_cost_breakdown, calculate_regime_cost_delta_bps, regime_aware_cost_breakdown_to_text
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.regime_costs.cost_curve_selector import select_slippage_curve_for_regime

def test_build_regime_aware_cost_breakdown():
    base = {"total_cost_bps": 10.0, "slippage_bps": 5.0}
    s = build_cost_regime_snapshot("SPY")
    sel = select_slippage_curve_for_regime("SPY", s)
    sel.multiplier.combined_multiplier = 2.0

    brk = build_regime_aware_cost_breakdown("SPY", base, s, sel)
    assert brk.total_adjusted_cost_bps == 10.0  # (5.0 * 2.0)
    assert brk.adjustment_delta_bps == 0.0

def test_apply_regime_multiplier():
    class DummyMult:
        combined_multiplier = 3.0
        max_cost_bps = 50.0
    base = {"total_cost_bps": 15.0, "slippage_bps": 5.0, "spread_cost_bps": 10.0}
    adj = apply_regime_multiplier_to_cost_breakdown(base, DummyMult())
    assert adj["slippage_bps"] == 15.0
    assert adj["spread_cost_bps"] == 30.0
    assert adj["total_cost_bps"] == 45.0

def test_calculate_delta():
    assert calculate_regime_cost_delta_bps(10.0, 15.0) == 5.0
    assert calculate_regime_cost_delta_bps(10.0, None) is None
