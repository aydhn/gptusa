from typing import Any, Dict, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import TargetPortfolioState, RebalancePlan

def rebalance_target_from_portfolio_construction_plan(plan_payload: Dict[str, Any], total_equity_usd: Optional[float] = None) -> TargetPortfolioState:
    from usa_signal_bot.portfolio_rebalance.target_extractor import build_target_state_from_construction_plan
    return build_target_state_from_construction_plan(plan_payload, total_equity_usd)

def attach_rebalance_feedback_to_construction_plan(plan_payload: Dict[str, Any], rebalance_plan: RebalancePlan) -> Dict[str, Any]:
    from usa_signal_bot.portfolio_rebalance.rebalance_models import rebalance_plan_to_dict
    plan_payload["rebalance_feedback"] = rebalance_plan_to_dict(rebalance_plan)
    return plan_payload

def construction_rebalance_summary(plan_payload: Dict[str, Any]) -> Dict[str, Any]:
    if "rebalance_feedback" not in plan_payload:
        return {}
    meta = plan_payload["rebalance_feedback"]
    return {
        "status": meta.get("status"),
        "proposed_action_count": meta.get("proposed_action_count"),
        "total_delta_notional_usd": meta.get("total_delta_notional_usd")
    }

def portfolio_construction_rebalance_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = construction_rebalance_summary(payload)
    if not summary:
        return "No Rebalance Feedback Available"
    return f"Rebalance Feedback: Status {summary.get('status')} | Actions {summary.get('proposed_action_count')}"
