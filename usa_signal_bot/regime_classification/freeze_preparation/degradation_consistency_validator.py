from typing import Any, Dict, List

ALLOWED_RECOMMENDED_ACTIONS = [
    "research_review",
    "data_quality_review",
    "documentation_review",
    "monitor_context",
    "baseline_refresh_review"
]

def validate_degradation_diagnostics_consistency(degradation_diagnostics: List[Dict[str, Any]], degradation_profiles: List[Dict[str, Any]]) -> List[str]:
    errors = []
    if len(degradation_diagnostics) == 0 and len(degradation_profiles) > 0:
        errors.append("Degradation profiles exist but diagnostics are empty")
    return errors

def validate_degradation_recommended_actions(degradation_diagnostics: List[Dict[str, Any]]) -> List[str]:
    errors = []
    for diag in degradation_diagnostics:
        action = diag.get("recommended_action_type")
        if action and action not in ALLOWED_RECOMMENDED_ACTIONS:
            errors.append(f"Forbidden recommended_action_type: {action}")
    return errors

def count_blocking_degradation(degradation_diagnostics: List[Dict[str, Any]]) -> int:
    return sum(1 for d in degradation_diagnostics if d.get("severity") == "blocked")

def count_degraded_contexts(degradation_diagnostics: List[Dict[str, Any]]) -> int:
    return len(degradation_diagnostics)

def degradation_consistency_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def degradation_consistency_to_text(errors: List[str]) -> str:
    if not errors:
        return "Degradation Consistency Valid."
    return f"Degradation Consistency Failed with {len(errors)} errors:\n" + "\n".join(f"- {e}" for e in errors)
