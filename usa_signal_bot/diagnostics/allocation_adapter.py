from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticReview, FailureModeAssessment

def allocation_failure_diagnostics(payload: Dict[str, Any]) -> List[FailureModeAssessment]:
    return []

def sizing_status_failure_diagnostics(payload: Dict[str, Any]) -> List[FailureModeAssessment]:
    return []

def attach_diagnostics_to_allocation_review(payload: Dict[str, Any], diagnostic_review: DiagnosticReview) -> Dict[str, Any]:
    if "metadata" not in payload:
        payload["metadata"] = {}
    payload["metadata"]["diagnostics"] = {"review_id": diagnostic_review.review_id}
    return payload

def allocation_diagnostics_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("metadata", {}).get("diagnostics", {})

def allocation_diagnostics_to_text(payload: Dict[str, Any]) -> str:
    return "Allocation Diagnostics Adapter: OK"
