from pathlib import Path
from typing import Any
import json
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderPaperSessionDossier,
    NoOrderDossierEvidenceItem,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerRule,
    PaperAdmissionBlockerEvent,
    NoOrderDossierAuditEntry,
    NoOrderDossierFullReview,
    no_order_paper_session_dossier_to_dict,
    no_order_dossier_evidence_item_to_dict,
    bridge_replay_audit_seal_to_dict,
    paper_admission_blocker_rule_to_dict,
    paper_admission_blocker_event_to_dict,
    no_order_dossier_audit_entry_to_dict,
    no_order_dossier_full_review_to_dict
)

def no_order_dossier_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_no_order_dossier"
    d.mkdir(parents=True, exist_ok=True)
    return d

def no_order_dossiers_dir(data_root: Path) -> Path:
    d = no_order_dossier_store_dir(data_root) / "dossiers"
    d.mkdir(exist_ok=True)
    return d

def no_order_evidence_dir(data_root: Path) -> Path:
    d = no_order_dossier_store_dir(data_root) / "evidence"
    d.mkdir(exist_ok=True)
    return d

def bridge_replay_audit_seals_dir(data_root: Path) -> Path:
    d = no_order_dossier_store_dir(data_root) / "replay_audit_seals"
    d.mkdir(exist_ok=True)
    return d

def admission_blocker_rules_dir(data_root: Path) -> Path:
    d = no_order_dossier_store_dir(data_root) / "admission_blocker_rules"
    d.mkdir(exist_ok=True)
    return d

def admission_blocker_events_dir(data_root: Path) -> Path:
    d = no_order_dossier_store_dir(data_root) / "admission_blocker_events"
    d.mkdir(exist_ok=True)
    return d

def no_order_dossier_audit_dir(data_root: Path) -> Path:
    d = no_order_dossier_store_dir(data_root) / "audit"
    d.mkdir(exist_ok=True)
    return d

def no_order_dossier_full_reviews_dir(data_root: Path) -> Path:
    d = no_order_dossier_store_dir(data_root) / "full_reviews"
    d.mkdir(exist_ok=True)
    return d

def write_no_order_dossier_json(path: Path, item: NoOrderPaperSessionDossier) -> Path:
    with open(path, "w") as f:
        json.dump(no_order_paper_session_dossier_to_dict(item), f, indent=2)
    return path

def write_no_order_evidence_jsonl(path: Path, items: list[NoOrderDossierEvidenceItem]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(no_order_dossier_evidence_item_to_dict(item)) + "\n")
    return path

def write_bridge_replay_audit_seal_json(path: Path, item: BridgeReplayAuditSeal) -> Path:
    with open(path, "w") as f:
        json.dump(bridge_replay_audit_seal_to_dict(item), f, indent=2)
    return path

def write_admission_blocker_rules_jsonl(path: Path, items: list[PaperAdmissionBlockerRule]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(paper_admission_blocker_rule_to_dict(item)) + "\n")
    return path

def write_admission_blocker_events_jsonl(path: Path, items: list[PaperAdmissionBlockerEvent]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(paper_admission_blocker_event_to_dict(item)) + "\n")
    return path

def write_no_order_dossier_audit_jsonl(path: Path, items: list[NoOrderDossierAuditEntry]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(no_order_dossier_audit_entry_to_dict(item)) + "\n")
    return path

def write_no_order_dossier_full_review_json(path: Path, item: NoOrderDossierFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(no_order_dossier_full_review_to_dict(item), f, indent=2)
    return path

def read_no_order_dossier_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_no_order_dossier_full_reviews(data_root: Path) -> list[Path]:
    d = no_order_dossier_full_reviews_dir(data_root)
    return sorted([f for f in d.glob("*.json")], key=lambda x: x.stat().st_mtime, reverse=True)

def get_latest_no_order_dossier_full_review(data_root: Path) -> Path | None:
    files = list_no_order_dossier_full_reviews(data_root)
    return files[0] if files else None

def no_order_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "dossiers_dir": str(no_order_dossiers_dir(data_root)),
        "full_reviews_count": len(list_no_order_dossier_full_reviews(data_root)),
        "latest_full_review": str(get_latest_no_order_dossier_full_review(data_root)) if get_latest_no_order_dossier_full_review(data_root) else None
    }


# --- Phase 92 ---
# Phase 92