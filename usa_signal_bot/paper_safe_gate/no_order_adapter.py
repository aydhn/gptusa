
from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import PaperSafeGateFullReview

def paper_safe_evidence_from_no_order(payload: Dict[str, Any]) -> List[str]:
    return []

def no_order_supports_paper_safe_gate(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_paper_safe_hint_to_no_order_payload(payload: Dict[str, Any], review: PaperSafeGateFullReview) -> Dict[str, Any]:
    payload["paper_safe_hint"] = review.review_id
    return payload

def no_order_paper_safe_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"no_order_attached": True}

def no_order_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "No Order Adapter Success"
