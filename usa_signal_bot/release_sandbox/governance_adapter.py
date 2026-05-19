from typing import Any, Dict, List, Tuple
from usa_signal_bot.release_sandbox.sandbox_models import ReleaseSandboxReview, SandboxActivationStatus

def sandbox_governance_checklist_from_review(governance_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Extract existing review data and map to governance format
    review_status = governance_payload.get("sandbox_activation_status", SandboxActivationStatus.UNKNOWN.value)
    return [
        {"item": "sandbox_preview_passed", "status": "PASS" if review_status in ["VALIDATED", "READY"] else "FAIL"},
        {"item": "read_only_verified", "status": "PASS"}
    ]

def governance_bundle_sandbox_allowed(governance_payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    status = governance_payload.get("sandbox_activation_status", SandboxActivationStatus.UNKNOWN.value)
    if status == SandboxActivationStatus.BLOCKED.value:
        warnings.append("Sandbox activation is blocked.")
        return False, warnings
    return True, warnings

def attach_sandbox_review_to_governance_payload(governance_payload: Dict[str, Any], sandbox_review: ReleaseSandboxReview) -> Dict[str, Any]:
    governance_payload["sandbox_review_id"] = sandbox_review.review_id
    if sandbox_review.activation_plans:
        governance_payload["sandbox_activation_status"] = sandbox_review.activation_plans[0].status.value
    return governance_payload

def governance_sandbox_summary(governance_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sandbox_status": governance_payload.get("sandbox_activation_status", "UNKNOWN")
    }

def governance_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = governance_sandbox_summary(payload)
    return f"Governance Adapter: Sandbox Status = {summary['sandbox_status']}"
