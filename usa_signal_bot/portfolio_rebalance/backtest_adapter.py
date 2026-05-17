from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceReview

def attach_rebalance_to_backtest_result(result: Dict[str, Any], review: Optional[RebalanceReview] = None) -> Dict[str, Any]:
    if review:
        from usa_signal_bot.portfolio_rebalance.rebalance_models import rebalance_review_to_dict
        result["rebalance_metadata"] = rebalance_review_to_dict(review)
    return result

def simulate_rebalance_metadata_for_backtest_window(window_payload: Dict[str, Any]) -> Dict[str, Any]:
    window_payload["rebalance_simulation_available"] = True
    return window_payload

def backtest_rebalance_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    if "rebalance_metadata" not in result:
        return {}
    meta = result["rebalance_metadata"]
    plan = meta.get("plan", {})
    return {
        "report_type": meta.get("report_type"),
        "plan_status": plan.get("status"),
        "proposed_action_count": plan.get("proposed_action_count")
    }

def backtest_turnover_warnings(result: Dict[str, Any]) -> List[str]:
    warnings = []
    if "rebalance_metadata" in result:
        meta = result["rebalance_metadata"]
        plan = meta.get("plan", {})
        ta = plan.get("turnover_assessment", {})
        if ta.get("status") in ["HIGH", "EXCESSIVE"]:
            warnings.append(f"Backtest period experienced {ta.get('status')} turnover.")
    return warnings
