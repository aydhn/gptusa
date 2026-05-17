from typing import Any, List, Optional
from .workflow_models import ExperimentPlan, ParameterChangeProposal

def build_default_rollback_plan(experiment_plan: Optional[ExperimentPlan] = None) -> dict[str, Any]:
    return {
        "baseline_config_ref": "current_main",
        "changed_parameters": [],
        "revert_steps": ["Checkout baseline_config_ref"],
        "artifacts_to_preserve": ["experiment_report.json"],
        "requires_manual_review": True
    }

def rollback_plan_for_parameter_change(proposals: List[ParameterChangeProposal]) -> dict[str, Any]:
    plan = build_default_rollback_plan()
    plan["changed_parameters"] = [p.parameter_name for p in proposals]
    plan["revert_steps"] = [f"Revert {p.parameter_name} to {p.baseline_value}" for p in proposals]
    return plan

def rollback_plan_for_filter_change(experiment_plan: ExperimentPlan) -> dict[str, Any]:
    plan = build_default_rollback_plan(experiment_plan)
    plan["revert_steps"].append("Revert filter configuration")
    return plan

def rollback_plan_warnings(plan: dict[str, Any]) -> List[str]:
    warnings = []
    if not plan.get("requires_manual_review", False):
        warnings.append("Rollback plan is missing manual review requirement")
    if not plan.get("baseline_config_ref"):
        warnings.append("Rollback plan is missing baseline_config_ref")
    return warnings

def rollback_plan_to_text(plan: dict[str, Any]) -> str:
    lines = ["Rollback Plan:"]
    for k, v in plan.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
