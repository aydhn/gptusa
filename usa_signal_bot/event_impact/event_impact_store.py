
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.event_impact.phase112_models import (
    EventImpactContext, EventImpactFullReview, EventImpactTag,
    SymbolEventExposure, MacroRegimeMetadata, CalendarAwareValidationResult,
    event_impact_context_to_dict, event_impact_full_review_to_dict,
    event_impact_tag_to_dict, symbol_event_exposure_to_dict,
    macro_regime_metadata_to_dict, calendar_aware_validation_result_to_dict
)

def event_impact_store_dir(data_root: Path) -> Path: return data_root / "event_impact"
def event_impact_contexts_dir(data_root: Path) -> Path: return event_impact_store_dir(data_root) / "contexts"
def event_impact_reviews_dir(data_root: Path) -> Path: return event_impact_store_dir(data_root) / "reviews"
def impact_tags_dir(data_root: Path) -> Path: return event_impact_store_dir(data_root) / "impact_tags"
def symbol_exposures_dir(data_root: Path) -> Path: return event_impact_store_dir(data_root) / "symbol_exposures"
def macro_regimes_dir(data_root: Path) -> Path: return event_impact_store_dir(data_root) / "macro_regimes"
def calendar_validations_dir(data_root: Path) -> Path: return event_impact_store_dir(data_root) / "calendar_validations"

def _ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def write_event_impact_context_json(path: Path, item: EventImpactContext) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(event_impact_context_to_dict(item), f, indent=2)
    return path

def write_event_impact_full_review_json(path: Path, item: EventImpactFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(event_impact_full_review_to_dict(item), f, indent=2)
    return path

def _write_jsonl(path: Path, items: List[Any], to_dict_func):
    _ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        for i in items:
            f.write(json.dumps(to_dict_func(i)) + "\n")
    return path

def write_event_impact_tags_jsonl(path: Path, items: List[EventImpactTag]) -> Path: return _write_jsonl(path, items, event_impact_tag_to_dict)
def write_symbol_exposures_jsonl(path: Path, items: List[SymbolEventExposure]) -> Path: return _write_jsonl(path, items, symbol_event_exposure_to_dict)
def write_macro_regimes_jsonl(path: Path, items: List[MacroRegimeMetadata]) -> Path: return _write_jsonl(path, items, macro_regime_metadata_to_dict)
def write_calendar_validations_jsonl(path: Path, items: List[CalendarAwareValidationResult]) -> Path: return _write_jsonl(path, items, calendar_aware_validation_result_to_dict)

def read_event_impact_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_event_impact_reviews(data_root: Path) -> List[Path]:
    d = event_impact_reviews_dir(data_root)
    if not d.exists(): return []
    return sorted(list(d.glob("*.json")), reverse=True)

def get_latest_event_impact_review(data_root: Path) -> Optional[Path]:
    l = list_event_impact_reviews(data_root)
    return l[0] if l else None

def event_impact_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_event_impact_reviews(data_root))}
