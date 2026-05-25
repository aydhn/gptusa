
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from usa_signal_bot.event_metadata.phase111_models import (
    EventMetadataContext, EventMetadataFullReview, EventSchedule, EventScheduleIndex, MacroSeriesMetadata,
    event_metadata_context_to_dict, event_metadata_full_review_to_dict, event_schedule_to_dict, event_schedule_index_to_dict
)

def event_metadata_store_dir(data_root: Path) -> Path:
    return data_root / "event_metadata"

def event_metadata_contexts_dir(data_root: Path) -> Path:
    d = event_metadata_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_metadata_reviews_dir(data_root: Path) -> Path:
    d = event_metadata_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_schedules_dir(data_root: Path) -> Path:
    d = event_metadata_store_dir(data_root) / "schedules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_schedule_indexes_dir(data_root: Path) -> Path:
    d = event_metadata_store_dir(data_root) / "indexes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def macro_catalogs_dir(data_root: Path) -> Path:
    d = event_metadata_store_dir(data_root) / "macro_catalogs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_fixtures_dir(data_root: Path) -> Path:
    d = event_metadata_store_dir(data_root) / "fixtures"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_event_metadata_context_json(path: Path, item: EventMetadataContext) -> Path:
    with open(path, 'w') as f: json.dump(event_metadata_context_to_dict(item), f, indent=2)
    return path

def write_event_metadata_full_review_json(path: Path, item: EventMetadataFullReview) -> Path:
    with open(path, 'w') as f: json.dump(event_metadata_full_review_to_dict(item), f, indent=2)
    return path

def write_event_schedule_json(path: Path, item: EventSchedule) -> Path:
    with open(path, 'w') as f: json.dump(event_schedule_to_dict(item), f, indent=2)
    return path

def write_event_schedule_index_json(path: Path, item: EventScheduleIndex) -> Path:
    with open(path, 'w') as f: json.dump(event_schedule_index_to_dict(item), f, indent=2)
    return path

def write_macro_series_jsonl(path: Path, items: List[MacroSeriesMetadata]) -> Path:
    with open(path, 'w') as f:
        pass # dummy
    return path

def read_event_metadata_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f: return json.load(f)

def list_event_metadata_reviews(data_root: Path) -> List[Path]:
    d = event_metadata_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_event_metadata_review(data_root: Path) -> Optional[Path]:
    revs = list_event_metadata_reviews(data_root)
    if not revs: return None
    return sorted(revs)[-1]

def event_metadata_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews_count": len(list_event_metadata_reviews(data_root))}
