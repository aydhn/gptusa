import os
from pathlib import Path
import json

FILES = {}

FILES["usa_signal_bot/paper_observation/observation_store.py"] = """\
from pathlib import Path
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
    p = data_root / "paper_observation"
    p.mkdir(parents=True, exist_ok=True)
    return p

def observation_windows_dir(data_root: Path) -> Path:
    p = observation_store_dir(data_root) / "windows"
    p.mkdir(parents=True, exist_ok=True)
    return p

def checkpoint_history_dir(data_root: Path) -> Path:
    p = observation_store_dir(data_root) / "checkpoints"
    p.mkdir(parents=True, exist_ok=True)
    return p

def telemetry_summaries_dir(data_root: Path) -> Path:
    p = observation_store_dir(data_root) / "telemetry"
    p.mkdir(parents=True, exist_ok=True)
    return p

def observation_scorecards_dir(data_root: Path) -> Path:
    p = observation_store_dir(data_root) / "scorecards"
    p.mkdir(parents=True, exist_ok=True)
    return p

def exit_reviews_dir(data_root: Path) -> Path:
    p = observation_store_dir(data_root) / "exit_reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def observation_audit_dir(data_root: Path) -> Path:
    p = observation_store_dir(data_root) / "audit"
    p.mkdir(parents=True, exist_ok=True)
    return p

def observation_reviews_dir(data_root: Path) -> Path:
    p = observation_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_observation_window_json(path: Path, item: ObservationWindow) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_checkpoint_history_jsonl(path: Path, items: List[CheckpointHistoryEntry]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\\n")
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
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\\n")
    return path

def write_observation_review_json(path: Path, item: ObservationReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def read_observation_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_observation_reviews(data_root: Path) -> List[Path]:
    p = observation_reviews_dir(data_root)
    return list(p.glob("*.json"))

def get_latest_observation_review(data_root: Path) -> Optional[Path]:
    files = list_observation_reviews(data_root)
    if not files:
        return None
    return sorted(files, key=os.path.getmtime)[-1]

def observation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews": len(list_observation_reviews(data_root)),
        "windows": len(list(observation_windows_dir(data_root).glob("*.json"))),
        "exit_reviews": len(list(exit_reviews_dir(data_root).glob("*.json")))
    }
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
