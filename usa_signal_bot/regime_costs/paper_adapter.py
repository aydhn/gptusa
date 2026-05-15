from typing import Dict, Any, Optional, List
from usa_signal_bot.regime_costs.regime_cost_models import CostRegimeSnapshot, RegimeAwareCostBreakdown
from usa_signal_bot.core.enums import AdaptiveExecutionDecision

def attach_regime_costs_to_paper_order(order: Dict[str, Any], snapshot: Optional[CostRegimeSnapshot] = None, regime_breakdown: Optional[RegimeAwareCostBreakdown] = None) -> Dict[str, Any]:
    order["metadata"] = order.get("metadata", {})
    if snapshot:
        order["metadata"]["cost_regime"] = snapshot.combined_regime.value
    if regime_breakdown:
        order["metadata"]["regime_cost_curve_profile"] = regime_breakdown.curve_selection.profile.value if regime_breakdown.curve_selection else "UNKNOWN"
        order["metadata"]["estimated_base_cost_bps"] = regime_breakdown.total_base_cost_bps
        order["metadata"]["estimated_adjusted_cost_bps"] = regime_breakdown.total_adjusted_cost_bps
    return order

def attach_regime_costs_to_paper_fill(fill: Dict[str, Any], regime_breakdown: Optional[RegimeAwareCostBreakdown] = None) -> Dict[str, Any]:
    fill["metadata"] = fill.get("metadata", {})
    if regime_breakdown:
        fill["metadata"]["applied_adjusted_cost_bps"] = regime_breakdown.total_adjusted_cost_bps
        if regime_breakdown.adaptive_decision and regime_breakdown.adaptive_decision.decision == AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION:
            fill["status"] = "BLOCKED_BY_REGIME"
    return fill

def paper_regime_cost_summary(orders_or_fills: List[Dict[str, Any]]) -> Dict[str, Any]:
    blocked = 0
    total = len(orders_or_fills)
    for i in orders_or_fills:
        if i.get("status") == "BLOCKED_BY_REGIME":
            blocked += 1

    return {
        "total_items": total,
        "blocked_by_regime": blocked
    }

def paper_regime_fill_allowed(regime_breakdown: Optional[RegimeAwareCostBreakdown]) -> bool:
    if regime_breakdown and regime_breakdown.adaptive_decision:
        if regime_breakdown.adaptive_decision.decision == AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION:
            return False
    return True
