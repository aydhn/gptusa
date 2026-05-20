from typing import Any, List
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunProposal
)

def build_dry_run_notification_preview(context: DryRunBridgeContext, proposals: List[DryRunProposal]) -> dict[str, Any]:
    message = format_dry_run_notification_message(context, proposals)
    return {
        "channel": "dry_run",
        "message": message,
        "is_real_send": False,
        "preview_only": True
    }

def format_dry_run_notification_message(context: DryRunBridgeContext, proposals: List[DryRunProposal]) -> str:
    lines = [
        "🧪 SUPERVISED DRY-RUN PREVIEW",
        f"Context: {context.context_id}",
        f"Mode: {context.mode.value}",
        f"Proposals Generated: {len(proposals)}",
        "",
        "⚠️ NOT INVESTMENT ADVICE. NO LIVE ORDERS GENERATED. NO PAPER STATE MUTATED."
    ]
    return "\n".join(lines)

def validate_dry_run_notification_preview_safe(payload: dict[str, Any] | str) -> List[str]:
    errors = []
    text = payload.get("message", "") if isinstance(payload, dict) else payload

    if isinstance(payload, dict) and payload.get("is_real_send", False):
        errors.append("Notification preview marked as real send.")

    unsafe_phrases = ["gönderildi", "kesin al", "kesin sat", "garanti", "real order", "live approved", "sent to broker", "paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr"]
    for phrase in unsafe_phrases:
        if phrase in text.lower():
            errors.append(f"Notification contains unsafe phrase: '{phrase}'")

    return errors

def dry_run_notification_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "is_real_send": payload.get("is_real_send", False),
        "preview_only": payload.get("preview_only", True),
        "message_length": len(payload.get("message", ""))
    }

def dry_run_notification_preview_to_text(payload: dict[str, Any]) -> str:
    return payload.get("message", "")
