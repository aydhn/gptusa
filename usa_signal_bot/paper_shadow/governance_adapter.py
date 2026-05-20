from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def governance_shadow_allowed(governance_payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def shadow_rehearsal_governance_checklist(session: ShadowRehearsalSession) -> List[Dict[str, Any]]:
    # Handle string or Enum for status
    status_str = session.status.value if hasattr(session.status, 'value') else session.status
    return [
        {"item": "Shadow rehearsal completed", "passed": status_str == "COMPLETED"},
        {"item": "No safety flags", "passed": len(session.safety_flags) == 0}
    ]

def attach_shadow_rehearsal_to_governance_payload(governance_payload: Dict[str, Any], session: ShadowRehearsalSession) -> Dict[str, Any]:
    status_str = session.status.value if hasattr(session.status, 'value') else session.status
    governance_payload["shadow_rehearsal_metadata"] = {
        "session_id": session.session_id,
        "status": status_str,
        "checklist": shadow_rehearsal_governance_checklist(session)
    }
    return governance_payload

def governance_shadow_summary(governance_payload: Dict[str, Any]) -> Dict[str, Any]:
    return governance_payload.get("shadow_rehearsal_metadata", {})

def governance_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"GovernanceShadowMetadata({payload})"
