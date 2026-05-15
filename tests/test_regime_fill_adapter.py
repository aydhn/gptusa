import pytest
from usa_signal_bot.regime_costs.regime_fill_adapter import (
    adapt_fill_simulation_with_regime, regime_adjusted_fill_price, fill_allowed_by_regime_decision
)
from usa_signal_bot.regime_costs.regime_cost_models import RegimeAwareCostBreakdown, AdaptiveExecutionRealismDecision
from usa_signal_bot.core.enums import AdaptiveExecutionDecision, CombinedCostRegime, RegimeCostAdjustmentStatus, RegimeCostCurveProfile
from usa_signal_bot.regime_costs.regime_cost_models import get_utc_now_str

def test_adapt_fill_simulation():
    dec = AdaptiveExecutionRealismDecision(
        "id", "SPY", get_utc_now_str(), AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION,
        RegimeCostAdjustmentStatus.APPLIED, CombinedCostRegime.BLOCKED, RegimeCostCurveProfile.BLOCKED,
        [], [], [], []
    )
    brk = RegimeAwareCostBreakdown(
        "id", "SPY", get_utc_now_str(), None, None, None, None, dec, 10.0, 20.0, 10.0,
        RegimeCostAdjustmentStatus.APPLIED, [], []
    )
    res = adapt_fill_simulation_with_regime({"reference_price": 100.0, "side": "BUY"}, brk)
    assert res["status"] == "BLOCKED_BY_REGIME"
    assert res["metadata"]["regime_blocked"] is True

def test_regime_adjusted_fill_price():
    assert regime_adjusted_fill_price(100.0, "BUY", 100.0) == 101.0  # 1% cost
    assert regime_adjusted_fill_price(100.0, "SELL", 100.0) == 99.0
