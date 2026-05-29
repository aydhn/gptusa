import json
import pandas as pd
from pathlib import Path
from typing import Any
from usa_signal_bot.core.exceptions import RegimeLabelingStoreError
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelingContext,
    RegimeLabelingFullReview,
    RegimeLabelingSpec,
    HeuristicRegimeLabelResult,
    RollingRegimeWindowResult,
    RegimeLabelSequence,
    RegimeLabelStabilityProfile,
    RegimeCandidateValidationResult,
    RegimeLabelingReadinessGate,
    regime_labeling_context_to_dict,
    regime_labeling_full_review_to_dict,
    regime_labeling_spec_to_dict,
    heuristic_regime_label_result_to_dict,
    rolling_regime_window_result_to_dict,
    regime_label_sequence_to_dict,
    regime_label_stability_profile_to_dict,
    regime_candidate_validation_result_to_dict,
    regime_labeling_readiness_gate_to_dict
)

def regime_labeling_store_dir(data_root: Path) -> Path:
    d = data_root / "regime_classification" / "labeling"
    d.mkdir(parents=True, exist_ok=True)
    return d

def regime_labeling_contexts_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "contexts"
    d.mkdir(exist_ok=True)
    return d

def regime_labeling_reviews_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "reviews"
    d.mkdir(exist_ok=True)
    return d

def regime_labeling_specs_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "specs"
    d.mkdir(exist_ok=True)
    return d

def regime_label_results_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "label_results"
    d.mkdir(exist_ok=True)
    return d

def regime_window_results_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "window_results"
    d.mkdir(exist_ok=True)
    return d

def regime_label_sequences_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "sequences"
    d.mkdir(exist_ok=True)
    return d

def regime_stability_profiles_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "stability_profiles"
    d.mkdir(exist_ok=True)
    return d

def regime_candidate_validation_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "candidate_validation"
    d.mkdir(exist_ok=True)
    return d

def regime_labeling_gates_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "gates"
    d.mkdir(exist_ok=True)
    return d

def labeled_regime_tables_dir(data_root: Path) -> Path:
    d = regime_labeling_store_dir(data_root) / "labeled_tables"
    d.mkdir(exist_ok=True)
    return d

def write_regime_labeling_context_json(path: Path, item: RegimeLabelingContext) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(regime_labeling_context_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write context: {str(e)}")

def write_regime_labeling_full_review_json(path: Path, item: RegimeLabelingFullReview) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(regime_labeling_full_review_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write full review: {str(e)}")

def write_regime_labeling_specs_jsonl(path: Path, items: list[RegimeLabelingSpec]) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(regime_labeling_spec_to_dict(item)) + "\n")
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write specs: {str(e)}")

def write_heuristic_label_results_jsonl(path: Path, items: list[HeuristicRegimeLabelResult]) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(heuristic_regime_label_result_to_dict(item)) + "\n")
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write label results: {str(e)}")

def write_rolling_window_results_jsonl(path: Path, items: list[RollingRegimeWindowResult]) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(rolling_regime_window_result_to_dict(item)) + "\n")
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write window results: {str(e)}")

def write_regime_label_sequences_jsonl(path: Path, items: list[RegimeLabelSequence]) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(regime_label_sequence_to_dict(item)) + "\n")
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write sequences: {str(e)}")

def write_regime_stability_profiles_jsonl(path: Path, items: list[RegimeLabelStabilityProfile]) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(regime_label_stability_profile_to_dict(item)) + "\n")
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write stability profiles: {str(e)}")

def write_candidate_validation_result_json(path: Path, item: RegimeCandidateValidationResult) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(regime_candidate_validation_result_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write candidate validation: {str(e)}")

def write_regime_labeling_readiness_gate_json(path: Path, item: RegimeLabelingReadinessGate) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(regime_labeling_readiness_gate_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write readiness gate: {str(e)}")

def write_labeled_regime_table_csv(path: Path, df: pd.DataFrame, overwrite: bool = False) -> Path:
    try:
        if path.exists() and not overwrite:
            raise RegimeLabelingStoreError(f"Table {path} already exists and overwrite is False")
        df.to_csv(path, index=False)
        return path
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to write labeled table: {str(e)}")

def read_regime_labeling_full_review_json(path: Path) -> dict[str, Any]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise RegimeLabelingStoreError(f"Failed to read full review: {str(e)}")

def list_regime_labeling_reviews(data_root: Path) -> list[Path]:
    d = regime_labeling_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_regime_labeling_review(data_root: Path) -> Path | None:
    files = list_regime_labeling_reviews(data_root)
    if not files:
        return None
    return files[0]

def regime_labeling_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews": len(list_regime_labeling_reviews(data_root))
    }
