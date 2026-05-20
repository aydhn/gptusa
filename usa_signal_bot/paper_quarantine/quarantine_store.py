import json
from pathlib import Path
from typing import Any

from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
    PaperSnapshotRef,
    QuarantineAuditEntry,
    QuarantineEnrollmentReview,
    quarantined_paper_candidate_to_dict,
    read_only_promotion_ticket_to_dict,
    supervised_dry_run_bridge_plan_to_dict,
    paper_snapshot_ref_to_dict,
    quarantine_audit_entry_to_dict,
    quarantine_enrollment_review_to_dict,
)
from usa_signal_bot.core.exceptions import QuarantineStorageError

def quarantine_store_dir(data_root: Path) -> Path:
    return data_root / "paper_quarantine"

def quarantined_candidates_dir(data_root: Path) -> Path:
    return quarantine_store_dir(data_root) / "candidates"

def promotion_tickets_dir(data_root: Path) -> Path:
    return quarantine_store_dir(data_root) / "tickets"

def bridge_plans_dir(data_root: Path) -> Path:
    return quarantine_store_dir(data_root) / "bridge_plans"

def paper_snapshot_refs_dir(data_root: Path) -> Path:
    return quarantine_store_dir(data_root) / "paper_snapshot_refs"

def quarantine_audit_dir(data_root: Path) -> Path:
    return quarantine_store_dir(data_root) / "audit"

def quarantine_reviews_dir(data_root: Path) -> Path:
    return quarantine_store_dir(data_root) / "reviews"

def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def write_quarantined_candidate_json(path: Path, item: QuarantinedPaperCandidate) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(quarantined_paper_candidate_to_dict(item), f, indent=2)
    return path

def write_promotion_ticket_json(path: Path, item: ReadOnlyPromotionTicket) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(read_only_promotion_ticket_to_dict(item), f, indent=2)
    return path

def write_bridge_plan_json(path: Path, item: SupervisedDryRunBridgePlan) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(supervised_dry_run_bridge_plan_to_dict(item), f, indent=2)
    return path

def write_paper_snapshot_ref_json(path: Path, item: PaperSnapshotRef) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(paper_snapshot_ref_to_dict(item), f, indent=2)
    return path

def write_quarantine_audit_jsonl(path: Path, items: list[QuarantineAuditEntry]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(quarantine_audit_entry_to_dict(item)) + "\n")
    return path

def write_quarantine_enrollment_review_json(path: Path, item: QuarantineEnrollmentReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(quarantine_enrollment_review_to_dict(item), f, indent=2)
    return path

def read_quarantine_enrollment_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise QuarantineStorageError(f"Review file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def list_quarantine_enrollment_reviews(data_root: Path) -> list[Path]:
    d = quarantine_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")), reverse=True)

def get_latest_quarantine_enrollment_review(data_root: Path) -> Path | None:
    reviews = list_quarantine_enrollment_reviews(data_root)
    if not reviews:
        return None
    return reviews[0]

def quarantine_store_summary(data_root: Path) -> dict[str, Any]:
    dirs = [
        quarantined_candidates_dir(data_root),
        promotion_tickets_dir(data_root),
        bridge_plans_dir(data_root),
        paper_snapshot_refs_dir(data_root),
        quarantine_audit_dir(data_root),
        quarantine_reviews_dir(data_root)
    ]
    summary = {}
    for d in dirs:
        summary[d.name] = len(list(d.glob("*.*"))) if d.exists() else 0
    return summary
