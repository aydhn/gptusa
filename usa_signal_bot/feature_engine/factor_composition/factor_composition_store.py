import json
from pathlib import Path
from typing import Any
import os
import glob
import dataclasses

from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FactorCompositionContext, FactorCompositionFullReview, FeatureGroupDefinition,
    FactorCandidateDefinition, FactorCompositionSpec, FeatureSelectionMetadata,
    FactorReadinessGate, feature_group_definition_to_dict, factor_candidate_definition_to_dict,
    feature_selection_metadata_to_dict, factor_composition_spec_to_dict,
    factor_readiness_gate_to_dict, factor_composition_context_to_dict,
    factor_composition_full_review_to_dict
)

def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def factor_composition_store_dir(data_root: Path) -> Path:
    return _ensure_dir(data_root / "feature_engine" / "factor_composition")

def factor_composition_contexts_dir(data_root: Path) -> Path:
    return _ensure_dir(factor_composition_store_dir(data_root) / "contexts")

def factor_composition_reviews_dir(data_root: Path) -> Path:
    return _ensure_dir(factor_composition_store_dir(data_root) / "reviews")

def feature_groups_dir(data_root: Path) -> Path:
    return _ensure_dir(factor_composition_store_dir(data_root) / "feature_groups")

def factor_candidates_dir(data_root: Path) -> Path:
    return _ensure_dir(factor_composition_store_dir(data_root) / "factor_candidates")

def factor_composition_specs_dir(data_root: Path) -> Path:
    return _ensure_dir(factor_composition_store_dir(data_root) / "composition_specs")

def feature_selection_metadata_dir(data_root: Path) -> Path:
    return _ensure_dir(factor_composition_store_dir(data_root) / "selection_metadata")

def factor_readiness_gates_dir(data_root: Path) -> Path:
    return _ensure_dir(factor_composition_store_dir(data_root) / "readiness_gates")

def write_factor_composition_context_json(path: Path, item: FactorCompositionContext) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_composition_context_to_dict(item), f, indent=2)
    return path

def write_factor_composition_full_review_json(path: Path, item: FactorCompositionFullReview) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_composition_full_review_to_dict(item), f, indent=2)
    return path

def write_feature_groups_jsonl(path: Path, items: list[FeatureGroupDefinition]) -> Path:
    with open(path, 'w') as f:
        for item in items:
            f.write(json.dumps(feature_group_definition_to_dict(item)) + "\n")
    return path

def write_factor_candidates_jsonl(path: Path, items: list[FactorCandidateDefinition]) -> Path:
    with open(path, 'w') as f:
        for item in items:
            f.write(json.dumps(factor_candidate_definition_to_dict(item)) + "\n")
    return path

def write_factor_composition_spec_json(path: Path, item: FactorCompositionSpec) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_composition_spec_to_dict(item), f, indent=2)
    return path

def write_feature_selection_metadata_jsonl(path: Path, items: list[FeatureSelectionMetadata]) -> Path:
    with open(path, 'w') as f:
        for item in items:
            f.write(json.dumps(feature_selection_metadata_to_dict(item)) + "\n")
    return path

def write_factor_readiness_gate_json(path: Path, item: FactorReadinessGate) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_readiness_gate_to_dict(item), f, indent=2)
    return path

def read_factor_composition_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def list_factor_composition_reviews(data_root: Path) -> list[Path]:
    d = factor_composition_reviews_dir(data_root)
    files = glob.glob(os.path.join(d, "*.json"))
    return [Path(f) for f in files]

def get_latest_factor_composition_review(data_root: Path) -> Path | None:
    files = list_factor_composition_reviews(data_root)
    if not files: return None
    return max(files, key=os.path.getctime)

def factor_composition_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "context_count": len(glob.glob(os.path.join(factor_composition_contexts_dir(data_root), "*.json"))),
        "review_count": len(glob.glob(os.path.join(factor_composition_reviews_dir(data_root), "*.json"))),
        "feature_group_count": len(glob.glob(os.path.join(feature_groups_dir(data_root), "*.jsonl"))),
        "factor_candidate_count": len(glob.glob(os.path.join(factor_candidates_dir(data_root), "*.jsonl")))
    }
