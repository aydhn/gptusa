from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningTicket,
    PaperAdjacentRehearsalRun,
    FinalHumanApprovalQueueItem
)
from usa_signal_bot.core.enums import ControlledPlanningSafetyFlag

def collect_controlled_planning_safety_flags(
    ticket: ControlledPlanningTicket,
    run: Optional[PaperAdjacentRehearsalRun] = None,
    queue_item: Optional[FinalHumanApprovalQueueItem] = None
) -> List[ControlledPlanningSafetyFlag]:
    flags = list(ticket.safety_flags)
    if run:
        flags.extend(run.safety_flags)
    if queue_item:
        flags.extend(queue_item.safety_flags)
        if not queue_item.reviewer_notes:
            flags.append(ControlledPlanningSafetyFlag.MISSING_HUMAN_APPROVAL_NOTES)
    # Deduplicate
    return list(set(flags))

def validate_controlled_planning_safety(
    ticket: ControlledPlanningTicket,
    run: Optional[PaperAdjacentRehearsalRun] = None,
    queue_item: Optional[FinalHumanApprovalQueueItem] = None
) -> List[str]:
    errors = []
    if ticket.allowed_for_active_paper: errors.append("Ticket allowed_for_active_paper is True")
    if ticket.allowed_for_broker_execution: errors.append("Ticket allowed_for_broker_execution is True")

    if run and run.context:
        if run.context.allow_active_paper: errors.append("Rehearsal Context allow_active_paper is True")
        if run.context.allow_broker_orders: errors.append("Rehearsal Context allow_broker_orders is True")
        for p in run.proposals:
            if p.is_real_order: errors.append(f"Proposal {p.proposal_id} is_real_order is True")

    if queue_item:
        if queue_item.allows_active_paper: errors.append("Approval Item allows_active_paper is True")
        if queue_item.allows_broker_execution: errors.append("Approval Item allows_broker_execution is True")

    return errors

def planning_has_blocking_flags(flags: List[ControlledPlanningSafetyFlag]) -> bool:
    blocking_flags = [
        ControlledPlanningSafetyFlag.REAL_ORDER_RISK,
        ControlledPlanningSafetyFlag.PAPER_ORDER_RISK,
        ControlledPlanningSafetyFlag.BROKER_ORDER_RISK,
        ControlledPlanningSafetyFlag.PAPER_STATE_MUTATION_RISK,
        ControlledPlanningSafetyFlag.TELEGRAM_REAL_SEND_RISK,
        ControlledPlanningSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ControlledPlanningSafetyFlag.ACTIVE_PAPER_ENABLE_RISK,
        ControlledPlanningSafetyFlag.APPROVAL_AUTO_ENABLE_RISK,
        ControlledPlanningSafetyFlag.BLOCKED_EXIT_DECISION
    ]
    return any(f in flags for f in blocking_flags)

def planning_safety_summary(flags: List[ControlledPlanningSafetyFlag]) -> dict[str, Any]:
    return {
        "flag_count": len(flags),
        "has_blocking_flags": planning_has_blocking_flags(flags),
        "flags": [f.value for f in flags]
    }

def planning_safety_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [
        "🚧 PLANNING SAFETY VALIDATOR",
        f"Has Blocking Flags: {payload.get('has_blocking_flags', False)}"
    ]
    flags = payload.get("flags", [])
    if flags:
        lines.append("Flags:")
        for f in flags:
            lines.append(f" - {f}")
    return "\n".join(lines)
