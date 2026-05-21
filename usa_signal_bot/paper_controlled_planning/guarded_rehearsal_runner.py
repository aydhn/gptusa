from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    PaperAdjacentRehearsalContext,
    PaperAdjacentProposal,
    PaperAdjacentRehearsalRun,
    create_paper_adjacent_rehearsal_run_id,
    _now_str
)
from usa_signal_bot.core.enums import (
    PaperAdjacentRehearsalMode,
    PaperAdjacentRehearsalStatus
)
from usa_signal_bot.paper_controlled_planning.rehearsal_safety_guard import (
    assert_rehearsal_safe,
    collect_rehearsal_safety_flags_from_context,
    collect_rehearsal_safety_flags_from_proposals
)
from usa_signal_bot.paper_controlled_planning.adjacent_proposal_builder import build_adjacent_proposals
from usa_signal_bot.core.exceptions import GuardedPaperAdjacentRehearsalError

class GuardedPaperAdjacentRehearsalRunner:
    def __init__(self, mode: PaperAdjacentRehearsalMode = PaperAdjacentRehearsalMode.FULL_GUARDED_REHEARSAL):
        self.mode = mode

    def run_proposal_stage(self, context: PaperAdjacentRehearsalContext) -> List[PaperAdjacentProposal]:
        if self.mode in [PaperAdjacentRehearsalMode.SNAPSHOT_COMPARE_ONLY, PaperAdjacentRehearsalMode.DISABLED]:
            return []
        proposals = build_adjacent_proposals(context)
        return proposals

    def run_rehearsal(self, context: PaperAdjacentRehearsalContext) -> PaperAdjacentRehearsalRun:
        run_id = create_paper_adjacent_rehearsal_run_id()
        started_at = _now_str()

        try:
            assert_rehearsal_safe(context)
        except GuardedPaperAdjacentRehearsalError as e:
            return PaperAdjacentRehearsalRun(
                run_id=run_id, created_at_utc=started_at, status=PaperAdjacentRehearsalStatus.BLOCKED,
                context=context, proposals=[], safety_flags=collect_rehearsal_safety_flags_from_context(context),
                started_at_utc=started_at, completed_at_utc=_now_str(), output_paths={}, warnings=[], errors=[str(e)]
            )

        proposals = self.run_proposal_stage(context)

        try:
            assert_rehearsal_safe(context, proposals)
        except GuardedPaperAdjacentRehearsalError as e:
            return PaperAdjacentRehearsalRun(
                run_id=run_id, created_at_utc=started_at, status=PaperAdjacentRehearsalStatus.BLOCKED,
                context=context, proposals=proposals, safety_flags=collect_rehearsal_safety_flags_from_proposals(proposals),
                started_at_utc=started_at, completed_at_utc=_now_str(), output_paths={}, warnings=[], errors=[str(e)]
            )

        flags = collect_rehearsal_safety_flags_from_context(context)
        flags.extend(collect_rehearsal_safety_flags_from_proposals(proposals))

        return PaperAdjacentRehearsalRun(
            run_id=run_id,
            created_at_utc=started_at,
            status=PaperAdjacentRehearsalStatus.COMPLETED,
            context=context,
            proposals=proposals,
            safety_flags=list(set(flags)),
            started_at_utc=started_at,
            completed_at_utc=_now_str(),
            output_paths={"metadata": f"data/paper_controlled_planning/rehearsals/{run_id}.json"},
            warnings=[],
            errors=[]
        )

def validate_rehearsal_run_safety(run: PaperAdjacentRehearsalRun) -> List[str]:
    errors = []
    if run.context:
        if run.context.allow_active_paper: errors.append("Context allows active paper")
        if run.context.allow_paper_state_mutation: errors.append("Context allows paper state mutation")
        if run.context.allow_broker_orders: errors.append("Context allows broker orders")
    for p in run.proposals:
        if p.is_real_order: errors.append(f"Proposal {p.proposal_id} is real order")
        if p.will_mutate_paper_state: errors.append(f"Proposal {p.proposal_id} mutates paper state")
    return errors

def rehearsal_run_summary(run: PaperAdjacentRehearsalRun) -> dict[str, Any]:
    return {
        "run_id": run.run_id,
        "status": run.status.value,
        "proposal_count": len(run.proposals),
        "is_safe": len(validate_rehearsal_run_safety(run)) == 0
    }
