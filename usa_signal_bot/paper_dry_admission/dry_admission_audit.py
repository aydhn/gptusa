from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    DryAdmissionAuditEntry,
    PaperModeDryAdmissionRun,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger,
    create_dry_admission_audit_id
)
from usa_signal_bot.core.enums import DryAdmissionRiskFlag
from usa_signal_bot.paper_dry_admission.dry_admission_safety_validator import collect_dry_admission_safety_flags

def create_dry_admission_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: List[str] | None = None,
    risk_flags: List[DryAdmissionRiskFlag] | None = None
) -> DryAdmissionAuditEntry:

    return DryAdmissionAuditEntry(
        audit_id=create_dry_admission_audit_id(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        rationale=rationale,
        decision=decision,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or []
    )

def audit_entry_from_dry_admission_run(run: PaperModeDryAdmissionRun) -> DryAdmissionAuditEntry:
    return create_dry_admission_audit_entry(
        entity_type="PaperModeDryAdmissionRun",
        entity_id=run.run_id,
        action="DRY_ADMISSION_REHEARSAL",
        rationale=f"Executed dry admission run. Status: {run.status.value}",
        decision=run.decision.value,
        evidence_refs=[run.plan.plan_id] if run.plan else [],
        risk_flags=run.safety_flags
    )

def audit_entry_from_write_lock_refresh(refresh: RuntimeWriteLockProofRefresh) -> DryAdmissionAuditEntry:
    return create_dry_admission_audit_entry(
        entity_type="RuntimeWriteLockProofRefresh",
        entity_id=refresh.refresh_id,
        action="WRITE_LOCK_PROOF_REFRESH",
        rationale=f"Refreshed runtime write lock proof. Unchanged: {refresh.hash_unchanged}",
        decision=refresh.decision.value,
        evidence_refs=[refresh.source_write_block_proof_id] if refresh.source_write_block_proof_id else [],
        risk_flags=refresh.risk_flags
    )

def audit_entry_from_human_ledger(ledger: HumanApprovalLedger) -> DryAdmissionAuditEntry:
    return create_dry_admission_audit_entry(
        entity_type="HumanApprovalLedger",
        entity_id=ledger.ledger_id,
        action="HUMAN_APPROVAL_LEDGER_REVIEW",
        rationale=f"Ledger created. Missing scopes: {len(ledger.missing_scopes)}",
        decision=ledger.decision.value,
        evidence_refs=[e.ledger_entry_id for e in ledger.entries],
        risk_flags=ledger.risk_flags
    )

def append_dry_admission_audit_entry(entries: List[DryAdmissionAuditEntry], entry: DryAdmissionAuditEntry) -> List[DryAdmissionAuditEntry]:
    return entries + [entry]

def dry_admission_audit_summary(entries: List[DryAdmissionAuditEntry]) -> dict[str, Any]:
    return {
        "entry_count": len(entries),
        "actions": [e.action for e in entries],
        "decisions": [e.decision for e in entries if e.decision]
    }

def dry_admission_audit_to_text(entries: List[DryAdmissionAuditEntry], limit: int = 100) -> str:
    lines = [f"Audit Entries: {len(entries)}"]
    for i, e in enumerate(entries[:limit]):
        lines.append(f"{i+1}. {e.action} on {e.entity_type} ({e.entity_id}) -> {e.decision or 'NO_DECISION'}")
    if len(entries) > limit:
        lines.append(f"... {len(entries) - limit} more entries")
    return "\n".join(lines)
