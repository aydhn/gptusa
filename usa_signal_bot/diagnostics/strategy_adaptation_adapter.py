from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticReview, FailureModeAssessment
from usa_signal_bot.diagnostics.event_normalizer import normalize_diagnostic_events
from usa_signal_bot.core.enums import DiagnosticScope

def strategy_gate_failure_diagnostics(payload: Dict[str, Any]) -> List[FailureModeAssessment]:
    # Placeholder for extracting gate failures
    return []

def ensemble_conflict_diagnostics(payload: Dict[str, Any]) -> List[FailureModeAssessment]:
    return []

def attach_diagnostics_to_strategy_adaptation_review(payload: Dict[str, Any], diagnostic_review: DiagnosticReview) -> Dict[str, Any]:
    if "metadata" not in payload:
        payload["metadata"] = {}
    payload["metadata"]["diagnostics"] = {
        "review_id": diagnostic_review.review_id,
        "diagnostic_status": diagnostic_review.scorecard.diagnostic_status.value if diagnostic_review.scorecard else "UNKNOWN"
    }
    return payload

def strategy_adaptation_diagnostics_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("metadata", {}).get("diagnostics", {})

def strategy_adaptation_diagnostics_to_text(payload: Dict[str, Any]) -> str:
    diags = payload.get("metadata", {}).get("diagnostics", {})
    return f"Strategy Adaptation Diagnostics: Status {diags.get('diagnostic_status')}"
