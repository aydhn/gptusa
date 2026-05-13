"""Calendar storage."""
import json
from pathlib import Path
from typing import Any

from usa_signal_bot.calendar.calendar_models import (
    MarketSession,
    TradingDayResult,
    SessionValidationResult,
    CalendarReviewResult,
    market_session_to_dict,
    trading_day_result_to_dict,
    session_validation_result_to_dict,
    calendar_review_result_to_dict
)
from usa_signal_bot.core.exceptions import CalendarStorageError

def calendar_store_dir(data_root: Path) -> Path:
    return data_root / "calendar"

def calendar_sessions_dir(data_root: Path) -> Path:
    return calendar_store_dir(data_root) / "sessions"

def calendar_reviews_dir(data_root: Path) -> Path:
    return calendar_store_dir(data_root) / "reviews"

def session_validations_dir(data_root: Path) -> Path:
    return calendar_store_dir(data_root) / "session_validations"

def write_market_sessions_jsonl(path: Path, sessions: list[MarketSession]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            for s in sessions:
                f.write(json.dumps(market_session_to_dict(s)) + "\n")
        return path
    except Exception as e:
        raise CalendarStorageError(f"Failed to write sessions to {path}: {e}")

def write_trading_day_results_jsonl(path: Path, results: list[TradingDayResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(trading_day_result_to_dict(r)) + "\n")
        return path
    except Exception as e:
        raise CalendarStorageError(f"Failed to write trading day results to {path}: {e}")

def write_session_validation_result_json(path: Path, result: SessionValidationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(session_validation_result_to_dict(result), f, indent=4)
        return path
    except Exception as e:
        raise CalendarStorageError(f"Failed to write session validation to {path}: {e}")

def write_calendar_review_result_json(path: Path, result: CalendarReviewResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(calendar_review_result_to_dict(result), f, indent=4)
        return path
    except Exception as e:
        raise CalendarStorageError(f"Failed to write calendar review to {path}: {e}")

def read_calendar_review_result_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CalendarStorageError(f"Calendar review file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise CalendarStorageError(f"Failed to read calendar review from {path}: {e}")

def list_calendar_reviews(data_root: Path) -> list[Path]:
    reviews_dir = calendar_reviews_dir(data_root)
    if not reviews_dir.exists():
        return []
    return sorted(list(reviews_dir.glob("*.json")))

def get_latest_calendar_review(data_root: Path) -> Path | None:
    files = list_calendar_reviews(data_root)
    return files[-1] if files else None

def calendar_store_summary(data_root: Path) -> dict[str, Any]:
    reviews = list_calendar_reviews(data_root)
    validations_dir = session_validations_dir(data_root)
    validations_count = len(list(validations_dir.glob("*.json"))) if validations_dir.exists() else 0
    sessions_dir = calendar_sessions_dir(data_root)
    sessions_count = len(list(sessions_dir.glob("*.jsonl"))) if sessions_dir.exists() else 0

    return {
        "reviews_count": len(reviews),
        "latest_review": str(reviews[-1]) if reviews else None,
        "validations_count": validations_count,
        "sessions_files_count": sessions_count
    }
