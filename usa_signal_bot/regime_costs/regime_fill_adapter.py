from typing import Dict, Any, Optional, List
from usa_signal_bot.regime_costs.regime_cost_models import RegimeAwareCostBreakdown, AdaptiveExecutionRealismDecision
from usa_signal_bot.core.enums import AdaptiveExecutionDecision

def adapt_fill_simulation_with_regime(fill_result: Dict[str, Any], regime_breakdown: RegimeAwareCostBreakdown) -> Dict[str, Any]:
    if not fill_allowed_by_regime_decision(regime_breakdown.adaptive_decision):
        fill_result["status"] = "BLOCKED_BY_REGIME"
        fill_result["metadata"] = fill_result.get("metadata", {})
        fill_result["metadata"]["regime_blocked"] = True
        return fill_result

    adj_bps = regime_breakdown.total_adjusted_cost_bps
    if adj_bps is not None and "reference_price" in fill_result and "side" in fill_result:
        new_price = regime_adjusted_fill_price(fill_result["reference_price"], fill_result["side"], adj_bps)
        if new_price is not None:
            fill_result["fill_price"] = new_price

    fill_result["metadata"] = fill_result.get("metadata", {})
    fill_result["metadata"]["regime_breakdown_id"] = regime_breakdown.breakdown_id

    return fill_result

def regime_adjusted_fill_price(reference_price: Optional[float], side: Any, adjusted_cost_bps: Optional[float]) -> Optional[float]:
    if reference_price is None or adjusted_cost_bps is None:
        return reference_price

    s = str(side).upper()
    factor = adjusted_cost_bps / 10000.0
    if s == "BUY":
        return reference_price * (1.0 + factor)
    elif s == "SELL":
        return reference_price * (1.0 - factor)
    return reference_price

def fill_allowed_by_regime_decision(decision: Optional[AdaptiveExecutionRealismDecision]) -> bool:
    if decision and decision.decision == AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION:
        return False
    return True

def regime_fill_warnings(regime_breakdown: RegimeAwareCostBreakdown) -> List[str]:
    w = []
    if not fill_allowed_by_regime_decision(regime_breakdown.adaptive_decision):
        w.append("Fill blocked by regime decision.")
    return w
