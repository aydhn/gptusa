from typing import Any, Dict, List
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    RebalancePlan, RebalanceAction, CurrentPortfolioState
)
from usa_signal_bot.core.enums import RebalanceStatus
from usa_signal_bot.portfolio_rebalance.portfolio_state import build_current_state_from_paper_payload

def build_current_state_from_paper_store_payload(payload: Dict[str, Any]) -> CurrentPortfolioState:
    return build_current_state_from_paper_payload(payload)

def attach_rebalance_plan_to_paper_state(paper_state: Dict[str, Any], plan: RebalancePlan) -> Dict[str, Any]:
    from usa_signal_bot.portfolio_rebalance.rebalance_models import rebalance_plan_to_dict
    paper_state["rebalance_metadata"] = rebalance_plan_to_dict(plan)
    return paper_state

def paper_rebalance_actions_as_local_intents(plan: RebalancePlan) -> List[Dict[str, Any]]:
    intents = []
    for action in plan.actions:
        if action.status == RebalanceStatus.PROPOSED:
            intents.append({
                "symbol": action.symbol,
                "action": action.action_type.value,
                "delta_notional_usd": action.delta_notional_usd,
                "estimated_cost_usd": action.estimated_cost_usd,
                "source": "REBALANCE_PLAN"
            })
    return intents

def paper_rebalance_allowed(action: RebalanceAction) -> bool:
    return action.status == RebalanceStatus.PROPOSED

def paper_rebalance_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "rebalance_metadata" not in payload:
        return {}
    meta = payload["rebalance_metadata"]
    return {
        "plan_id": meta.get("plan_id"),
        "status": meta.get("status"),
        "proposed_action_count": meta.get("proposed_action_count"),
        "total_delta_notional_usd": meta.get("total_delta_notional_usd")
    }
