from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import CurrentPortfolioState, RebalanceAction, RebalancePlan

def current_state_from_allocation_payloads(payloads: List[Dict[str, Any]], total_equity_usd: Optional[float] = None) -> CurrentPortfolioState:
    from usa_signal_bot.portfolio_rebalance.portfolio_state import build_current_state_from_positions
    # Assuming allocation payloads have structure compatible with positions or can be adapted
    positions = []
    for p in payloads:
        # Map allocation result to portfolio position
        pos = {
            "symbol": p.get("symbol", ""),
            "market_value_usd": p.get("final_size_usd", 0.0),
            "side": p.get("side", "LONG"),
            "strategy_name": p.get("strategy_name")
        }
        positions.append(pos)

    return build_current_state_from_positions(positions, total_equity_usd)

def rebalance_actions_to_allocation_adjustments(actions: List[RebalanceAction]) -> List[Dict[str, Any]]:
    adjustments = []
    for action in actions:
        adjustments.append({
            "symbol": action.symbol,
            "action_type": action.action_type.value,
            "delta_notional_usd": action.delta_notional_usd,
            "status": action.status.value,
            "throttle_reasons": [r.value for r in action.throttle_reasons]
        })
    return adjustments

def attach_rebalance_to_allocation_review(allocation_review_payload: Dict[str, Any], rebalance_plan: RebalancePlan) -> Dict[str, Any]:
    from usa_signal_bot.portfolio_rebalance.rebalance_models import rebalance_plan_to_dict
    allocation_review_payload["rebalance_metadata"] = rebalance_plan_to_dict(rebalance_plan)
    return allocation_review_payload

def allocation_rebalance_adapter_to_text(payload: Dict[str, Any]) -> str:
    if "rebalance_metadata" not in payload:
        return "No Rebalance Adjustments in Allocation Review"
    meta = payload["rebalance_metadata"]
    return f"Allocation Review Rebalance Plan: Status {meta.get('status')} | Actions {meta.get('proposed_action_count')}"
