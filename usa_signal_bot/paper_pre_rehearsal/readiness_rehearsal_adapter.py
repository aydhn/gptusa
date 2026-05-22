from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import PrePaperDryRehearsalReview

def pre_paper_evidence_from_readiness_rehearsal(payload: Dict[str, Any]) -> List[str]:
    evidence = []
    if payload.get("sandbox_result") == "PASS":
        evidence.append("Release sandbox rehearsal passed")
    return evidence

def readiness_rehearsal_supports_pre_paper_rehearsal(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    if payload.get("sandbox_result") != "PASS":
        warnings.append("Sandbox result is not PASS")
        return False, warnings
    return True, warnings

def attach_pre_paper_hint_to_readiness_payload(payload: Dict[str, Any], review: PrePaperDryRehearsalReview) -> Dict[str, Any]:
    updated = payload.copy()
    updated["pre_paper_hint_review_id"] = review.review_id
    return updated

def readiness_rehearsal_pre_paper_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    supports, _ = readiness_rehearsal_supports_pre_paper_rehearsal(payload)
    return {
        "supports_pre_paper": supports,
        "has_hint": "pre_paper_hint_review_id" in payload
    }

def readiness_rehearsal_adapter_to_text(payload: Dict[str, Any]) -> str:
    s = readiness_rehearsal_pre_paper_summary(payload)
    return f"Readiness Adapter: Supports={s['supports_pre_paper']}, Has Hint={s['has_hint']}"
