import datetime
from typing import Any, Dict, Optional
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    ReadinessRehearsalReview, ReadinessRehearsalRun, FinalReviewLock,
    GuardedHandoffRegistryEntry, HandoffEvidenceIndex, create_readiness_rehearsal_review_id
)
from usa_signal_bot.core.enums import ReadinessRehearsalReportType
from usa_signal_bot.paper_readiness_rehearsal.handoff_audit import (
    audit_entry_from_rehearsal_run, audit_entry_from_final_lock, audit_entry_from_handoff_entry
)

def build_readiness_rehearsal_review(
    run: ReadinessRehearsalRun,
    lock: Optional[FinalReviewLock] = None,
    handoff_entry: Optional[GuardedHandoffRegistryEntry] = None,
    evidence_index: Optional[HandoffEvidenceIndex] = None
) -> ReadinessRehearsalReview:

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    audit_entries = [audit_entry_from_rehearsal_run(run)]
    if lock:
        audit_entries.append(audit_entry_from_final_lock(lock))
    if handoff_entry:
        audit_entries.append(audit_entry_from_handoff_entry(handoff_entry))

    return ReadinessRehearsalReview(
        review_id=create_readiness_rehearsal_review_id(),
        created_at_utc=now_utc,
        report_type=ReadinessRehearsalReportType.FULL_READINESS_REHEARSAL_REVIEW,
        rehearsal_runs=[run],
        final_locks=[lock] if lock else [],
        handoff_entries=[handoff_entry] if handoff_entry else [],
        evidence_indexes=[evidence_index] if evidence_index else [],
        audit_entries=audit_entries,
        output_paths={},
        warnings=[],
        errors=[]
    )

def readiness_rehearsal_review_summary(review: ReadinessRehearsalReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "runs_count": len(review.rehearsal_runs),
        "locks_count": len(review.final_locks),
        "handoffs_count": len(review.handoff_entries),
        "evidences_count": len(review.evidence_indexes),
        "audit_entries_count": len(review.audit_entries)
    }

def readiness_rehearsal_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- No broker execution or live/demo order generation.\n"
        "- No active paper trading enablement.\n"
        "- No real paper state mutation.\n"
        "- No Telegram real send or dispatch.\n"
        "- No production config patching.\n"
        "- Final review lock is NOT a deployment approval.\n"
        "- Guarded handoff registry is NOT an activation.\n"
        "- NOT investment advice."
    )

def readiness_rehearsal_review_to_text(review: ReadinessRehearsalReview, limit: int = 100) -> str:
    lines = [f"Readiness Rehearsal Review [{review.review_id}]:"]
    lines.append(f"Runs: {len(review.rehearsal_runs)}")
    lines.append(f"Locks: {len(review.final_locks)}")
    lines.append(f"Handoffs: {len(review.handoff_entries)}")
    lines.append(f"Evidence Indexes: {len(review.evidence_indexes)}")
    lines.append(f"Audits: {len(review.audit_entries)}")
    lines.append(readiness_rehearsal_limitations_text())
    return "\n".join(lines)
