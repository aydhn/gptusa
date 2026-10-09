import os
from pathlib import Path
from usa_signal_bot.paper_common.io import ensure_dir, list_files, count_files
from typing import Any, List, Optional
import json
from usa_signal_bot.paper_observation.observation_models import (
    ObservationWindow, CheckpointHistoryEntry, ObservationTelemetrySummary,
    ObservationScorecard, QuarantineExitReview, ObservationAuditEntry, ObservationReview
)
import dataclasses

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, set):
            return list(o)
        return super().default(o)

def observation_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_observation")

def observation_windows_dir(data_root: Path) -> Path:
    return ensure_dir(observation_store_dir(data_root) / "windows")

def checkpoint_history_dir(data_root: Path) -> Path:
    return ensure_dir(observation_store_dir(data_root) / "checkpoints")

def telemetry_summaries_dir(data_root: Path) -> Path:
    return ensure_dir(observation_store_dir(data_root) / "telemetry")

def observation_scorecards_dir(data_root: Path) -> Path:
    return ensure_dir(observation_store_dir(data_root) / "scorecards")

def exit_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(observation_store_dir(data_root) / "exit_reviews")

def observation_audit_dir(data_root: Path) -> Path:
    return ensure_dir(observation_store_dir(data_root) / "audit")

def observation_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(observation_store_dir(data_root) / "reviews")

def write_observation_window_json(path: Path, item: ObservationWindow) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_checkpoint_history_jsonl(path: Path, items: List[CheckpointHistoryEntry]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_observation_telemetry_summary_json(path: Path, item: ObservationTelemetrySummary) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_observation_scorecard_json(path: Path, item: ObservationScorecard) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_quarantine_exit_review_json(path: Path, item: QuarantineExitReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_observation_audit_jsonl(path: Path, items: List[ObservationAuditEntry]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_observation_review_json(path: Path, item: ObservationReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def read_observation_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_observation_reviews(data_root: Path) -> List[Path]:
    return list_files(observation_reviews_dir(data_root), "*.json")

def get_latest_observation_review(data_root: Path) -> Optional[Path]:
    files = list_observation_reviews(data_root)
    if not files:
        return None
    return sorted(files, key=os.path.getmtime)[-1]

def observation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews": len(list_observation_reviews(data_root)),
        "windows": count_files(observation_windows_dir(data_root), "*.json"),
        "exit_reviews": count_files(exit_reviews_dir(data_root), "*.json")
    }
