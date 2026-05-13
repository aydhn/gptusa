"""Corporate action storage."""
import json
from pathlib import Path
from typing import Any

from usa_signal_bot.corporate_actions.corporate_action_models import (
    CorporateActionEvent,
    CorporateActionGuardResult,
    CorporateActionReviewResult,
    AdjustedPriceValidationResult,
    corporate_action_event_to_dict,
    corporate_action_guard_result_to_dict,
    corporate_action_review_result_to_dict,
    adjusted_price_validation_result_to_dict
)
from usa_signal_bot.core.exceptions import CorporateActionStorageError

def corporate_action_store_dir(data_root: Path) -> Path:
    return data_root / "corporate_actions"

def corporate_action_events_dir(data_root: Path) -> Path:
    return corporate_action_store_dir(data_root) / "events"

def corporate_action_guards_dir(data_root: Path) -> Path:
    return corporate_action_store_dir(data_root) / "guards"

def corporate_action_reviews_dir(data_root: Path) -> Path:
    return corporate_action_store_dir(data_root) / "reviews"

def adjusted_validation_dir(data_root: Path) -> Path:
    return corporate_action_store_dir(data_root) / "adjusted_validation"

def write_corporate_action_events_jsonl(path: Path, events: list[CorporateActionEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(corporate_action_event_to_dict(e)) + "\n")
        return path
    except Exception as e:
        raise CorporateActionStorageError(f"Failed to write events to {path}: {e}")

def write_corporate_action_guard_result_json(path: Path, result: CorporateActionGuardResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(corporate_action_guard_result_to_dict(result), f, indent=4)
        return path
    except Exception as e:
        raise CorporateActionStorageError(f"Failed to write guard result to {path}: {e}")

def write_corporate_action_review_result_json(path: Path, result: CorporateActionReviewResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(corporate_action_review_result_to_dict(result), f, indent=4)
        return path
    except Exception as e:
        raise CorporateActionStorageError(f"Failed to write review result to {path}: {e}")

def write_adjusted_validation_result_json(path: Path, result: AdjustedPriceValidationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(adjusted_price_validation_result_to_dict(result), f, indent=4)
        return path
    except Exception as e:
        raise CorporateActionStorageError(f"Failed to write adjusted validation to {path}: {e}")

def read_corporate_action_review_result_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CorporateActionStorageError(f"Review file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise CorporateActionStorageError(f"Failed to read review result from {path}: {e}")

def list_corporate_action_reviews(data_root: Path) -> list[Path]:
    reviews_dir = corporate_action_reviews_dir(data_root)
    if not reviews_dir.exists():
        return []
    return sorted(list(reviews_dir.glob("*.json")))

def get_latest_corporate_action_review(data_root: Path) -> Path | None:
    files = list_corporate_action_reviews(data_root)
    return files[-1] if files else None

def corporate_action_store_summary(data_root: Path) -> dict[str, Any]:
    reviews = list_corporate_action_reviews(data_root)
    guards_dir = corporate_action_guards_dir(data_root)
    guards_count = len(list(guards_dir.glob("*.json"))) if guards_dir.exists() else 0
    adj_dir = adjusted_validation_dir(data_root)
    adj_count = len(list(adj_dir.glob("*.json"))) if adj_dir.exists() else 0

    return {
        "reviews_count": len(reviews),
        "latest_review": str(reviews[-1]) if reviews else None,
        "guards_count": guards_count,
        "adjusted_validations_count": adj_count
    }
