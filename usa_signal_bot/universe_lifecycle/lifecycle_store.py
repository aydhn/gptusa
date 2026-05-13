from pathlib import Path
from typing import Any, List, Dict, Optional
import json

from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, SymbolAliasRecord, UniverseSnapshot, SymbolHistoryCheck,
    SurvivorshipBiasAssessment, UniverseLifecycleReviewResult,
    symbol_lifecycle_record_to_dict, symbol_alias_record_to_dict,
    universe_snapshot_to_dict, symbol_history_check_to_dict,
    survivorship_bias_assessment_to_dict, universe_lifecycle_review_result_to_dict
)

def lifecycle_store_dir(data_root: Path) -> Path:
    return data_root / "universe_lifecycle"

def lifecycle_registry_dir(data_root: Path) -> Path:
    return lifecycle_store_dir(data_root) / "registry"

def lifecycle_snapshots_dir(data_root: Path) -> Path:
    return lifecycle_store_dir(data_root) / "snapshots"

def lifecycle_reviews_dir(data_root: Path) -> Path:
    return lifecycle_store_dir(data_root) / "reviews"

def lifecycle_history_checks_dir(data_root: Path) -> Path:
    return lifecycle_store_dir(data_root) / "history_checks"

def lifecycle_assessments_dir(data_root: Path) -> Path:
    return lifecycle_store_dir(data_root) / "assessments"

def write_lifecycle_records_jsonl(path: Path, records: List[SymbolLifecycleRecord]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(symbol_lifecycle_record_to_dict(r)) + "\n")
    return path

def write_symbol_aliases_jsonl(path: Path, aliases: List[SymbolAliasRecord]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for a in aliases:
            f.write(json.dumps(symbol_alias_record_to_dict(a)) + "\n")
    return path

def write_universe_snapshot_json(path: Path, snapshot: UniverseSnapshot) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(universe_snapshot_to_dict(snapshot), f, indent=2)
    return path

def write_symbol_history_checks_jsonl(path: Path, checks: List[SymbolHistoryCheck]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for c in checks:
            f.write(json.dumps(symbol_history_check_to_dict(c)) + "\n")
    return path

def write_survivorship_assessment_json(path: Path, assessment: SurvivorshipBiasAssessment) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(survivorship_bias_assessment_to_dict(assessment), f, indent=2)
    return path

def write_universe_lifecycle_review_json(path: Path, result: UniverseLifecycleReviewResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(universe_lifecycle_review_result_to_dict(result), f, indent=2)
    return path

def read_universe_snapshot_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_universe_lifecycle_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_universe_lifecycle_reviews(data_root: Path) -> List[Path]:
    d = lifecycle_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")))

def get_latest_universe_lifecycle_review(data_root: Path) -> Optional[Path]:
    paths = list_universe_lifecycle_reviews(data_root)
    return paths[-1] if paths else None

def lifecycle_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_universe_lifecycle_reviews(data_root)),
        "snapshots": len(list(lifecycle_snapshots_dir(data_root).glob("*.json"))) if lifecycle_snapshots_dir(data_root).exists() else 0
    }
