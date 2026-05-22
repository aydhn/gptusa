import json
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
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_plans_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_runs_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_lock_refreshes_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "write_lock_refreshes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def human_ledgers_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "human_ledgers"
    d.mkdir(parents=True, exist_ok=True)
    return d

def human_ledger_entries_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "human_ledger_entries"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_audit_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_reviews_dir(data_root: Path) -> Path:
    d = dry_admission_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_dry_admission_plan_json(path: Path, item: PaperModeDryAdmissionPlan) -> Path:
    with open(path, "w") as f:
        json.dump(paper_mode_dry_admission_plan_to_dict(item), f, indent=2)
    return path

def write_dry_admission_run_json(path: Path, item: PaperModeDryAdmissionRun) -> Path:
    with open(path, "w") as f:
        json.dump(paper_mode_dry_admission_run_to_dict(item), f, indent=2)
    return path

def write_write_lock_refresh_json(path: Path, item: RuntimeWriteLockProofRefresh) -> Path:
    with open(path, "w") as f:
        json.dump(runtime_write_lock_proof_refresh_to_dict(item), f, indent=2)
    return path

def write_human_approval_ledger_json(path: Path, item: HumanApprovalLedger) -> Path:
    with open(path, "w") as f:
        json.dump(human_approval_ledger_to_dict(item), f, indent=2)
    return path

def write_human_approval_ledger_entries_jsonl(path: Path, items: List[HumanApprovalLedgerEntry]) -> Path:
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(human_approval_ledger_entry_to_dict(item)) + "\n")
    return path

def write_dry_admission_audit_jsonl(path: Path, items: List[DryAdmissionAuditEntry]) -> Path:
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(dry_admission_audit_entry_to_dict(item)) + "\n")
    return path

def write_dry_admission_full_review_json(path: Path, item: DryAdmissionFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(dry_admission_full_review_to_dict(item), f, indent=2)
    return path

def read_dry_admission_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_dry_admission_full_reviews(data_root: Path) -> List[Path]:
    d = dry_admission_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_dry_admission_full_review(data_root: Path) -> Path | None:
    files = list_dry_admission_full_reviews(data_root)
    return files[-1] if files else None

def dry_admission_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "plans": len(list(dry_admission_plans_dir(data_root).glob("*.json"))),
        "runs": len(list(dry_admission_runs_dir(data_root).glob("*.json"))),
        "write_lock_refreshes": len(list(write_lock_refreshes_dir(data_root).glob("*.json"))),
        "human_ledgers": len(list(human_ledgers_dir(data_root).glob("*.json"))),
        "reviews": len(list_dry_admission_full_reviews(data_root))
    }
