from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.paper_shadow.shadow_safety_guard import assert_shadow_session_safe, ShadowSafetyError

def validate_shadow_session_safety(session: ShadowRehearsalSession) -> list[str]:
    errors = []
    try:
        assert_shadow_session_safe(session.context, session.order_intents, session.fills)
    except ShadowSafetyError as e:
        errors.append(str(e))
    return errors

def validate_shadow_session_no_real_orders(session: ShadowRehearsalSession) -> list[str]:
    errors = []
    if session.context and session.context.allow_real_orders:
        errors.append("Context allows real orders.")
    for intent in session.order_intents:
        if intent.is_real_order:
             errors.append(f"Intent {intent.intent_id} is marked real.")
    for fill in session.fills:
        if fill.is_real_fill:
             errors.append(f"Fill {fill.fill_id} is marked real.")
    return errors

def validate_shadow_session_no_paper_mutation(session: ShadowRehearsalSession) -> list[str]:
    errors = []
    if session.context and session.context.allow_paper_state_mutation:
        errors.append("Context allows paper mutation.")
    return errors

def validate_shadow_session_no_real_telegram(session: ShadowRehearsalSession) -> list[str]:
    errors = []
    if session.context and session.context.allow_telegram_real_send:
        errors.append("Context allows real telegram send.")
    return errors

def validate_shadow_session_outputs(session: ShadowRehearsalSession) -> list[str]:
    errors = []
    if not session.output_paths:
         errors.append("Session has no output paths.")
    return errors

def shadow_validator_summary(session: ShadowRehearsalSession) -> dict[str, Any]:
    return {
        "safety_errors": len(validate_shadow_session_safety(session)),
        "real_order_errors": len(validate_shadow_session_no_real_orders(session)),
        "paper_mutation_errors": len(validate_shadow_session_no_paper_mutation(session)),
        "telegram_errors": len(validate_shadow_session_no_real_telegram(session)),
        "output_errors": len(validate_shadow_session_outputs(session))
    }

def shadow_validator_to_text(payload: dict[str, Any]) -> str:
    text = "Shadow Validator Summary\n"
    for k, v in payload.items():
        text += f"{k}: {v}\n"
    return text
