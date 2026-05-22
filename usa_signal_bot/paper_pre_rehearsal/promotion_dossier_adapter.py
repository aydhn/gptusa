from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import PrePaperDryRehearsalReview

def pre_paper_evidence_from_promotion_dossier(payload: Dict[str, Any]) -> List[str]:
    evidence = []
    if payload.get("dossier_status") == "APPROVED_FOR_SANDBOX":
        evidence.append("Dossier approved for sandbox")
    return evidence

def promotion_dossier_supports_pre_paper_rehearsal(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    if payload.get("dossier_status") != "APPROVED_FOR_SANDBOX":
        warnings.append("Dossier is not APPROVED_FOR_SANDBOX")
        return False, warnings
    return True, warnings

def attach_pre_paper_hint_to_promotion_dossier_payload(payload: Dict[str, Any], review: PrePaperDryRehearsalReview) -> Dict[str, Any]:
    updated = payload.copy()
    updated["pre_paper_hint_review_id"] = review.review_id
    return updated

def promotion_dossier_pre_paper_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    supports, _ = promotion_dossier_supports_pre_paper_rehearsal(payload)
    return {
        "supports_pre_paper": supports,
        "has_hint": "pre_paper_hint_review_id" in payload
    }

def promotion_dossier_adapter_to_text(payload: Dict[str, Any]) -> str:
    s = promotion_dossier_pre_paper_summary(payload)
    return f"Promotion Adapter: Supports={s['supports_pre_paper']}, Has Hint={s['has_hint']}"
