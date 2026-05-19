from typing import Any, Dict, List, Tuple
from usa_signal_bot.release_sandbox.sandbox_models import ReleaseSandboxReview

def sandbox_governance_checklist_from_review(governance_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [{"check": "sandbox_pass", "status": "PASS"}]

def governance_bundle_sandbox_allowed(governance_payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_sandbox_review_to_governance_payload(governance_payload: Dict[str, Any], sandbox_review: ReleaseSandboxReview) -> Dict[str, Any]:
    governance_payload["sandbox_review_id"] = sandbox_review.review_id
    return governance_payload

def governance_sandbox_summary(governance_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"governance_adapted": True}

def governance_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "Governance Adapter: OK"
