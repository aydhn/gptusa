from pathlib import Path
from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json
from typing import Any
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
    return ensure_dir(data_root / "paper_no_order_dossier")

def no_order_dossiers_dir(data_root: Path) -> Path:
    return ensure_dir(no_order_dossier_store_dir(data_root) / "dossiers")

def no_order_evidence_dir(data_root: Path) -> Path:
    return ensure_dir(no_order_dossier_store_dir(data_root) / "evidence")

def bridge_replay_audit_seals_dir(data_root: Path) -> Path:
    return ensure_dir(no_order_dossier_store_dir(data_root) / "replay_audit_seals")

def admission_blocker_rules_dir(data_root: Path) -> Path:
    return ensure_dir(no_order_dossier_store_dir(data_root) / "admission_blocker_rules")

def admission_blocker_events_dir(data_root: Path) -> Path:
    return ensure_dir(no_order_dossier_store_dir(data_root) / "admission_blocker_events")

def no_order_dossier_audit_dir(data_root: Path) -> Path:
    return ensure_dir(no_order_dossier_store_dir(data_root) / "audit")

def no_order_dossier_full_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(no_order_dossier_store_dir(data_root) / "full_reviews")

def write_no_order_dossier_json(path: Path, item: NoOrderPaperSessionDossier) -> Path:
    return write_json(path, no_order_paper_session_dossier_to_dict(item), ensure_parent=False)

def write_no_order_evidence_jsonl(path: Path, items: list[NoOrderDossierEvidenceItem]) -> Path:
    return write_jsonl(path, (no_order_dossier_evidence_item_to_dict(item) for item in items), ensure_parent=False)

def write_bridge_replay_audit_seal_json(path: Path, item: BridgeReplayAuditSeal) -> Path:
    return write_json(path, bridge_replay_audit_seal_to_dict(item), ensure_parent=False)

def write_admission_blocker_rules_jsonl(path: Path, items: list[PaperAdmissionBlockerRule]) -> Path:
    return write_jsonl(path, (paper_admission_blocker_rule_to_dict(item) for item in items), ensure_parent=False)

def write_admission_blocker_events_jsonl(path: Path, items: list[PaperAdmissionBlockerEvent]) -> Path:
    return write_jsonl(path, (paper_admission_blocker_event_to_dict(item) for item in items), ensure_parent=False)

def write_no_order_dossier_audit_jsonl(path: Path, items: list[NoOrderDossierAuditEntry]) -> Path:
    return write_jsonl(path, (no_order_dossier_audit_entry_to_dict(item) for item in items), ensure_parent=False)

def write_no_order_dossier_full_review_json(path: Path, item: NoOrderDossierFullReview) -> Path:
    return write_json(path, no_order_dossier_full_review_to_dict(item), ensure_parent=False)

def read_no_order_dossier_full_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

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