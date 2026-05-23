from typing import Any, Optional
from usa_signal_bot.core.enums import NoWriteTransitionRiskFlag
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionDossier,
    PaperSandboxBridgeEnvelope,
    PaperSandboxBridgeRoute
)
from usa_signal_bot.paper_no_write_transition.bridge_route_guard import collect_bridge_route_risk_flags

def collect_sandbox_bridge_safety_flags(
    dossier: Optional[NoWriteTransitionDossier] = None,
    envelope: Optional[PaperSandboxBridgeEnvelope] = None,
    routes: Optional[list[PaperSandboxBridgeRoute]] = None
) -> list[NoWriteTransitionRiskFlag]:
    flags = set()

    if envelope:
        if envelope.activation_allowed:
            flags.add(NoWriteTransitionRiskFlag.ACTIVATION_ALLOWED_RISK)
        if envelope.allows_active_paper:
            flags.add(NoWriteTransitionRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if envelope.allows_broker_execution:
            flags.add(NoWriteTransitionRiskFlag.BROKER_ORDER_RISK)
        if envelope.allows_paper_state_mutation:
            flags.add(NoWriteTransitionRiskFlag.PAPER_STATE_MUTATION_RISK)
        if envelope.allows_telegram_real_send:
            flags.add(NoWriteTransitionRiskFlag.TELEGRAM_REAL_SEND_RISK)

    if routes:
        flags.update(collect_bridge_route_risk_flags(routes))

    return list(flags)

def sandbox_bridge_has_blocking_flags(flags: list[NoWriteTransitionRiskFlag]) -> bool:
    return len(flags) > 0

def validate_sandbox_bridge_safety(
    dossier: Optional[NoWriteTransitionDossier] = None,
    envelope: Optional[PaperSandboxBridgeEnvelope] = None,
    routes: Optional[list[PaperSandboxBridgeRoute]] = None
) -> list[str]:
    flags = collect_sandbox_bridge_safety_flags(dossier, envelope, routes)
    return [f.value for f in flags]

def sandbox_bridge_safety_summary(flags: list[NoWriteTransitionRiskFlag]) -> dict[str, Any]:
    return {
        "is_safe": not sandbox_bridge_has_blocking_flags(flags),
        "flags": [f.value for f in flags]
    }

def sandbox_bridge_safety_validator_to_text(payload: dict[str, Any]) -> str:
    return f"Sandbox Bridge Safety: Safe={payload.get('is_safe')} Flags={payload.get('flags')}"
