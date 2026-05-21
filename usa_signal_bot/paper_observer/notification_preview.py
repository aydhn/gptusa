from datetime import datetime, timezone
from typing import Any, Dict, List, Union
from usa_signal_bot.core.enums import ObserverOutputType, ObserverSafetyFlag
from usa_signal_bot.paper_observer.observer_models import (
    ObserverRuntimeContext,
    ObserverOutput,
    create_observer_output_id
)

def format_observer_notification_message(context: ObserverRuntimeContext, outputs: List[ObserverOutput]) -> str:
    return f"[PREVIEW] Observer {context.candidate_id} generated {len(outputs)} outputs."

def build_observer_notification_preview(context: ObserverRuntimeContext, outputs: List[ObserverOutput]) -> ObserverOutput:
    msg = format_observer_notification_message(context, outputs)
    return ObserverOutput(
        output_id=create_observer_output_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        output_type=ObserverOutputType.NOTIFICATION_PREVIEW,
        symbol=None,
        status="PREVIEW_GENERATED",
        summary={"message_length": len(msg)},
        payload={"message": msg},
        is_real_order=False,
        mutates_paper_state=False,
        sends_to_broker=False,
        sends_telegram_real=False,
        safety_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def validate_observer_notification_safe(output: Union[ObserverOutput, str]) -> List[str]:
    errors = []
    if isinstance(output, ObserverOutput):
        if output.sends_telegram_real:
            errors.append("Notification must not send real Telegram message")
        msg = output.payload.get("message", "")
    else:
        msg = output

    unsafe_words = ["gönderildi", "kesin al", "garanti", "gerçek emir"]
    for w in unsafe_words:
        if w.lower() in msg.lower():
            errors.append(f"Notification contains unsafe word: {w}")
    return errors

def observer_notification_summary(output: ObserverOutput) -> Dict[str, Any]:
    return output.summary

def observer_notification_to_text(output: ObserverOutput) -> str:
    return output.payload.get("message", "No message")
