from pathlib import Path
from typing import Dict, Any, List
import json
from usa_signal_bot.advanced_transition.phase101_models import (
    AdvancedTransitionContext,
    AdvancedTransitionFullReview,
    ModuleInventoryRecord,
    RuntimeBoundaryManifest,
    advanced_transition_context_to_dict,
    advanced_transition_full_review_to_dict,
    module_inventory_record_to_dict,
    runtime_boundary_manifest_to_dict
)

def advanced_transition_store_dir(data_root: Path) -> Path:
    return data_root / "advanced_transition"

def advanced_transition_contexts_dir(data_root: Path) -> Path:
    return advanced_transition_store_dir(data_root) / "contexts"

def advanced_transition_reviews_dir(data_root: Path) -> Path:
    return advanced_transition_store_dir(data_root) / "reviews"

def advanced_transition_inventory_dir(data_root: Path) -> Path:
    return advanced_transition_store_dir(data_root) / "inventory"

def advanced_transition_boundaries_dir(data_root: Path) -> Path:
    return advanced_transition_store_dir(data_root) / "boundaries"

def write_advanced_transition_context_json(path: Path, item: AdvancedTransitionContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(advanced_transition_context_to_dict(item), f, indent=2)
    return path

def write_advanced_transition_full_review_json(path: Path, item: AdvancedTransitionFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(advanced_transition_full_review_to_dict(item), f, indent=2)
    return path

def write_module_inventory_jsonl(path: Path, items: List[ModuleInventoryRecord]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(module_inventory_record_to_dict(item)) + "\n")
    return path

def write_runtime_boundary_manifest_json(path: Path, item: RuntimeBoundaryManifest) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(runtime_boundary_manifest_to_dict(item), f, indent=2)
    return path

def read_advanced_transition_full_review_json(path: Path) -> Dict[str, Any]:
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def list_advanced_transition_reviews(data_root: Path) -> List[Path]:
    d = advanced_transition_reviews_dir(data_root)
    if d.exists():
        return list(d.glob("*.json"))
    return []

def get_latest_advanced_transition_review(data_root: Path) -> Path | None:
    files = list_advanced_transition_reviews(data_root)
    if not files:
        return None
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files[0]

def advanced_transition_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_advanced_transition_reviews(data_root))}
