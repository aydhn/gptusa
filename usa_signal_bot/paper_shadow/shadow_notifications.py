from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def build_shadow_notification_preview(session: ShadowRehearsalSession) -> Dict[str, Any]:
    return {
        "message": format_shadow_rehearsal_message(session),
        "is_real_send": False,
        "warnings": ["Telegram real send disabled for shadow notifications."]
    }

def format_shadow_rehearsal_message(session: ShadowRehearsalSession) -> str:
    return f"Shadow Session {session.session_id} completed. No real orders sent."

def validate_shadow_notification_safe(payload: Dict[str, Any] | str) -> List[str]:
    errors = []
    if isinstance(payload, dict) and payload.get("is_real_send"):
        errors.append("Shadow notification payload must not have is_real_send=True.")
    return errors

def shadow_notification_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"message_length": len(payload.get("message", ""))}

def shadow_notification_to_text(payload: Dict[str, Any]) -> str:
    return f"ShadowNotificationPreview(msg='{payload.get('message', '')}')"
