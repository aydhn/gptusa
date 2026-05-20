from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowOrderIntent, ShadowFill
)
from usa_signal_bot.core.enums import ShadowSafetyFlag
from usa_signal_bot.core.exceptions import ShadowSafetyError

def collect_shadow_safety_flags_from_context(context: ShadowSimulationContext) -> List[ShadowSafetyFlag]:
    flags = []
    if context.allow_real_orders:
        flags.append(ShadowSafetyFlag.REAL_ORDER_RISK)
    if context.allow_paper_state_mutation:
        flags.append(ShadowSafetyFlag.PAPER_STATE_MUTATION_RISK)
    if context.allow_telegram_real_send:
        flags.append(ShadowSafetyFlag.TELEGRAM_REAL_SEND_RISK)
    if context.allow_production_config_write:
        flags.append(ShadowSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK)
    return flags

def collect_shadow_safety_flags_from_intents(intents: List[ShadowOrderIntent]) -> List[ShadowSafetyFlag]:
    flags = []
    for intent in intents:
        if intent.is_real_order:
            flags.append(ShadowSafetyFlag.REAL_ORDER_RISK)
        if intent.broker_destination is not None:
            flags.append(ShadowSafetyFlag.BROKER_FIELD_RISK)
    return list(set(flags))

def collect_shadow_safety_flags_from_fills(fills: List[ShadowFill]) -> List[ShadowSafetyFlag]:
    flags = []
    for fill in fills:
        if fill.is_real_fill:
            flags.append(ShadowSafetyFlag.PAPER_STATE_MUTATION_RISK)
    return list(set(flags))

def shadow_session_has_blocking_flags(flags: List[ShadowSafetyFlag]) -> bool:
    return len(flags) > 0

def assert_shadow_session_safe(context: ShadowSimulationContext, intents: List[ShadowOrderIntent] | None = None, fills: List[ShadowFill] | None = None) -> None:
    flags = collect_shadow_safety_flags_from_context(context)
    if intents:
        flags.extend(collect_shadow_safety_flags_from_intents(intents))
    if fills:
        flags.extend(collect_shadow_safety_flags_from_fills(fills))

    if shadow_session_has_blocking_flags(flags):
        raise ShadowSafetyError(f"Shadow session blocked due to safety flags: {flags}")

def shadow_safety_summary(flags: List[ShadowSafetyFlag]) -> Dict[str, Any]:
    return {"flag_count": len(flags), "flags": [f.value for f in flags]}

def shadow_safety_guard_to_text(payload: Dict[str, Any]) -> str:
    return f"ShadowSafetyGuard(flags={payload['flag_count']})"
