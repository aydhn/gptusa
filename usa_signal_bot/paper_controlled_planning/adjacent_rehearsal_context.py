from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    PaperAdjacentRehearsalContext,
    ControlledPlanningTicket,
    create_paper_adjacent_context_id,
    _now_str
)
from usa_signal_bot.core.enums import PaperAdjacentRehearsalMode
from usa_signal_bot.paper_controlled_planning.paper_snapshot_comparator import build_read_only_paper_snapshot_for_planning

def build_paper_adjacent_rehearsal_context(
    ticket: ControlledPlanningTicket,
    paper_snapshot: Optional[dict[str, Any]] = None,
    mode: PaperAdjacentRehearsalMode = PaperAdjacentRehearsalMode.FULL_GUARDED_REHEARSAL
) -> PaperAdjacentRehearsalContext:
    snapshot = build_read_only_paper_snapshot_for_planning(paper_snapshot)
    return PaperAdjacentRehearsalContext(
        context_id=create_paper_adjacent_context_id(),
        created_at_utc=_now_str(),
        candidate_id=ticket.candidate_id,
        planning_ticket_id=ticket.ticket_id,
        mode=mode,
        read_only_paper_snapshot=snapshot,
        candidate_metadata=ticket.metadata.copy(),
        output_path=None,
        allow_active_paper=False,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_config_patch=False,
        warnings=[],
        errors=[]
    )

def build_mock_paper_adjacent_rehearsal_context() -> PaperAdjacentRehearsalContext:
    snapshot = build_read_only_paper_snapshot_for_planning(None)
    return PaperAdjacentRehearsalContext(
        context_id=create_paper_adjacent_context_id("mock_context"),
        created_at_utc=_now_str(),
        candidate_id="mock-candidate-123",
        planning_ticket_id="mock-ticket-123",
        mode=PaperAdjacentRehearsalMode.FULL_GUARDED_REHEARSAL,
        read_only_paper_snapshot=snapshot,
        candidate_metadata={},
        output_path=None,
        allow_active_paper=False,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_config_patch=False,
        warnings=[],
        errors=[]
    )

def validate_adjacent_context_safety(context: PaperAdjacentRehearsalContext) -> List[str]:
    errors = []
    if context.allow_active_paper: errors.append("Context allow_active_paper is True")
    if context.allow_paper_state_mutation: errors.append("Context allow_paper_state_mutation is True")
    if context.allow_paper_orders: errors.append("Context allow_paper_orders is True")
    if context.allow_broker_orders: errors.append("Context allow_broker_orders is True")
    if context.allow_telegram_real_send: errors.append("Context allow_telegram_real_send is True")
    if context.allow_config_patch: errors.append("Context allow_config_patch is True")
    return errors

def adjacent_context_summary(context: PaperAdjacentRehearsalContext) -> dict[str, Any]:
    return {
        "context_id": context.context_id,
        "mode": context.mode.value,
        "candidate_id": context.candidate_id
    }

def adjacent_context_to_text(context: PaperAdjacentRehearsalContext) -> str:
    lines = [
        "🛡️ PAPER-ADJACENT REHEARSAL CONTEXT",
        f"Context ID: {context.context_id}",
        f"Mode: {context.mode.value}",
        f"Ticket ID: {context.planning_ticket_id or 'Unknown'}"
    ]
    errs = validate_adjacent_context_safety(context)
    if errs:
        lines.append("SAFETY ERRORS:")
        for e in errs:
            lines.append(f" - {e}")
    lines.append("LIMITATION: This context forces read-only snapshot and disables active paper enable.")
    return "\n".join(lines)
