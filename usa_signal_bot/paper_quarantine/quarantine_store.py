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
from usa_signal_bot.paper_common.io import (
    ensure_dir, write_json, write_jsonl, read_json, list_files, count_files,
)

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

_ensure_dir = ensure_dir

def write_quarantined_candidate_json(path: Path, item: QuarantinedPaperCandidate) -> Path:
    return write_json(path, quarantined_paper_candidate_to_dict(item))

def write_promotion_ticket_json(path: Path, item: ReadOnlyPromotionTicket) -> Path:
    return write_json(path, read_only_promotion_ticket_to_dict(item))

def write_bridge_plan_json(path: Path, item: SupervisedDryRunBridgePlan) -> Path:
    return write_json(path, supervised_dry_run_bridge_plan_to_dict(item))

def write_paper_snapshot_ref_json(path: Path, item: PaperSnapshotRef) -> Path:
    return write_json(path, paper_snapshot_ref_to_dict(item))

def write_quarantine_audit_jsonl(path: Path, items: list[QuarantineAuditEntry]) -> Path:
    return write_jsonl(path, (quarantine_audit_entry_to_dict(i) for i in items), mode="a")

def write_quarantine_enrollment_review_json(path: Path, item: QuarantineEnrollmentReview) -> Path:
    return write_json(path, quarantine_enrollment_review_to_dict(item))

def read_quarantine_enrollment_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise QuarantineStorageError(f"Review file not found: {path}")
    return read_json(path)

def list_quarantine_enrollment_reviews(data_root: Path) -> list[Path]:
    return list_files(quarantine_reviews_dir(data_root), "*.json", reverse=True)

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
        summary[d.name] = count_files(d, "*.*")
    return summary
