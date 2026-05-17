from typing import Any, Dict, List
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalancePlan

def rebalance_risk_summary(plan: RebalancePlan) -> Dict[str, Any]:
    high_drift_count = sum(1 for d in plan.drift_measurements if d.severity.value in ["HIGH", "CRITICAL"])
    return {
        "status": plan.status.value,
        "high_drift_count": high_drift_count,
        "turnover_pct": plan.turnover_assessment.estimated_turnover_pct_equity if plan.turnover_assessment else 0.0,
        "turnover_status": plan.turnover_assessment.status.value if plan.turnover_assessment else "UNKNOWN",
        "suppressed_action_count": plan.suppressed_action_count,
        "blocked_action_count": plan.blocked_action_count
    }

def rebalance_risk_warnings(plan: RebalancePlan) -> List[str]:
    warnings = []
    if plan.turnover_assessment and plan.turnover_assessment.status.value in ["HIGH", "EXCESSIVE"]:
        warnings.append(f"Turnover level is {plan.turnover_assessment.status.value}.")
    if sum(1 for d in plan.drift_measurements if d.severity.value == "CRITICAL") > 0:
        warnings.append("Critical drifts detected.")
    if plan.blocked_action_count > 0:
         warnings.append(f"{plan.blocked_action_count} actions were blocked.")
    return warnings

def attach_rebalance_to_risk_report(report: Dict[str, Any], plan: RebalancePlan) -> Dict[str, Any]:
    from usa_signal_bot.portfolio_rebalance.rebalance_models import rebalance_plan_to_dict
    report["rebalance_metadata"] = rebalance_plan_to_dict(plan)
    report["rebalance_risk_summary"] = rebalance_risk_summary(plan)
    report["rebalance_risk_warnings"] = rebalance_risk_warnings(plan)
    return report

def rebalance_risk_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = payload.get("rebalance_risk_summary", {})
    if not summary:
        return "No Rebalance Risk Data"
    return f"Rebalance Risk: Drift High {summary.get('high_drift_count', 0)} | Turnover {summary.get('turnover_pct', 0.0):.2f}%"
