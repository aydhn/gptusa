from pathlib import Path
from usa_signal_bot.paper_common.io import (ensure_dir, write_json, write_jsonl, read_json, list_files)
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
    return ensure_dir(data_root / "paper_mode_dry_admission_dossier")

def dry_admission_dossiers_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_dossier_store_dir(data_root) / "dossiers")

def dry_admission_dossier_evidence_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_dossier_store_dir(data_root) / "evidence")

def dry_admission_acceptance_seals_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_dossier_store_dir(data_root) / "acceptance_seals")

def rehearsal_blocker_rules_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_dossier_store_dir(data_root) / "rehearsal_blocker_rules")

def rehearsal_blocker_events_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_dossier_store_dir(data_root) / "rehearsal_blocker_events")

def dry_admission_dossier_audit_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_dossier_store_dir(data_root) / "audit")

def dry_admission_dossier_full_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_dossier_store_dir(data_root) / "full_reviews")

def write_dry_admission_dossier_json(path: Path, item: DryAdmissionGateDossier) -> Path:
    return write_json(path, dry_admission_gate_dossier_to_dict(item), ensure_parent=False)

def write_dry_admission_dossier_evidence_jsonl(path: Path, items: list[DryAdmissionDossierEvidenceItem]) -> Path:
    return write_jsonl(path, (dry_admission_dossier_evidence_item_to_dict(item) for item in items), ensure_parent=False)

def write_dry_admission_acceptance_seal_json(path: Path, item: DryAdmissionAcceptanceSeal) -> Path:
    return write_json(path, dry_admission_acceptance_seal_to_dict(item), ensure_parent=False)

def write_rehearsal_blocker_rules_jsonl(path: Path, items: list[PaperModeRehearsalBlockerRule]) -> Path:
    return write_jsonl(path, (rehearsal_blocker_rule_to_dict(item) for item in items), ensure_parent=False)

def write_rehearsal_blocker_events_jsonl(path: Path, items: list[PaperModeRehearsalBlockerEvent]) -> Path:
    return write_jsonl(path, (rehearsal_blocker_event_to_dict(item) for item in items), ensure_parent=False)

def write_dry_admission_dossier_audit_jsonl(path: Path, items: list[DryAdmissionDossierAuditEntry]) -> Path:
    return write_jsonl(path, (dry_admission_dossier_audit_entry_to_dict(item) for item in items), ensure_parent=False)

def write_dry_admission_dossier_full_review_json(path: Path, item: DryAdmissionDossierFullReview) -> Path:
    return write_json(path, dry_admission_dossier_full_review_to_dict(item), ensure_parent=False)

def read_dry_admission_dossier_full_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def list_dry_admission_dossier_full_reviews(data_root: Path) -> list[Path]:
    d = dry_admission_dossier_full_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_dry_admission_dossier_full_review(data_root: Path) -> Path | None:
    reviews = list_dry_admission_dossier_full_reviews(data_root)
    return reviews[0] if reviews else None

def dry_admission_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    try:
        reviews = list_dry_admission_dossier_full_reviews(data_root)
        dossiers = list_files(dry_admission_dossiers_dir(data_root), "*.json")
        seals = list_files(dry_admission_acceptance_seals_dir(data_root), "*.json")
        return {
            "reviews": len(reviews),
            "dossiers": len(dossiers),
            "seals": len(seals)
        }
    except Exception:
        return {"reviews": 0, "dossiers": 0, "seals": 0}
