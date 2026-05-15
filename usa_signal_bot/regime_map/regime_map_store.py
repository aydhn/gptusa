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
    p = data_root / "regime_map"
    p.mkdir(parents=True, exist_ok=True)
    return p

def timeframe_snapshots_dir(data_root: Path) -> Path:
    p = regime_map_store_dir(data_root) / "timeframe_snapshots"
    p.mkdir(exist_ok=True)
    return p

def confirmations_dir(data_root: Path) -> Path:
    p = regime_map_store_dir(data_root) / "confirmations"
    p.mkdir(exist_ok=True)
    return p

def cross_sectional_maps_dir(data_root: Path) -> Path:
    p = regime_map_store_dir(data_root) / "cross_sectional_maps"
    p.mkdir(exist_ok=True)
    return p

def alignments_dir(data_root: Path) -> Path:
    p = regime_map_store_dir(data_root) / "alignments"
    p.mkdir(exist_ok=True)
    return p

def transitions_dir(data_root: Path) -> Path:
    p = regime_map_store_dir(data_root) / "transitions"
    p.mkdir(exist_ok=True)
    return p

def regime_map_reviews_dir(data_root: Path) -> Path:
    p = regime_map_store_dir(data_root) / "reviews"
    p.mkdir(exist_ok=True)
    return p

def write_timeframe_regime_snapshot_json(path: Path, item: TimeframeRegimeSnapshot) -> Path:
    with open(path, "w") as f:
        json.dump(timeframe_regime_snapshot_to_dict(item), f, indent=2)
    return path

def write_multi_timeframe_confirmation_json(path: Path, item: MultiTimeframeRegimeConfirmation) -> Path:
    with open(path, "w") as f:
        json.dump(multi_timeframe_regime_confirmation_to_dict(item), f, indent=2)
    return path

def write_cross_sectional_regime_map_json(path: Path, item: CrossSectionalRegimeMap) -> Path:
    with open(path, "w") as f:
        json.dump(cross_sectional_regime_map_to_dict(item), f, indent=2)
    return path

def write_symbol_regime_alignment_json(path: Path, item: SymbolRegimeAlignment) -> Path:
    with open(path, "w") as f:
        json.dump(symbol_regime_alignment_to_dict(item), f, indent=2)
    return path

def write_regime_transition_signals_jsonl(path: Path, items: list[RegimeTransitionSignal]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(regime_transition_signal_to_dict(item)) + "\n")
    return path

def write_regime_map_review_json(path: Path, item: RegimeMapReview) -> Path:
    with open(path, "w") as f:
        json.dump(regime_map_review_to_dict(item), f, indent=2)
    return path

def read_regime_map_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
         return json.load(f)

def list_regime_map_reviews(data_root: Path) -> list[Path]:
    d = regime_map_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_regime_map_review(data_root: Path) -> Path | None:
    files = list_regime_map_reviews(data_root)
    if not files:
        return None
    return files[-1]

def regime_map_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "snapshots_dir": str(timeframe_snapshots_dir(data_root)),
        "confirmations_dir": str(confirmations_dir(data_root)),
        "maps_dir": str(cross_sectional_maps_dir(data_root)),
        "alignments_dir": str(alignments_dir(data_root)),
        "transitions_dir": str(transitions_dir(data_root)),
        "reviews_dir": str(regime_map_reviews_dir(data_root)),
        "review_count": len(list_regime_map_reviews(data_root))
    }
