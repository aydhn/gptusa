import pytest
from usa_signal_bot.core.enums import CombinedCostRegime, RegimeCostCurveProfile
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.regime_costs.cost_curve_selector import (
    select_cost_curve_profile, select_slippage_curve_for_regime,
    curve_profile_to_default_multiplier, cost_curve_selection_to_text
)

def test_select_cost_curve_profile():
    s = build_cost_regime_snapshot("SPY") # defaults to NORMAL
    s.combined_regime = CombinedCostRegime.NORMAL
    assert select_cost_curve_profile(s) == RegimeCostCurveProfile.BASELINE

    s.combined_regime = CombinedCostRegime.HIGH_RISK
    assert select_cost_curve_profile(s) == RegimeCostCurveProfile.EXTREME

    s.combined_regime = CombinedCostRegime.BLOCKED
    assert select_cost_curve_profile(s) == RegimeCostCurveProfile.BLOCKED

    s.combined_regime = CombinedCostRegime.STRESSED
    assert select_cost_curve_profile(s) == RegimeCostCurveProfile.STRESSED

def test_select_slippage_curve_for_regime():
    s = build_cost_regime_snapshot("SPY")
    s.combined_regime = CombinedCostRegime.NORMAL
    sel = select_slippage_curve_for_regime("SPY", s)
    assert sel.profile == RegimeCostCurveProfile.BASELINE
    assert sel.selected_curve_id is not None

def test_curve_profile_to_default_multiplier():
    assert curve_profile_to_default_multiplier(RegimeCostCurveProfile.BASELINE) == 1.0
    assert curve_profile_to_default_multiplier(RegimeCostCurveProfile.EXTREME) == 4.0

def test_text():
    s = build_cost_regime_snapshot("SPY")
    sel = select_slippage_curve_for_regime("SPY", s)
    assert "CONSERVATIVE" in cost_curve_selection_to_text(sel)
