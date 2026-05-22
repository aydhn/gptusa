from typing import Any
from pathlib import Path
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import (
    NoWritePaperAdmissionContract, NoWriteContractClause, ActivationReplayPlan,
    ActivationReplayResult, PaperModePreflightRun, NoWriteAdmissionAuditEntry,
    NoWriteAdmissionFullReview
)

def no_write_admission_store_dir(data_root: Path) -> Path:
    return data_root / "paper_no_write_admission"

def contracts_dir(data_root: Path) -> Path:
    return no_write_admission_store_dir(data_root) / "contracts"

def contract_clauses_dir(data_root: Path) -> Path:
    return no_write_admission_store_dir(data_root) / "clauses"

def activation_replay_plans_dir(data_root: Path) -> Path:
    return no_write_admission_store_dir(data_root) / "activation_replay_plans"

def activation_replay_results_dir(data_root: Path) -> Path:
    return no_write_admission_store_dir(data_root) / "activation_replay_results"

def paper_mode_preflights_dir(data_root: Path) -> Path:
    return no_write_admission_store_dir(data_root) / "paper_mode_preflights"

def no_write_admission_audit_dir(data_root: Path) -> Path:
    return no_write_admission_store_dir(data_root) / "audit"

def no_write_full_reviews_dir(data_root: Path) -> Path:
    return no_write_admission_store_dir(data_root) / "full_reviews"

def write_no_write_contract_json(path: Path, item: NoWritePaperAdmissionContract) -> Path:
    return path

def write_contract_clauses_jsonl(path: Path, items: list[NoWriteContractClause]) -> Path:
    return path

def write_activation_replay_plan_json(path: Path, item: ActivationReplayPlan) -> Path:
    return path

def write_activation_replay_result_json(path: Path, item: ActivationReplayResult) -> Path:
    return path

def write_paper_mode_preflight_json(path: Path, item: PaperModePreflightRun) -> Path:
    return path

def write_no_write_admission_audit_jsonl(path: Path, items: list[NoWriteAdmissionAuditEntry]) -> Path:
    return path

def write_no_write_full_review_json(path: Path, item: NoWriteAdmissionFullReview) -> Path:
    return path

def read_no_write_full_review_json(path: Path) -> dict[str, Any]:
    return {}

def list_no_write_full_reviews(data_root: Path) -> list[Path]:
    return []

def get_latest_no_write_full_review(data_root: Path) -> Path | None:
    return None

def no_write_admission_store_summary(data_root: Path) -> dict[str, Any]:
    return {}
