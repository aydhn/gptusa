from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PaperSafeDossierFullReview

def paper_safe_dossier_evidence_from_no_order(payload: Dict[str, Any]) -> List[str]:
    return [payload.get("review_id")] if payload.get("review_id") else []

def no_order_supports_paper_safe_dossier(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if payload.get("report_type") != "NO_ORDER_DOSSIER_REPORT":
        return False, ["Not a no-order dossier report"]
    return True, []

def attach_paper_safe_dossier_hint_to_no_order_payload(payload: Dict[str, Any], review: PaperSafeDossierFullReview) -> Dict[str, Any]:
    payload["paper_safe_dossier_hint"] = review.review_id
    return payload

def no_order_paper_safe_dossier_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"hint": payload.get("paper_safe_dossier_hint")}

def no_order_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"No-Order Adapter Hint: {payload.get('paper_safe_dossier_hint')}"
