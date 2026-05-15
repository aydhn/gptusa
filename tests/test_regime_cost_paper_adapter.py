import pytest
from usa_signal_bot.regime_costs.paper_adapter import (
    attach_regime_costs_to_paper_order, attach_regime_costs_to_paper_fill,
    paper_regime_cost_summary
)
from usa_signal_bot.regime_costs.regime_cost_models import RegimeAwareCostBreakdown, AdaptiveExecutionRealismDecision, get_utc_now_str
from usa_signal_bot.core.enums import AdaptiveExecutionDecision, CombinedCostRegime, RegimeCostAdjustmentStatus, RegimeCostCurveProfile

def test_paper_adapter():
    dec = AdaptiveExecutionRealismDecision("id", "SPY", get_utc_now_str(), AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION, RegimeCostAdjustmentStatus.APPLIED, CombinedCostRegime.BLOCKED, RegimeCostCurveProfile.BLOCKED, [], [], [], [])
    brk = RegimeAwareCostBreakdown("id", "SPY", get_utc_now_str(), None, None, None, None, dec, 10.0, 20.0, 10.0, RegimeCostAdjustmentStatus.APPLIED, [], [])

    fill = attach_regime_costs_to_paper_fill({}, brk)
    assert fill["status"] == "BLOCKED_BY_REGIME"

    order = attach_regime_costs_to_paper_order({}, regime_breakdown=brk)
    assert order["metadata"]["estimated_adjusted_cost_bps"] == 20.0

    sum = paper_regime_cost_summary([fill])
    assert sum["blocked_by_regime"] == 1
