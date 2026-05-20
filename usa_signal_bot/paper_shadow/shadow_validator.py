from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def validate_shadow_session_safety(session: ShadowRehearsalSession) -> List[str]:
    errors = []
    errors.extend(validate_shadow_session_no_real_orders(session))
    errors.extend(validate_shadow_session_no_paper_mutation(session))
    errors.extend(validate_shadow_session_no_real_telegram(session))
    return errors

def validate_shadow_session_no_real_orders(session: ShadowRehearsalSession) -> List[str]:
    errors = []
    if session.context and session.context.allow_real_orders:
        errors.append("Session context allows real orders.")
    for intent in session.order_intents:
        if intent.is_real_order:
            errors.append(f"Intent {intent.intent_id} is a real order.")
    return errors

def validate_shadow_session_no_paper_mutation(session: ShadowRehearsalSession) -> List[str]:
    errors = []
    if session.context and session.context.allow_paper_state_mutation:
        errors.append("Session context allows paper state mutation.")
    for fill in session.fills:
        if fill.is_real_fill:
            errors.append(f"Fill {fill.fill_id} is a real fill.")
    return errors

def validate_shadow_session_no_real_telegram(session: ShadowRehearsalSession) -> List[str]:
    errors = []
    if session.context and session.context.allow_telegram_real_send:
        errors.append("Session context allows real telegram send.")
    return errors

def validate_shadow_session_outputs(session: ShadowRehearsalSession) -> List[str]:
    return []

def shadow_validator_summary(session: ShadowRehearsalSession) -> Dict[str, Any]:
    errors = validate_shadow_session_safety(session)
    return {"is_valid": len(errors) == 0, "error_count": len(errors)}

def shadow_validator_to_text(payload: Dict[str, Any]) -> str:
    return f"ShadowValidator(valid={payload['is_valid']}, err={payload['error_count']})"
