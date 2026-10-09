from pathlib import Path
from typing import Any
from usa_signal_bot.paper_common.io import (
    ensure_dir, write_json, write_jsonl, read_json, list_files, count_files,
)

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    HumanReviewChecklistItem,
    ReviewerNote,
    ActivationStillDeniedRegistryEntry,
    ReadinessConfirmationAuditEntry,
    ReadinessConfirmationReview,
    readiness_confirmation_queue_item_to_dict,
    human_review_bundle_to_dict,
    human_review_checklist_item_to_dict,
    reviewer_note_to_dict,
    activation_still_denied_registry_entry_to_dict,
    readiness_confirmation_audit_entry_to_dict,
    readiness_confirmation_review_to_dict
)

def readiness_confirmation_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_readiness_confirmation")

def confirmation_queue_dir(data_root: Path) -> Path:
    return ensure_dir(readiness_confirmation_store_dir(data_root) / "queue")

def human_review_bundles_dir(data_root: Path) -> Path:
    return ensure_dir(readiness_confirmation_store_dir(data_root) / "human_review_bundles")

def review_checklists_dir(data_root: Path) -> Path:
    return ensure_dir(readiness_confirmation_store_dir(data_root) / "checklists")

def reviewer_notes_dir(data_root: Path) -> Path:
    return ensure_dir(readiness_confirmation_store_dir(data_root) / "reviewer_notes")

def activation_denied_registry_dir(data_root: Path) -> Path:
    return ensure_dir(readiness_confirmation_store_dir(data_root) / "activation_denied_registry")

def confirmation_audit_dir(data_root: Path) -> Path:
    return ensure_dir(readiness_confirmation_store_dir(data_root) / "audit")

def confirmation_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(readiness_confirmation_store_dir(data_root) / "reviews")

def write_confirmation_queue_item_json(path: Path, item: ReadinessConfirmationQueueItem) -> Path:
    data = readiness_confirmation_queue_item_to_dict(item)
    return write_json(path / f"{item.queue_item_id}.json", data, ensure_parent=False)

def write_human_review_bundle_json(path: Path, item: HumanReviewBundle) -> Path:
    data = human_review_bundle_to_dict(item)
    return write_json(path / f"{item.bundle_id}.json", data, ensure_parent=False)

def write_review_checklist_jsonl(path: Path, items: list[HumanReviewChecklistItem]) -> Path:
    return write_jsonl(path / "checklists.jsonl", (human_review_checklist_item_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_reviewer_notes_jsonl(path: Path, items: list[ReviewerNote]) -> Path:
    return write_jsonl(path / "reviewer_notes.jsonl", (reviewer_note_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_activation_denied_registry_entry_json(path: Path, item: ActivationStillDeniedRegistryEntry) -> Path:
    data = activation_still_denied_registry_entry_to_dict(item)
    return write_json(path / f"{item.registry_entry_id}.json", data, ensure_parent=False)

def write_confirmation_audit_jsonl(path: Path, items: list[ReadinessConfirmationAuditEntry]) -> Path:
    return write_jsonl(path / "audit_trail.jsonl", (readiness_confirmation_audit_entry_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_readiness_confirmation_review_json(path: Path, item: ReadinessConfirmationReview) -> Path:
    data = readiness_confirmation_review_to_dict(item)
    return write_json(path / f"{item.review_id}.json", data, ensure_parent=False)

def read_readiness_confirmation_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return read_json(path)

def list_readiness_confirmation_reviews(data_root: Path) -> list[Path]:
    d = confirmation_reviews_dir(data_root)
    return list_files(d, "*.json", sort=True)

def get_latest_readiness_confirmation_review(data_root: Path) -> Path | None:
    files = list_readiness_confirmation_reviews(data_root)
    if files:
        return files[-1]
    return None

def readiness_confirmation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "queues": count_files(confirmation_queue_dir(data_root), "*.json"),
        "bundles": count_files(human_review_bundles_dir(data_root), "*.json"),
        "registry": count_files(activation_denied_registry_dir(data_root), "*.json"),
        "reviews": len(list_readiness_confirmation_reviews(data_root))
    }
