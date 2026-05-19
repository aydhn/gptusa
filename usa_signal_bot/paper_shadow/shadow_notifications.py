from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def build_shadow_notification_preview(session: ShadowRehearsalSession) -> dict[str, Any]:
    msg = format_shadow_rehearsal_message(session)
    return {
        "message": msg,
        "is_safe": not validate_shadow_notification_safe(msg)
    }

def format_shadow_rehearsal_message(session: ShadowRehearsalSession) -> str:
    return f"Shadow Rehearsal {session.session_id} completed with status {session.status.value}."

def validate_shadow_notification_safe(payload: dict[str, Any] | str) -> list[str]:
    errors = []
    text = payload if isinstance(payload, str) else str(payload)
    text = text.lower()
    unsafe_terms = ["gönderildi", "kesin", "tavsiye", "garanti", "broker", "live order", "sent"]
    for term in unsafe_terms:
        if term in text:
            errors.append(f"Unsafe language detected: {term}")
    return errors

def shadow_notification_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "message_length": len(payload.get("message", "")),
        "is_safe": payload.get("is_safe", False)
    }

def shadow_notification_to_text(payload: dict[str, Any]) -> str:
    summary = shadow_notification_summary(payload)
    text = "Shadow Notification Preview\n"
    text += f"Safe: {summary['is_safe']}\n"
    text += f"Content: {payload.get('message', '')}\n"
    text += "Note: This is a preview only. No real Telegram send will occur."
    return text
