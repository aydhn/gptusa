from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction

def estimate_action_turnover_cost(action: RebalanceAction, cost_payload: Optional[Dict[str, Any]] = None) -> RebalanceAction:
    if action.delta_notional_usd is None or action.delta_notional_usd == 0:
        return action

    abs_notional = abs(action.delta_notional_usd)

    # If we have a cost payload from Phase 55, use it
    if cost_payload and "adjusted_cost_bps" in cost_payload:
        bps = cost_payload["adjusted_cost_bps"]
    else:
        # Conservative fallback
        bps = 50.0

    cost_usd = abs_notional * (bps / 10000.0)

    action.estimated_cost_bps = bps
    action.estimated_cost_usd = cost_usd

    if bps > 150.0:
        action.warnings.append(f"High estimated transaction cost: {bps:.1f} bps")

    return action

def estimate_actions_turnover_cost(actions: List[RebalanceAction], cost_payloads_by_symbol: Optional[Dict[str, Dict[str, Any]]] = None) -> List[RebalanceAction]:
    cost_map = cost_payloads_by_symbol or {}
    return [estimate_action_turnover_cost(a, cost_map.get(a.symbol)) for a in actions]

def total_estimated_rebalance_cost_usd(actions: List[RebalanceAction]) -> float:
    return sum(a.estimated_cost_usd for a in actions if a.estimated_cost_usd is not None and a.status.value in ["PROPOSED", "NOT_NEEDED"])

def total_estimated_rebalance_cost_bps(actions: List[RebalanceAction]) -> Optional[float]:
    total_cost_usd = total_estimated_rebalance_cost_usd(actions)
    total_notional = sum(abs(a.delta_notional_usd) for a in actions if a.delta_notional_usd is not None and a.status.value in ["PROPOSED", "NOT_NEEDED"])

    if total_notional > 0:
        return (total_cost_usd / total_notional) * 10000.0
    return None

def turnover_cost_summary_to_text(actions: List[RebalanceAction]) -> str:
    total_usd = total_estimated_rebalance_cost_usd(actions)
    total_bps = total_estimated_rebalance_cost_bps(actions)

    bps_str = f"{total_bps:.1f} bps" if total_bps is not None else "N/A"
    return f"Total Estimated Rebalance Cost: ${total_usd:.2f} ({bps_str} avg on turnover)"
