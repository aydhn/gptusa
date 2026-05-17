from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceStatus

def cost_aware_rebalance_multiplier(cost_payload: Optional[Dict[str, Any]] = None, robustness_payload: Optional[Dict[str, Any]] = None) -> float:
    # A multiplier to scale thresholds. Not strictly needed if policy does it, but useful for heuristics
    return 1.0

def should_suppress_rebalance_for_cost(action: RebalanceAction, cost_payload: Optional[Dict[str, Any]] = None) -> bool:
    if action.action_type.value in ["EXIT", "DECREASE"]:
        return False # Generally don't block exits purely for cost unless extreme

    if cost_payload:
        status = cost_payload.get("status")
        robustness = cost_payload.get("cost_robustness_status")
        impact = cost_payload.get("market_impact_severity")

        if status in ["EXCESSIVE", "BLOCKED"]:
            return True

        if robustness == "FAILED":
            return True

        if impact in ["HIGH", "CRITICAL"]:
            return True

    # Using the bps we estimated in turnover cost
    if action.estimated_cost_bps and action.estimated_cost_bps > 300.0:
        return True

    return False

def apply_cost_aware_rebalance_filter(actions: List[RebalanceAction], cost_payloads_by_symbol: Optional[Dict[str, Dict[str, Any]]] = None) -> List[RebalanceAction]:
    cost_map = cost_payloads_by_symbol or {}

    for action in actions:
        if action.status != RebalanceStatus.PROPOSED:
            continue

        payload = cost_map.get(action.symbol)
        if should_suppress_rebalance_for_cost(action, payload):
            action.status = RebalanceStatus.SUPPRESSED_BY_COST
            action.warnings.append("Action suppressed due to high cost or market impact estimates.")

    return actions

def cost_aware_rebalance_warnings(actions: List[RebalanceAction]) -> List[str]:
    warnings = []
    suppressed = sum(1 for a in actions if a.status == RebalanceStatus.SUPPRESSED_BY_COST)
    if suppressed > 0:
        warnings.append(f"{suppressed} actions were suppressed due to high cost/impact estimates.")
    return warnings

def cost_aware_rebalance_to_text(payload: Dict[str, Any]) -> str:
    # Placeholder for reporting
    return "Cost Aware Rebalance Summary"
