from typing import Any, List
from ..core.enums import ExperimentScope, ExperimentType

def build_default_validation_plan(scope: ExperimentScope, experiment_type: ExperimentType) -> dict[str, Any]:
    return {
        "baseline_period": "YTD",
        "candidate_period": "YTD",
        "requires_oos": True,
        "requires_manual_review": True,
        "leakage_guard_enabled": True
    }

def build_walk_forward_validation_plan(min_windows: int = 3, require_oos: bool = True) -> dict[str, Any]:
    return {
        "type": "WALK_FORWARD",
        "min_windows": min_windows,
        "require_oos": require_oos,
        "requires_manual_review": True
    }

def build_holdout_validation_plan(holdout_pct: float = 20.0) -> dict[str, Any]:
    return {
        "type": "HOLDOUT",
        "holdout_pct": holdout_pct,
        "requires_manual_review": True
    }

def build_cost_robustness_validation_plan() -> dict[str, Any]:
    return {
        "type": "COST_ROBUSTNESS",
        "requires_manual_review": True
    }

def build_regime_validation_plan() -> dict[str, Any]:
    return {
        "type": "REGIME",
        "requires_manual_review": True
    }

def validation_plan_warnings(plan: dict[str, Any]) -> List[str]:
    warnings = []
    if not plan.get("requires_manual_review", False):
        warnings.append("Plan is missing manual review requirement")
    if plan.get("type") == "HOLDOUT" and plan.get("holdout_pct", 0) <= 0:
        warnings.append("Holdout percentage is zero or invalid")
    return warnings

def validation_plan_to_text(plan: dict[str, Any]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in plan.items()])
