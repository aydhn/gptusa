import json
from typing import Any, Dict
from .admission_review_models import (
    AdmissionReviewGate,
    LedgerReconciliationItem,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal,
    FinalNoWriteTransitionCheckpoint,
    PaperModeAdmissionReview,
    AdmissionReviewAuditEntry,
    AdmissionReviewFullReport
)
from .admission_report import admission_review_limitations_text

def admission_review_gate_to_text(item: AdmissionReviewGate) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def ledger_reconciliation_item_to_text(item: LedgerReconciliationItem) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def ledger_reconciliation_report_to_text(item: LedgerReconciliationReport, limit: int = 100) -> str:
    d = item.__dict__.copy()
    d["items"] = [i.__dict__ for i in item.items[:limit]]
    return json.dumps(d, indent=2, default=str)

def admission_evidence_seal_to_text(item: AdmissionEvidenceSeal) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def final_no_write_transition_checkpoint_to_text(item: FinalNoWriteTransitionCheckpoint) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def paper_mode_admission_review_to_text(item: PaperModeAdmissionReview, limit: int = 100) -> str:
    d = item.__dict__.copy()
    d["gates"] = [g.__dict__ for g in item.gates[:limit]]
    if item.ledger_reconciliation:
        d["ledger_reconciliation"] = "..."
    if item.evidence_seal:
        d["evidence_seal"] = "..."
    return json.dumps(d, indent=2, default=str)

def admission_review_audit_entry_to_text(item: AdmissionReviewAuditEntry) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def admission_review_full_report_to_text(item: AdmissionReviewFullReport, limit: int = 100) -> str:
    d = item.__dict__.copy()
    d["admission_reviews"] = [paper_mode_admission_review_to_text(r, limit) for r in item.admission_reviews[:limit]]
    return json.dumps(d, indent=2, default=str)

def admission_review_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return json.dumps(summary, indent=2)
