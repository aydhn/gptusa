import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import GuardedHandoffStatus, GuardedHandoffDecision
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    GuardedHandoffRegistryEntry, ReadinessRehearsalRun, FinalReviewLock, HandoffEvidenceIndex,
    create_guarded_handoff_id, validate_guarded_handoff_registry_entry
)
from usa_signal_bot.paper_readiness_rehearsal.handoff_decision_metadata import (
    determine_guarded_handoff_decision, guarded_handoff_required_followups
)

def build_guarded_handoff_registry_entry(run: ReadinessRehearsalRun, lock: FinalReviewLock, evidence_index: HandoffEvidenceIndex) -> GuardedHandoffRegistryEntry:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    decision = determine_guarded_handoff_decision(run, lock, evidence_index)

    if decision == GuardedHandoffDecision.BLOCK:
        status = GuardedHandoffStatus.BLOCKED
    elif decision == GuardedHandoffDecision.REJECT:
        status = GuardedHandoffStatus.REJECTED
    elif decision == GuardedHandoffDecision.REGISTER_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW:
        status = GuardedHandoffStatus.READY_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW
    else:
        status = GuardedHandoffStatus.REQUEST_CHANGES

    followups = guarded_handoff_required_followups(decision, run.safety_flags)

    entry = GuardedHandoffRegistryEntry(
        handoff_id=create_guarded_handoff_id(),
        created_at_utc=now_utc,
        status=status,
        decision=decision,
        candidate_id=run.candidate_id,
        dossier_id=None, # Needs to be passed down if available
        board_review_id=None,
        readiness_package_id=run.source_package_id,
        rehearsal_run_id=run.run_id,
        final_lock_id=lock.lock_id,
        evidence_refs=[evidence_index.evidence_index_id],
        required_followups=followups,
        safety_flags=run.safety_flags.copy(),
        manual_review_required=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )
    validate_guarded_handoff_registry_entry(entry)
    return entry

def register_guarded_handoff_entry(entry: GuardedHandoffRegistryEntry, registry: Optional[List[GuardedHandoffRegistryEntry]] = None) -> List[GuardedHandoffRegistryEntry]:
    registry = registry or []
    registry.append(entry)
    return registry

def find_handoff_entry_by_id(registry: List[GuardedHandoffRegistryEntry], handoff_id: str) -> Optional[GuardedHandoffRegistryEntry]:
    for entry in registry:
        if entry.handoff_id == handoff_id:
            return entry
    return None

def find_handoff_entries_by_candidate_id(registry: List[GuardedHandoffRegistryEntry], candidate_id: str) -> List[GuardedHandoffRegistryEntry]:
    return [e for e in registry if e.candidate_id == candidate_id]

def latest_handoff_entry_for_candidate(registry: List[GuardedHandoffRegistryEntry], candidate_id: str) -> Optional[GuardedHandoffRegistryEntry]:
    entries = find_handoff_entries_by_candidate_id(registry, candidate_id)
    if not entries:
        return None
    # Sort by created_at_utc
    return sorted(entries, key=lambda x: x.created_at_utc)[-1]

def guarded_handoff_registry_summary(registry: List[GuardedHandoffRegistryEntry]) -> Dict[str, Any]:
    return {"total_entries": len(registry)}

def guarded_handoff_registry_to_text(registry: List[GuardedHandoffRegistryEntry], limit: int = 100) -> str:
    lines = [f"Guarded Handoff Registry ({len(registry)} entries):"]
    for e in registry[:limit]:
        lines.append(f" - {e.handoff_id}: Status {e.status.value}, Decision {e.decision.value}")
    return "\n".join(lines)
