import json
from pathlib import Path
from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionGateDossier,
    DryAdmissionDossierEvidenceItem,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerRule,
    PaperModeRehearsalBlockerEvent,
    DryAdmissionDossierAuditEntry,
    DryAdmissionDossierFullReview,
    dry_admission_gate_dossier_to_dict,
    dry_admission_dossier_evidence_item_to_dict,
    dry_admission_acceptance_seal_to_dict,
    rehearsal_blocker_rule_to_dict,
    rehearsal_blocker_event_to_dict,
    dry_admission_dossier_audit_entry_to_dict,
    dry_admission_dossier_full_review_to_dict
)

def dry_admission_dossier_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_mode_dry_admission_dossier"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossiers_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "dossiers"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossier_evidence_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "evidence"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_acceptance_seals_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "acceptance_seals"
    d.mkdir(parents=True, exist_ok=True)
    return d

def rehearsal_blocker_rules_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "rehearsal_blocker_rules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def rehearsal_blocker_events_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "rehearsal_blocker_events"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossier_audit_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossier_full_reviews_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "full_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_dry_admission_dossier_json(path: Path, item: DryAdmissionGateDossier) -> Path:
    with open(path, "w") as f:
        json.dump(dry_admission_gate_dossier_to_dict(item), f, indent=2)
    return path

def write_dry_admission_dossier_evidence_jsonl(path: Path, items: list[DryAdmissionDossierEvidenceItem]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_admission_dossier_evidence_item_to_dict(item)) + "\n")
    return path

def write_dry_admission_acceptance_seal_json(path: Path, item: DryAdmissionAcceptanceSeal) -> Path:
    with open(path, "w") as f:
        json.dump(dry_admission_acceptance_seal_to_dict(item), f, indent=2)
    return path

def write_rehearsal_blocker_rules_jsonl(path: Path, items: list[PaperModeRehearsalBlockerRule]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(rehearsal_blocker_rule_to_dict(item)) + "\n")
    return path

def write_rehearsal_blocker_events_jsonl(path: Path, items: list[PaperModeRehearsalBlockerEvent]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(rehearsal_blocker_event_to_dict(item)) + "\n")
    return path

def write_dry_admission_dossier_audit_jsonl(path: Path, items: list[DryAdmissionDossierAuditEntry]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_admission_dossier_audit_entry_to_dict(item)) + "\n")
    return path

def write_dry_admission_dossier_full_review_json(path: Path, item: DryAdmissionDossierFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(dry_admission_dossier_full_review_to_dict(item), f, indent=2)
    return path

def read_dry_admission_dossier_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_dry_admission_dossier_full_reviews(data_root: Path) -> list[Path]:
    d = dry_admission_dossier_full_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_dry_admission_dossier_full_review(data_root: Path) -> Path | None:
    reviews = list_dry_admission_dossier_full_reviews(data_root)
    return reviews[0] if reviews else None

def dry_admission_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    try:
        reviews = list_dry_admission_dossier_full_reviews(data_root)
        dossiers = list(dry_admission_dossiers_dir(data_root).glob("*.json"))
        seals = list(dry_admission_acceptance_seals_dir(data_root).glob("*.json"))
        return {
            "reviews": len(reviews),
            "dossiers": len(dossiers),
            "seals": len(seals)
        }
    except Exception:
        return {"reviews": 0, "dossiers": 0, "seals": 0}
