from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json, list_files, count_files
from pathlib import Path
from typing import Any
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorDossierEvidenceItem,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerRule,
    PaperSandboxRuntimeAdmissionBlockerEvent,
    SimulatorDossierAuditEntry,
    SimulatorDossierFullReview,
    local_paper_admission_simulator_gate_dossier_to_dict,
    simulator_dossier_evidence_item_to_dict,
    simulator_acceptance_seal_to_dict,
    sandbox_runtime_admission_blocker_rule_to_dict,
    sandbox_runtime_admission_blocker_event_to_dict,
    simulator_dossier_audit_entry_to_dict,
    simulator_dossier_full_review_to_dict
)

def simulator_dossier_store_dir(data_root: Path) -> Path:
    p = data_root / "local_paper_admission_simulator_dossier"
    ensure_dir(p)
    return p

def simulator_dossiers_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "dossiers"
    ensure_dir(p)
    return p

def simulator_dossier_evidence_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "evidence"
    ensure_dir(p)
    return p

def simulator_acceptance_seals_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "acceptance_seals"
    ensure_dir(p)
    return p

def sandbox_runtime_admission_blocker_rules_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "sandbox_runtime_admission_blocker_rules"
    ensure_dir(p)
    return p

def sandbox_runtime_admission_blocker_events_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "sandbox_runtime_admission_blocker_events"
    ensure_dir(p)
    return p

def simulator_dossier_audit_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "audit"
    ensure_dir(p)
    return p

def simulator_dossier_full_reviews_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "full_reviews"
    ensure_dir(p)
    return p

def write_simulator_dossier_json(path: Path, item: LocalPaperAdmissionSimulatorGateDossier) -> Path:
    return write_json(path, local_paper_admission_simulator_gate_dossier_to_dict(item), ensure_parent=False)

def write_simulator_dossier_evidence_jsonl(path: Path, items: list[SimulatorDossierEvidenceItem]) -> Path:
    return write_jsonl(path, (simulator_dossier_evidence_item_to_dict(i) for i in items), ensure_parent=False)

def write_simulator_acceptance_seal_json(path: Path, item: SimulatorAcceptanceSeal) -> Path:
    return write_json(path, simulator_acceptance_seal_to_dict(item), ensure_parent=False)

def write_sandbox_runtime_admission_blocker_rules_jsonl(path: Path, items: list[PaperSandboxRuntimeAdmissionBlockerRule]) -> Path:
    return write_jsonl(path, (sandbox_runtime_admission_blocker_rule_to_dict(i) for i in items), ensure_parent=False)

def write_sandbox_runtime_admission_blocker_events_jsonl(path: Path, items: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> Path:
    return write_jsonl(path, (sandbox_runtime_admission_blocker_event_to_dict(i) for i in items), ensure_parent=False)

def write_simulator_dossier_audit_jsonl(path: Path, items: list[SimulatorDossierAuditEntry]) -> Path:
    return write_jsonl(path, (simulator_dossier_audit_entry_to_dict(i) for i in items), ensure_parent=False)

def write_simulator_dossier_full_review_json(path: Path, item: SimulatorDossierFullReview) -> Path:
    return write_json(path, simulator_dossier_full_review_to_dict(item), ensure_parent=False)

def read_simulator_dossier_full_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def list_simulator_dossier_full_reviews(data_root: Path) -> list[Path]:
    p = simulator_dossier_full_reviews_dir(data_root)
    return list_files(p, "*.json", reverse=True)

def get_latest_simulator_dossier_full_review(data_root: Path) -> Path | None:
    files = list_simulator_dossier_full_reviews(data_root)
    return files[0] if files else None

def simulator_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "dossiers": count_files(simulator_dossiers_dir(data_root), "*.json"),
        "evidence_files": count_files(simulator_dossier_evidence_dir(data_root), "*.jsonl"),
        "seals": count_files(simulator_acceptance_seals_dir(data_root), "*.json"),
        "blocker_rules": count_files(sandbox_runtime_admission_blocker_rules_dir(data_root), "*.jsonl"),
        "blocker_events": count_files(sandbox_runtime_admission_blocker_events_dir(data_root), "*.jsonl"),
        "audits": count_files(simulator_dossier_audit_dir(data_root), "*.jsonl"),
        "full_reviews": len(list_simulator_dossier_full_reviews(data_root))
    }
