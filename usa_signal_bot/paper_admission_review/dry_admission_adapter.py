from typing import Any, Dict
import json
from .admission_review_models import PaperModeAdmissionReview, LedgerReconciliationReport, FinalNoWriteTransitionCheckpoint, AdmissionReviewFullReport
from .admission_report import build_admission_review_full_report

def admission_review_from_dry_admission(payload: Dict[str, Any]) -> PaperModeAdmissionReview:
    report = build_admission_review_full_report(payload)
    return report.admission_reviews[0]

def ledger_reconciliation_from_dry_admission(payload: Dict[str, Any]) -> LedgerReconciliationReport:
    report = build_admission_review_full_report(payload)
    return report.ledger_reconciliations[0] if report.ledger_reconciliations else None

def transition_checkpoint_from_dry_admission(payload: Dict[str, Any]) -> FinalNoWriteTransitionCheckpoint:
    report = build_admission_review_full_report(payload)
    return report.transition_checkpoints[0] if report.transition_checkpoints else None

def admission_full_report_from_dry_admission(payload: Dict[str, Any]) -> AdmissionReviewFullReport:
    return build_admission_review_full_report(payload)

def attach_admission_review_metadata_to_dry_admission_payload(payload: Dict[str, Any], report: AdmissionReviewFullReport) -> Dict[str, Any]:
    payload["admission_review_id"] = report.admission_reviews[0].admission_review_id if report.admission_reviews else None
    payload["transition_checkpoint_id"] = report.transition_checkpoints[0].checkpoint_id if report.transition_checkpoints else None
    return payload

def dry_admission_admission_review_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"admission_review_id": payload.get("admission_review_id")}

def dry_admission_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(dry_admission_admission_review_summary(payload), indent=2)
