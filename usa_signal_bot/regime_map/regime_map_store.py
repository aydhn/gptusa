import json
from pathlib import Path
from typing import Any
from usa_signal_bot.regime_map.regime_map_models import (
    TimeframeRegimeSnapshot,
    MultiTimeframeRegimeConfirmation,
    CrossSectionalRegimeMap,
    SymbolRegimeAlignment,
    RegimeTransitionSignal,
    RegimeMapReview,
    timeframe_regime_snapshot_to_dict,
    multi_timeframe_regime_confirmation_to_dict,
    cross_sectional_regime_map_to_dict,
    symbol_regime_alignment_to_dict,
    regime_transition_signal_to_dict,
    regime_map_review_to_dict
)

def regime_map_store_dir(data_root: Path) -> Path:
    d = data_root / "regime_map"
    d.mkdir(parents=True, exist_ok=True)
    return d

def timeframe_snapshots_dir(data_root: Path) -> Path:
    d = regime_map_store_dir(data_root) / "timeframe_snapshots"
    d.mkdir(exist_ok=True)
    return d

def confirmations_dir(data_root: Path) -> Path:
    d = regime_map_store_dir(data_root) / "confirmations"
    d.mkdir(exist_ok=True)
    return d

def cross_sectional_maps_dir(data_root: Path) -> Path:
    d = regime_map_store_dir(data_root) / "cross_sectional_maps"
    d.mkdir(exist_ok=True)
    return d

def alignments_dir(data_root: Path) -> Path:
    d = regime_map_store_dir(data_root) / "alignments"
    d.mkdir(exist_ok=True)
    return d

def transitions_dir(data_root: Path) -> Path:
    d = regime_map_store_dir(data_root) / "transitions"
    d.mkdir(exist_ok=True)
    return d

def regime_map_reviews_dir(data_root: Path) -> Path:
    d = regime_map_store_dir(data_root) / "reviews"
    d.mkdir(exist_ok=True)
    return d

def write_timeframe_regime_snapshot_json(path: Path, item: TimeframeRegimeSnapshot) -> Path:
    data = timeframe_regime_snapshot_to_dict(item)
    path.write_text(json.dumps(data, indent=2))
    return path

def write_multi_timeframe_confirmation_json(path: Path, item: MultiTimeframeRegimeConfirmation) -> Path:
    data = multi_timeframe_regime_confirmation_to_dict(item)
    path.write_text(json.dumps(data, indent=2))
    return path

def write_cross_sectional_regime_map_json(path: Path, item: CrossSectionalRegimeMap) -> Path:
    data = cross_sectional_regime_map_to_dict(item)
    path.write_text(json.dumps(data, indent=2))
    return path

def write_symbol_regime_alignment_json(path: Path, item: SymbolRegimeAlignment) -> Path:
    data = symbol_regime_alignment_to_dict(item)
    path.write_text(json.dumps(data, indent=2))
    return path

def write_regime_transition_signals_jsonl(path: Path, items: list[RegimeTransitionSignal]) -> Path:
    with path.open("a", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(regime_transition_signal_to_dict(item)) + "\n")
    return path

def write_regime_map_review_json(path: Path, item: RegimeMapReview) -> Path:
    data = regime_map_review_to_dict(item)
    path.write_text(json.dumps(data, indent=2))
    return path

def read_regime_map_review_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())

def list_regime_map_reviews(data_root: Path) -> list[Path]:
    d = regime_map_reviews_dir(data_root)
    return sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_regime_map_review(data_root: Path) -> Path | None:
    reviews = list_regime_map_reviews(data_root)
    return reviews[0] if reviews else None

def regime_map_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "snapshots": len(list(timeframe_snapshots_dir(data_root).glob("*.json"))),
        "confirmations": len(list(confirmations_dir(data_root).glob("*.json"))),
        "cross_sectional_maps": len(list(cross_sectional_maps_dir(data_root).glob("*.json"))),
        "alignments": len(list(alignments_dir(data_root).glob("*.json"))),
        "transitions": len(list(transitions_dir(data_root).glob("*.jsonl"))),
        "reviews": len(list(regime_map_reviews_dir(data_root).glob("*.json"))),
    }
