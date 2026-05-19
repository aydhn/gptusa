from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowOrderIntent,
    ShadowFill,
    ShadowSafetyFlag
)
from usa_signal_bot.core.exceptions import ShadowSafetyError

def collect_shadow_safety_flags_from_context(context: ShadowSimulationContext) -> list[ShadowSafetyFlag]:
    flags = []
    if context.allow_real_orders:
        flags.append(ShadowSafetyFlag.REAL_ORDER_RISK)
    if context.allow_broker_calls:
        flags.append(ShadowSafetyFlag.BROKER_FIELD_RISK)
    if context.allow_paper_state_mutation:
        flags.append(ShadowSafetyFlag.PAPER_STATE_MUTATION_RISK)
    if context.allow_telegram_real_send:
        flags.append(ShadowSafetyFlag.TELEGRAM_REAL_SEND_RISK)
    if context.allow_production_config_write:
        flags.append(ShadowSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK)
    return flags

def collect_shadow_safety_flags_from_intents(intents: list[ShadowOrderIntent]) -> list[ShadowSafetyFlag]:
    flags = []
    for intent in intents:
        if intent.is_real_order:
            if ShadowSafetyFlag.REAL_ORDER_RISK not in flags:
                flags.append(ShadowSafetyFlag.REAL_ORDER_RISK)
        if intent.broker_destination is not None:
             if ShadowSafetyFlag.BROKER_FIELD_RISK not in flags:
                flags.append(ShadowSafetyFlag.BROKER_FIELD_RISK)
    return flags

def collect_shadow_safety_flags_from_fills(fills: list[ShadowFill]) -> list[ShadowSafetyFlag]:
    flags = []
    for fill in fills:
        if fill.is_real_fill:
             if ShadowSafetyFlag.REAL_ORDER_RISK not in flags:
                flags.append(ShadowSafetyFlag.REAL_ORDER_RISK)
    return flags

def shadow_session_has_blocking_flags(flags: list[ShadowSafetyFlag]) -> bool:
    blocking = [
        ShadowSafetyFlag.REAL_ORDER_RISK,
        ShadowSafetyFlag.PAPER_STATE_MUTATION_RISK,
        ShadowSafetyFlag.TELEGRAM_REAL_SEND_RISK,
        ShadowSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ShadowSafetyFlag.BROKER_FIELD_RISK
    ]
    return any(f in blocking for f in flags)

def assert_shadow_session_safe(context: ShadowSimulationContext, intents: list[ShadowOrderIntent] | None = None, fills: list[ShadowFill] | None = None) -> None:
    flags = collect_shadow_safety_flags_from_context(context)
    if intents:
        flags.extend(collect_shadow_safety_flags_from_intents(intents))
    if fills:
         flags.extend(collect_shadow_safety_flags_from_fills(fills))

    if shadow_session_has_blocking_flags(flags):
        raise ShadowSafetyError(f"Shadow session blocked due to safety flags: {flags}")

def shadow_safety_summary(flags: list[ShadowSafetyFlag]) -> dict[str, Any]:
    return {
        "flag_count": len(flags),
        "has_blocking": shadow_session_has_blocking_flags(flags),
        "flags": [f.value for f in flags]
    }

def shadow_safety_guard_to_text(payload: dict[str, Any]) -> str:
    text = "Shadow Safety Guard Summary\n"
    text += f"Flags Detected: {payload.get('flag_count', 0)}\n"
    text += f"Blocking: {payload.get('has_blocking', False)}\n"
    if payload.get('flags'):
        text += "Flags: " + ", ".join(payload['flags']) + "\n"
    return text
