import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    ReadinessRehearsalAuditEntry, ReadinessRehearsalRun, FinalReviewLock, GuardedHandoffRegistryEntry,
    create_readiness_rehearsal_audit_id
)
from usa_signal_bot.core.enums import ReadinessRehearsalRiskFlag

def create_readiness_rehearsal_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[ReadinessRehearsalRiskFlag]] = None
) -> ReadinessRehearsalAuditEntry:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ReadinessRehearsalAuditEntry(
        audit_id=create_readiness_rehearsal_audit_id(),
        created_at_utc=now_utc,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[],
        metadata={}
    )

def audit_entry_from_rehearsal_run(run: ReadinessRehearsalRun) -> ReadinessRehearsalAuditEntry:
    return create_readiness_rehearsal_audit_entry(
        entity_type="ReadinessRehearsalRun",
        entity_id=run.run_id,
        action="Run Rehearsal",
        rationale="Staged paper readiness rehearsal completed",
        decision=run.decision.value,
        evidence_refs=[r.result_id for r in run.stage_results],
        risk_flags=run.safety_flags
    )

def audit_entry_from_final_lock(lock: FinalReviewLock) -> ReadinessRehearsalAuditEntry:
    return create_readiness_rehearsal_audit_entry(
        entity_type="FinalReviewLock",
        entity_id=lock.lock_id,
        action="Generate Lock",
        rationale=lock.lock_reason,
        decision=lock.status.value,
        evidence_refs=lock.locked_artifact_refs,
        risk_flags=[]
    )

def audit_entry_from_handoff_entry(entry: GuardedHandoffRegistryEntry) -> ReadinessRehearsalAuditEntry:
    return create_readiness_rehearsal_audit_entry(
        entity_type="GuardedHandoffRegistryEntry",
        entity_id=entry.handoff_id,
        action="Register Handoff",
        rationale="Registered in guarded handoff registry",
        decision=entry.decision.value,
        evidence_refs=entry.evidence_refs,
        risk_flags=entry.safety_flags
    )

def append_readiness_rehearsal_audit_entry(entries: List[ReadinessRehearsalAuditEntry], entry: ReadinessRehearsalAuditEntry) -> List[ReadinessRehearsalAuditEntry]:
    entries.append(entry)
    return entries

def readiness_rehearsal_audit_summary(entries: List[ReadinessRehearsalAuditEntry]) -> Dict[str, Any]:
    return {"total_audit_entries": len(entries)}

def readiness_rehearsal_audit_to_text(entries: List[ReadinessRehearsalAuditEntry], limit: int = 100) -> str:
    lines = [f"Readiness Rehearsal Audit Log ({len(entries)} entries):"]
    for e in entries[:limit]:
        lines.append(f" - [{e.created_at_utc}] {e.action} on {e.entity_type} ({e.entity_id}): {e.decision} - {e.rationale}")
    return "\n".join(lines)
