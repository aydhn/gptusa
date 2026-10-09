from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json, list_files, count_files
from pathlib import Path
from typing import Any, List

from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    PaperModeDryAdmissionPlan,
    PaperModeDryAdmissionRun,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger,
    HumanApprovalLedgerEntry,
    DryAdmissionAuditEntry,
    DryAdmissionFullReview,
    paper_mode_dry_admission_plan_to_dict,
    paper_mode_dry_admission_run_to_dict,
    runtime_write_lock_proof_refresh_to_dict,
    human_approval_ledger_to_dict,
    human_approval_ledger_entry_to_dict,
    dry_admission_audit_entry_to_dict,
    dry_admission_full_review_to_dict
)

def dry_admission_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_dry_admission"
    ensure_dir(d)
    return d

def dry_admission_plans_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "plans"
    ensure_dir(d)
    return d

def dry_admission_runs_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "runs"
    ensure_dir(d)
    return d

def write_lock_refreshes_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "write_lock_refreshes"
    ensure_dir(d)
    return d

def human_ledgers_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "human_ledgers"
    ensure_dir(d)
    return d

def human_ledger_entries_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "human_ledger_entries"
    ensure_dir(d)
    return d

def dry_admission_audit_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "audit"
    ensure_dir(d)
    return d

def dry_admission_reviews_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "reviews"
    ensure_dir(d)
    return d


def write_dry_admission_plan_json(path: Path, item: PaperModeDryAdmissionPlan) -> Path:
    return write_json(path, paper_mode_dry_admission_plan_to_dict(item), ensure_parent=False)

def write_dry_admission_run_json(path: Path, item: PaperModeDryAdmissionRun) -> Path:
    return write_json(path, paper_mode_dry_admission_run_to_dict(item), ensure_parent=False)

def write_write_lock_refresh_json(path: Path, item: RuntimeWriteLockProofRefresh) -> Path:
    return write_json(path, runtime_write_lock_proof_refresh_to_dict(item), ensure_parent=False)

def write_human_approval_ledger_json(path: Path, item: HumanApprovalLedger) -> Path:
    return write_json(path, human_approval_ledger_to_dict(item), ensure_parent=False)

def write_human_approval_ledger_entries_jsonl(path: Path, items: List[HumanApprovalLedgerEntry]) -> Path:
    return write_jsonl(path, (human_approval_ledger_entry_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_dry_admission_audit_jsonl(path: Path, items: List[DryAdmissionAuditEntry]) -> Path:
    return write_jsonl(path, (dry_admission_audit_entry_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_dry_admission_full_review_json(path: Path, item: DryAdmissionFullReview) -> Path:
    return write_json(path, dry_admission_full_review_to_dict(item), ensure_parent=False)

def read_dry_admission_full_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def list_dry_admission_full_reviews(data_root: Path) -> List[Path]:
    d = dry_admission_reviews_dir(data_root)
    return list_files(d, "*.json", sort=True)

def get_latest_dry_admission_full_review(data_root: Path) -> Path | None:
    files = list_dry_admission_full_reviews(data_root)
    return files[-1] if files else None

def dry_admission_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "plans": count_files(dry_admission_plans_dir(data_root), "*.json"),
        "runs": count_files(dry_admission_runs_dir(data_root), "*.json"),
        "write_lock_refreshes": count_files(write_lock_refreshes_dir(data_root), "*.json"),
        "human_ledgers": count_files(human_ledgers_dir(data_root), "*.json"),
        "reviews": len(list_dry_admission_full_reviews(data_root))
    }
