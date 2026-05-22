from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    ArchiveIntegrityReport,
    PrePaperGovernanceCheckpoint,
    FinalHandoffAuditEntry,
    FinalHandoffFullReview,
    final_handoff_review_to_dict,
    sealed_readiness_archive_manifest_to_dict,
    archive_integrity_report_to_dict,
    pre_paper_governance_checkpoint_to_dict,
    final_handoff_audit_entry_to_dict,
    final_handoff_full_review_to_dict
)

def final_handoff_store_dir(data_root: Path) -> Path: return data_root / "paper_final_handoff"
def handoff_reviews_dir(data_root: Path) -> Path: return final_handoff_store_dir(data_root) / "handoff_reviews"
def archive_manifests_dir(data_root: Path) -> Path: return final_handoff_store_dir(data_root) / "archive_manifests"
def archive_integrity_dir(data_root: Path) -> Path: return final_handoff_store_dir(data_root) / "archive_integrity"
def pre_paper_checkpoints_dir(data_root: Path) -> Path: return final_handoff_store_dir(data_root) / "pre_paper_checkpoints"
def final_handoff_audit_dir(data_root: Path) -> Path: return final_handoff_store_dir(data_root) / "audit"
def final_handoff_full_reviews_dir(data_root: Path) -> Path: return final_handoff_store_dir(data_root) / "full_reviews"

def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def write_final_handoff_review_json(path: Path, item: FinalHandoffReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(final_handoff_review_to_dict(item), f, indent=2)
    return path

def write_sealed_archive_manifest_json(path: Path, item: SealedReadinessArchiveManifest) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(sealed_readiness_archive_manifest_to_dict(item), f, indent=2)
    return path

def write_archive_integrity_report_json(path: Path, item: ArchiveIntegrityReport) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(archive_integrity_report_to_dict(item), f, indent=2)
    return path

def write_pre_paper_checkpoint_json(path: Path, item: PrePaperGovernanceCheckpoint) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(pre_paper_governance_checkpoint_to_dict(item), f, indent=2)
    return path

def write_final_handoff_audit_jsonl(path: Path, items: List[FinalHandoffAuditEntry]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "a") as f:
        for item in items: f.write(json.dumps(final_handoff_audit_entry_to_dict(item)) + "\n")
    return path

def write_final_handoff_full_review_json(path: Path, item: FinalHandoffFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(final_handoff_full_review_to_dict(item), f, indent=2)
    return path

def read_final_handoff_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f: return json.load(f)

def list_final_handoff_full_reviews(data_root: Path) -> List[Path]:
    d = final_handoff_full_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_final_handoff_full_review(data_root: Path) -> Optional[Path]:
    files = list_final_handoff_full_reviews(data_root)
    if not files: return None
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

def final_handoff_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"full_reviews_count": len(list_final_handoff_full_reviews(data_root))}
