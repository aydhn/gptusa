from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .admission_review_models import (
    AdmissionReviewAuditEntry,
    create_admission_audit_id,
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    FinalNoWriteTransitionCheckpoint
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_admission_review_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[AdmissionReviewRiskFlag]] = None
) -> AdmissionReviewAuditEntry:
    return AdmissionReviewAuditEntry(
        audit_id=create_admission_audit_id(),
        created_at_utc=_now(),
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

def audit_entry_from_admission_review(review: PaperModeAdmissionReview) -> AdmissionReviewAuditEntry:
    return create_admission_review_audit_entry(
        entity_type="PaperModeAdmissionReview",
        entity_id=review.admission_review_id,
        action="Admission Review Processed",
        rationale=f"Review completed with status {review.status}",
        decision=review.decision,
        evidence_refs=review.evidence_refs,
        risk_flags=review.safety_flags
    )

def audit_entry_from_ledger_reconciliation(report: LedgerReconciliationReport) -> AdmissionReviewAuditEntry:
    return create_admission_review_audit_entry(
        entity_type="LedgerReconciliationReport",
        entity_id=report.reconciliation_id,
        action="Ledger Reconciliation Processed",
        rationale=f"Reconciliation completed with status {report.status}",
        decision=report.decision,
        evidence_refs=[],
        risk_flags=report.safety_flags
    )

def audit_entry_from_transition_checkpoint(checkpoint: FinalNoWriteTransitionCheckpoint) -> AdmissionReviewAuditEntry:
    return create_admission_review_audit_entry(
        entity_type="FinalNoWriteTransitionCheckpoint",
        entity_id=checkpoint.checkpoint_id,
        action="Transition Checkpoint Processed",
        rationale=f"Checkpoint completed with status {checkpoint.status}",
        decision=checkpoint.decision,
        evidence_refs=[],
        risk_flags=checkpoint.safety_flags
    )

def append_admission_audit_entry(entries: List[AdmissionReviewAuditEntry], entry: AdmissionReviewAuditEntry) -> List[AdmissionReviewAuditEntry]:
    # Placeholder for redaction
    redacted_entry = entry
    entries.append(redacted_entry)
    return entries

def admission_audit_summary(entries: List[AdmissionReviewAuditEntry]) -> Dict[str, Any]:
    return {
        "total_entries": len(entries),
        "latest_audit_id": entries[-1].audit_id if entries else None,
        "actions": list(set([e.action for e in entries]))
    }

def admission_audit_to_text(entries: List[AdmissionReviewAuditEntry], limit: int = 100) -> str:
    return json.dumps([e.__dict__ for e in entries[:limit]], indent=2, default=str)
