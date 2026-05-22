from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import AdmissionReviewReportType
from .admission_review_models import (
    AdmissionReviewFullReport,
    create_admission_full_report_id,
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    FinalNoWriteTransitionCheckpoint,
    AdmissionEvidenceSeal,
    AdmissionReviewAuditEntry
)
from .admission_decision import GuardedPaperModeAdmissionReviewDecisionEngine
from .ledger_reconciliation import reconcile_human_approval_ledger
from .admission_evidence_seal import build_admission_evidence_seal
from .transition_checkpoint import build_final_no_write_transition_checkpoint
from .admission_gates import default_admission_review_gates
from .admission_audit import (
    audit_entry_from_admission_review,
    audit_entry_from_ledger_reconciliation,
    audit_entry_from_transition_checkpoint
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def admission_review_limitations_text() -> str:
    return """
ADMISSION REVIEW LIMITATIONS:
- Admission review is metadata only.
- Ledger reconciliation is not an active paper/live/demo approval.
- Final no-write transition checkpoint is not an activation.
- No broker API is used.
- No paper state mutation occurs.
- No Telegram real send is executed.
- No production config patch is applied.
- This is NOT investment advice.
"""

def build_admission_review_full_report(dry_admission_payload: Dict[str, Any]) -> AdmissionReviewFullReport:
    engine = GuardedPaperModeAdmissionReviewDecisionEngine()
    gates = default_admission_review_gates(dry_admission_payload)
    reconciliation = reconcile_human_approval_ledger(dry_admission_payload)
    evidence_seal = build_admission_evidence_seal(evidence_refs=dry_admission_payload.get("evidence_refs", []))

    review = engine.decide(dry_admission_payload, gates, reconciliation, evidence_seal)
    evidence_seal = build_admission_evidence_seal(review)
    review.evidence_seal = evidence_seal

    checkpoint = build_final_no_write_transition_checkpoint(review, reconciliation, evidence_seal)

    return build_admission_review_report_from_parts(review, reconciliation, checkpoint, evidence_seal)

def build_admission_review_report_from_parts(
    admission_review: PaperModeAdmissionReview,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    checkpoint: Optional[FinalNoWriteTransitionCheckpoint] = None,
    evidence_seal: Optional[AdmissionEvidenceSeal] = None
) -> AdmissionReviewFullReport:

    audit_entries = []
    audit_entries.append(audit_entry_from_admission_review(admission_review))
    if reconciliation:
        audit_entries.append(audit_entry_from_ledger_reconciliation(reconciliation))
    if checkpoint:
        audit_entries.append(audit_entry_from_transition_checkpoint(checkpoint))

    return AdmissionReviewFullReport(
        report_id=create_admission_full_report_id(),
        created_at_utc=_now(),
        report_type=AdmissionReviewReportType.FULL_ADMISSION_REVIEW,
        admission_reviews=[admission_review],
        ledger_reconciliations=[reconciliation] if reconciliation else [],
        evidence_seals=[evidence_seal] if evidence_seal else [],
        transition_checkpoints=[checkpoint] if checkpoint else [],
        audit_entries=audit_entries,
        output_paths={},
        warnings=[admission_review_limitations_text()],
        errors=[]
    )

def admission_review_full_report_summary(report: AdmissionReviewFullReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "reviews_count": len(report.admission_reviews),
        "reconciliations_count": len(report.ledger_reconciliations),
        "seals_count": len(report.evidence_seals),
        "checkpoints_count": len(report.transition_checkpoints),
        "audit_entries_count": len(report.audit_entries)
    }

def admission_review_full_report_to_text(report: AdmissionReviewFullReport, limit: int = 100) -> str:
    return json.dumps(admission_review_full_report_summary(report), indent=2)
