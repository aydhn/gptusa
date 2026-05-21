from typing import Any, List, Optional
from usa_signal_bot.core.enums import ControlledPlanningSafetyFlag
from usa_signal_bot.paper_controlled_planning.planning_models import (
    PaperAdjacentRehearsalContext,
    PaperAdjacentProposal
)
from usa_signal_bot.core.exceptions import GuardedPaperAdjacentRehearsalError

def collect_rehearsal_safety_flags_from_context(context: PaperAdjacentRehearsalContext) -> List[ControlledPlanningSafetyFlag]:
    flags = []
    if context.allow_active_paper: flags.append(ControlledPlanningSafetyFlag.ACTIVE_PAPER_ENABLE_RISK)
    if context.allow_paper_state_mutation: flags.append(ControlledPlanningSafetyFlag.PAPER_STATE_MUTATION_RISK)
    if context.allow_paper_orders: flags.append(ControlledPlanningSafetyFlag.PAPER_ORDER_RISK)
    if context.allow_broker_orders: flags.append(ControlledPlanningSafetyFlag.BROKER_ORDER_RISK)
    if context.allow_telegram_real_send: flags.append(ControlledPlanningSafetyFlag.TELEGRAM_REAL_SEND_RISK)
    if context.allow_config_patch: flags.append(ControlledPlanningSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK)
    return flags

def collect_rehearsal_safety_flags_from_proposals(proposals: List[PaperAdjacentProposal]) -> List[ControlledPlanningSafetyFlag]:
    flags = []
    for p in proposals:
        if p.is_real_order:
            if ControlledPlanningSafetyFlag.REAL_ORDER_RISK not in flags:
                flags.append(ControlledPlanningSafetyFlag.REAL_ORDER_RISK)
        if p.will_mutate_paper_state:
            if ControlledPlanningSafetyFlag.PAPER_STATE_MUTATION_RISK not in flags:
                flags.append(ControlledPlanningSafetyFlag.PAPER_STATE_MUTATION_RISK)
        if p.will_send_to_broker:
            if ControlledPlanningSafetyFlag.BROKER_ORDER_RISK not in flags:
                flags.append(ControlledPlanningSafetyFlag.BROKER_ORDER_RISK)
    return flags

def rehearsal_has_blocking_flags(flags: List[ControlledPlanningSafetyFlag]) -> bool:
    blocking_flags = [
        ControlledPlanningSafetyFlag.REAL_ORDER_RISK,
        ControlledPlanningSafetyFlag.PAPER_ORDER_RISK,
        ControlledPlanningSafetyFlag.BROKER_ORDER_RISK,
        ControlledPlanningSafetyFlag.PAPER_STATE_MUTATION_RISK,
        ControlledPlanningSafetyFlag.TELEGRAM_REAL_SEND_RISK,
        ControlledPlanningSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ControlledPlanningSafetyFlag.ACTIVE_PAPER_ENABLE_RISK
    ]
    return any(f in flags for f in blocking_flags)

def assert_rehearsal_safe(context: PaperAdjacentRehearsalContext, proposals: Optional[List[PaperAdjacentProposal]] = None) -> None:
    ctx_flags = collect_rehearsal_safety_flags_from_context(context)
    if rehearsal_has_blocking_flags(ctx_flags):
        raise GuardedPaperAdjacentRehearsalError(f"Context has blocking safety flags: {[f.value for f in ctx_flags]}")

    if proposals:
        prop_flags = collect_rehearsal_safety_flags_from_proposals(proposals)
        if rehearsal_has_blocking_flags(prop_flags):
            raise GuardedPaperAdjacentRehearsalError(f"Proposals have blocking safety flags: {[f.value for f in prop_flags]}")

def rehearsal_safety_summary(flags: List[ControlledPlanningSafetyFlag]) -> dict[str, Any]:
    return {
        "flag_count": len(flags),
        "is_safe": not rehearsal_has_blocking_flags(flags),
        "flags": [f.value for f in flags]
    }

def rehearsal_safety_guard_to_text(payload: dict[str, Any]) -> str:
    lines = [
        "🚧 REHEARSAL SAFETY GUARD",
        f"Is Safe: {payload.get('is_safe', False)}"
    ]
    flags = payload.get("flags", [])
    if flags:
        lines.append("Flags:")
        for f in flags:
            lines.append(f" - {f}")
    return "\n".join(lines)
