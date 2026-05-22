from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperAuditEntry,
    PrePaperDryRehearsalRun,
    ActivationDeniedCheckpoint,
    create_pre_paper_audit_id
)
from usa_signal_bot.core.enums import PrePaperRiskFlag

def create_pre_paper_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[PrePaperRiskFlag]] = None
) -> PrePaperAuditEntry:
    return PrePaperAuditEntry(
        audit_id=create_pre_paper_audit_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[]
    )

def audit_entry_from_pre_paper_run(run: PrePaperDryRehearsalRun) -> PrePaperAuditEntry:
    return create_pre_paper_audit_entry(
        entity_type="PrePaperDryRehearsalRun",
        entity_id=run.run_id,
        action="Run Rehearsal",
        decision=run.decision.value,
        rationale=f"Completed pre-paper rehearsal run with status {run.status.value}",
        evidence_refs=[run.plan.plan_id] if run.plan else [],
        risk_flags=run.safety_flags
    )

def audit_entry_from_activation_checkpoint(checkpoint: ActivationDeniedCheckpoint) -> PrePaperAuditEntry:
    return create_pre_paper_audit_entry(
        entity_type="ActivationDeniedCheckpoint",
        entity_id=checkpoint.checkpoint_id,
        action="Evaluate Activation",
        decision=checkpoint.decision.value,
        rationale=checkpoint.denial_reason,
        evidence_refs=[checkpoint.source_run_id] if checkpoint.source_run_id else [],
        risk_flags=checkpoint.safety_flags
    )

def append_pre_paper_audit_entry(entries: List[PrePaperAuditEntry], entry: PrePaperAuditEntry) -> List[PrePaperAuditEntry]:
    return entries + [entry]

def pre_paper_audit_summary(entries: List[PrePaperAuditEntry]) -> Dict[str, Any]:
    return {
        "audit_count": len(entries),
        "entities": list(set(e.entity_type for e in entries))
    }

def pre_paper_audit_to_text(entries: List[PrePaperAuditEntry], limit: int = 100) -> str:
    s = pre_paper_audit_summary(entries)
    return f"Pre-Paper Audit: {s['audit_count']} entries across {len(s['entities'])} entity types"
