from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_common.io import write_json, write_jsonl, read_json, list_files

from usa_signal_bot.core.exceptions import AdmissionReviewStorageError
from .admission_review_models import (
    PaperModeAdmissionReview,
    AdmissionReviewGate,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal,
    FinalNoWriteTransitionCheckpoint,
    AdmissionReviewAuditEntry,
    AdmissionReviewFullReport,
    paper_mode_admission_review_to_dict,
    admission_review_gate_to_dict,
    ledger_reconciliation_report_to_dict,
    admission_evidence_seal_to_dict,
    final_no_write_transition_checkpoint_to_dict,
    admission_review_audit_entry_to_dict,
    admission_review_full_report_to_dict
)

def admission_review_store_dir(data_root: Path) -> Path:
    return data_root / "paper_admission_review"

def admission_reviews_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "admission_reviews"

def admission_gates_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "gates"

def ledger_reconciliations_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "ledger_reconciliations"

def admission_evidence_seals_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "evidence_seals"

def transition_checkpoints_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "transition_checkpoints"

def admission_audit_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "audit"

def admission_full_reports_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "full_reports"

def write_admission_review_json(path: Path, item: PaperModeAdmissionReview) -> Path:
    return write_json(path, paper_mode_admission_review_to_dict(item))

def write_admission_gates_jsonl(path: Path, items: List[AdmissionReviewGate]) -> Path:
    return write_jsonl(path, (admission_review_gate_to_dict(item) for item in items))

def write_ledger_reconciliation_json(path: Path, item: LedgerReconciliationReport) -> Path:
    return write_json(path, ledger_reconciliation_report_to_dict(item))

def write_admission_evidence_seal_json(path: Path, item: AdmissionEvidenceSeal) -> Path:
    return write_json(path, admission_evidence_seal_to_dict(item))

def write_transition_checkpoint_json(path: Path, item: FinalNoWriteTransitionCheckpoint) -> Path:
    return write_json(path, final_no_write_transition_checkpoint_to_dict(item))

def write_admission_audit_jsonl(path: Path, items: List[AdmissionReviewAuditEntry]) -> Path:
    return write_jsonl(path, (admission_review_audit_entry_to_dict(item) for item in items), mode="a")

def write_admission_full_report_json(path: Path, item: AdmissionReviewFullReport) -> Path:
    return write_json(path, admission_review_full_report_to_dict(item))

def read_admission_full_report_json(path: Path) -> Dict[str, Any]:
    return read_json(path)

def list_admission_full_reports(data_root: Path) -> List[Path]:
    d = admission_full_reports_dir(data_root)
    return list_files(d, "*.json", sort=True)

def get_latest_admission_full_report(data_root: Path) -> Optional[Path]:
    reports = list_admission_full_reports(data_root)
    return reports[-1] if reports else None

def admission_review_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "full_reports_count": len(list_admission_full_reports(data_root))
    }

# Phase 90 integration stub

# Phase 90 integration
