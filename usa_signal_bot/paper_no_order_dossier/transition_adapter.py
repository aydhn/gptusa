from typing import Any
import json
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import NoOrderDossierFullReview

def no_order_evidence_from_transition(payload: dict[str, Any]) -> list[str]:
    evidence = []
    if payload.get("dossier_id"):
        evidence.append(payload["dossier_id"])
    return evidence

def transition_supports_no_order_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if payload.get("activation_allowed"):
        reasons.append("transition allows activation")
    if not payload.get("all_writes_blocked", True):
        reasons.append("transition does not block writes")
    return len(reasons) == 0, reasons

def attach_no_order_hint_to_transition_payload(payload: dict[str, Any], review: NoOrderDossierFullReview) -> dict[str, Any]:
    out = payload.copy()
    out["no_order_dossier_review_id"] = review.review_id
    dossier = review.dossiers[0] if review.dossiers else None
    if dossier:
        out["no_order_dossier_status"] = dossier.status.value
    return out

def transition_no_order_summary(payload: dict[str, Any]) -> dict[str, Any]:
    supports, reasons = transition_supports_no_order_dossier(payload)
    return {
        "supports_no_order_dossier": supports,
        "reasons": reasons,
        "evidence_refs": no_order_evidence_from_transition(payload)
    }

def transition_adapter_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(transition_no_order_summary(payload), indent=2)
