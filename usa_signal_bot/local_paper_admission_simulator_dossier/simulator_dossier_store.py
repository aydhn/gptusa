import json
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
    p.mkdir(parents=True, exist_ok=True)
    return p

def simulator_dossiers_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "dossiers"
    p.mkdir(parents=True, exist_ok=True)
    return p

def simulator_dossier_evidence_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "evidence"
    p.mkdir(parents=True, exist_ok=True)
    return p

def simulator_acceptance_seals_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "acceptance_seals"
    p.mkdir(parents=True, exist_ok=True)
    return p

def sandbox_runtime_admission_blocker_rules_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "sandbox_runtime_admission_blocker_rules"
    p.mkdir(parents=True, exist_ok=True)
    return p

def sandbox_runtime_admission_blocker_events_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "sandbox_runtime_admission_blocker_events"
    p.mkdir(parents=True, exist_ok=True)
    return p

def simulator_dossier_audit_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "audit"
    p.mkdir(parents=True, exist_ok=True)
    return p

def simulator_dossier_full_reviews_dir(data_root: Path) -> Path:
    p = simulator_dossier_store_dir(data_root) / "full_reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_simulator_dossier_json(path: Path, item: LocalPaperAdmissionSimulatorGateDossier) -> Path:
    with open(path, "w") as f:
        json.dump(local_paper_admission_simulator_gate_dossier_to_dict(item), f, indent=2)
    return path

def write_simulator_dossier_evidence_jsonl(path: Path, items: list[SimulatorDossierEvidenceItem]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(simulator_dossier_evidence_item_to_dict(i)) + "\n")
    return path

def write_simulator_acceptance_seal_json(path: Path, item: SimulatorAcceptanceSeal) -> Path:
    with open(path, "w") as f:
        json.dump(simulator_acceptance_seal_to_dict(item), f, indent=2)
    return path

def write_sandbox_runtime_admission_blocker_rules_jsonl(path: Path, items: list[PaperSandboxRuntimeAdmissionBlockerRule]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(sandbox_runtime_admission_blocker_rule_to_dict(i)) + "\n")
    return path

def write_sandbox_runtime_admission_blocker_events_jsonl(path: Path, items: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(sandbox_runtime_admission_blocker_event_to_dict(i)) + "\n")
    return path

def write_simulator_dossier_audit_jsonl(path: Path, items: list[SimulatorDossierAuditEntry]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(simulator_dossier_audit_entry_to_dict(i)) + "\n")
    return path

def write_simulator_dossier_full_review_json(path: Path, item: SimulatorDossierFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(simulator_dossier_full_review_to_dict(item), f, indent=2)
    return path

def read_simulator_dossier_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_simulator_dossier_full_reviews(data_root: Path) -> list[Path]:
    p = simulator_dossier_full_reviews_dir(data_root)
    return sorted(list(p.glob("*.json")), reverse=True)

def get_latest_simulator_dossier_full_review(data_root: Path) -> Path | None:
    files = list_simulator_dossier_full_reviews(data_root)
    return files[0] if files else None

def simulator_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "dossiers": len(list(simulator_dossiers_dir(data_root).glob("*.json"))),
        "evidence_files": len(list(simulator_dossier_evidence_dir(data_root).glob("*.jsonl"))),
        "seals": len(list(simulator_acceptance_seals_dir(data_root).glob("*.json"))),
        "blocker_rules": len(list(sandbox_runtime_admission_blocker_rules_dir(data_root).glob("*.jsonl"))),
        "blocker_events": len(list(sandbox_runtime_admission_blocker_events_dir(data_root).glob("*.jsonl"))),
        "audits": len(list(simulator_dossier_audit_dir(data_root).glob("*.jsonl"))),
        "full_reviews": len(list_simulator_dossier_full_reviews(data_root))
    }
