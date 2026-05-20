from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowAcceptanceGateType, ShadowAcceptanceStatus
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceGate, create_shadow_acceptance_gate_id

def detect_real_send_language(text: str) -> List[str]:
    bad = ["telegrama gönderildi", "sent to telegram", "real send", "canlıya al"]
    t = text.lower()
    return [b for b in bad if b in t]

def detect_order_advice_language(text: str) -> List[str]:
    bad = ["kesin al", "kesin sat", "garanti", "emir gönderildi", "sent to broker", "live approved"]
    t = text.lower()
    return [b for b in bad if b in t]

def review_shadow_notification_preview(session_payload: Dict[str, Any]) -> Dict[str, Any]:
    nots = session_payload.get("notifications", [])
    all_text = " ".join([str(n) for n in nots])
    rs = detect_real_send_language(all_text)
    oa = detect_order_advice_language(all_text)
    return {
        "real_send_violations": rs,
        "order_advice_violations": oa,
        "safe": len(rs) == 0 and len(oa) == 0
    }

def notification_safety_gate(session_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    rev = review_shadow_notification_preview(session_payload)
    status = ShadowAcceptanceStatus.PASS if rev["safe"] else ShadowAcceptanceStatus.FAIL
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NOTIFICATION_SAFE),
        gate_type=ShadowAcceptanceGateType.NOTIFICATION_SAFE,
        status=status,
        threshold=0,
        observed_value=len(rev["real_send_violations"]) + len(rev["order_advice_violations"]),
        description="Check for safe notification language",
        risk_flags=[], warnings=[], errors=[]
    )

def shadow_notification_review_to_text(payload: Dict[str, Any]) -> str:
    return f"Notification Safe: {payload.get('safe', False)}"
