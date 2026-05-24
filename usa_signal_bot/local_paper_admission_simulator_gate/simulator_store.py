from pathlib import Path
from typing import Any
from .simulator_gate_models import (
    FinalLocalPaperAdmissionSimulatorGate, RehearsalReplayPlan, RehearsalReplayResult,
    RehearsalReplayItem, DryAdmissionEvidenceFreezeBundle, SimulatorGateRule,
    SimulatorGateAssertion, SimulatorGateAuditEntry, SimulatorGateFullReview
)

def simulator_gate_store_dir(data_root: Path) -> Path:
    return data_root / "local_paper_admission_simulator_gate"

def final_simulator_gates_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "gates"

def rehearsal_replay_plans_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "rehearsal_replay_plans"

def rehearsal_replay_results_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "rehearsal_replay_results"

def rehearsal_replay_items_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "rehearsal_replay_items"

def dry_admission_evidence_freezes_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "dry_admission_evidence_freezes"

def simulator_rules_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "rules"

def simulator_assertions_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "assertions"

def simulator_audit_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "audit"

def simulator_full_reviews_dir(data_root: Path) -> Path:
    return simulator_gate_store_dir(data_root) / "full_reviews"

def write_final_simulator_gate_json(path: Path, item: FinalLocalPaperAdmissionSimulatorGate) -> Path:
    return path

def write_rehearsal_replay_plan_json(path: Path, item: RehearsalReplayPlan) -> Path:
    return path

def write_rehearsal_replay_result_json(path: Path, item: RehearsalReplayResult) -> Path:
    return path

def write_rehearsal_replay_items_jsonl(path: Path, items: list[RehearsalReplayItem]) -> Path:
    return path

def write_dry_admission_evidence_freeze_json(path: Path, item: DryAdmissionEvidenceFreezeBundle) -> Path:
    return path

def write_simulator_rules_jsonl(path: Path, items: list[SimulatorGateRule]) -> Path:
    return path

def write_simulator_assertions_jsonl(path: Path, items: list[SimulatorGateAssertion]) -> Path:
    return path

def write_simulator_audit_jsonl(path: Path, items: list[SimulatorGateAuditEntry]) -> Path:
    return path

def write_simulator_full_review_json(path: Path, item: SimulatorGateFullReview) -> Path:
    return path

def read_simulator_full_review_json(path: Path) -> dict[str, Any]:
    return {}

def list_simulator_full_reviews(data_root: Path) -> list[Path]:
    return []

def get_latest_simulator_full_review(data_root: Path) -> Path | None:
    return None

def simulator_store_summary(data_root: Path) -> dict[str, Any]:
    return {}
