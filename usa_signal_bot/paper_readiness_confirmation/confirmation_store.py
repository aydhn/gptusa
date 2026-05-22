from pathlib import Path
from typing import Any
import json

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
    d = data_root / "paper_readiness_confirmation"
    d.mkdir(parents=True, exist_ok=True)
    return d

def confirmation_queue_dir(data_root: Path) -> Path:
    d = readiness_confirmation_store_dir(data_root) / "queue"
    d.mkdir(parents=True, exist_ok=True)
    return d

def human_review_bundles_dir(data_root: Path) -> Path:
    d = readiness_confirmation_store_dir(data_root) / "human_review_bundles"
    d.mkdir(parents=True, exist_ok=True)
    return d

def review_checklists_dir(data_root: Path) -> Path:
    d = readiness_confirmation_store_dir(data_root) / "checklists"
    d.mkdir(parents=True, exist_ok=True)
    return d

def reviewer_notes_dir(data_root: Path) -> Path:
    d = readiness_confirmation_store_dir(data_root) / "reviewer_notes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def activation_denied_registry_dir(data_root: Path) -> Path:
    d = readiness_confirmation_store_dir(data_root) / "activation_denied_registry"
    d.mkdir(parents=True, exist_ok=True)
    return d

def confirmation_audit_dir(data_root: Path) -> Path:
    d = readiness_confirmation_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def confirmation_reviews_dir(data_root: Path) -> Path:
    d = readiness_confirmation_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_confirmation_queue_item_json(path: Path, item: ReadinessConfirmationQueueItem) -> Path:
    data = readiness_confirmation_queue_item_to_dict(item)
    file_path = path / f"{item.queue_item_id}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    return file_path

def write_human_review_bundle_json(path: Path, item: HumanReviewBundle) -> Path:
    data = human_review_bundle_to_dict(item)
    file_path = path / f"{item.bundle_id}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    return file_path

def write_review_checklist_jsonl(path: Path, items: list[HumanReviewChecklistItem]) -> Path:
    file_path = path / "checklists.jsonl"
    with open(file_path, "a") as f:
        for item in items:
            f.write(json.dumps(human_review_checklist_item_to_dict(item)) + "\n")
    return file_path

def write_reviewer_notes_jsonl(path: Path, items: list[ReviewerNote]) -> Path:
    file_path = path / "reviewer_notes.jsonl"
    with open(file_path, "a") as f:
        for item in items:
            f.write(json.dumps(reviewer_note_to_dict(item)) + "\n")
    return file_path

def write_activation_denied_registry_entry_json(path: Path, item: ActivationStillDeniedRegistryEntry) -> Path:
    data = activation_still_denied_registry_entry_to_dict(item)
    file_path = path / f"{item.registry_entry_id}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    return file_path

def write_confirmation_audit_jsonl(path: Path, items: list[ReadinessConfirmationAuditEntry]) -> Path:
    file_path = path / "audit_trail.jsonl"
    with open(file_path, "a") as f:
        for item in items:
            f.write(json.dumps(readiness_confirmation_audit_entry_to_dict(item)) + "\n")
    return file_path

def write_readiness_confirmation_review_json(path: Path, item: ReadinessConfirmationReview) -> Path:
    data = readiness_confirmation_review_to_dict(item)
    file_path = path / f"{item.review_id}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    return file_path

def read_readiness_confirmation_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def list_readiness_confirmation_reviews(data_root: Path) -> list[Path]:
    d = confirmation_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_readiness_confirmation_review(data_root: Path) -> Path | None:
    files = list_readiness_confirmation_reviews(data_root)
    if files:
        return files[-1]
    return None

def readiness_confirmation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "queues": len(list(confirmation_queue_dir(data_root).glob("*.json"))),
        "bundles": len(list(human_review_bundles_dir(data_root).glob("*.json"))),
        "registry": len(list(activation_denied_registry_dir(data_root).glob("*.json"))),
        "reviews": len(list_readiness_confirmation_reviews(data_root))
    }
