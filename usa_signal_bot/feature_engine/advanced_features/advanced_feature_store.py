import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    AdvancedFeatureContext,
    AdvancedFeatureFullReview,
    AdvancedFeatureSpec,
    AdvancedFeatureComputationResult,
    AdvancedFeatureTableResult,
    AdvancedFeatureAudit,
    advanced_feature_context_to_dict,
    advanced_feature_full_review_to_dict,
    advanced_feature_spec_to_dict,
    advanced_feature_computation_result_to_dict,
    advanced_feature_table_result_to_dict,
    advanced_feature_audit_to_dict
)

def advanced_feature_store_dir(data_root: Path) -> Path:
    return data_root / "feature_engine" / "advanced_features"

def advanced_feature_contexts_dir(data_root: Path) -> Path:
    return advanced_feature_store_dir(data_root) / "contexts"

def advanced_feature_reviews_dir(data_root: Path) -> Path:
    return advanced_feature_store_dir(data_root) / "reviews"

def advanced_feature_specs_dir(data_root: Path) -> Path:
    return advanced_feature_store_dir(data_root) / "specs"

def advanced_feature_results_dir(data_root: Path) -> Path:
    return advanced_feature_store_dir(data_root) / "results"

def advanced_feature_tables_dir(data_root: Path) -> Path:
    return advanced_feature_store_dir(data_root) / "feature_tables"

def advanced_feature_audits_dir(data_root: Path) -> Path:
    return advanced_feature_store_dir(data_root) / "audits"

def cross_sectional_dir(data_root: Path) -> Path:
    return advanced_feature_store_dir(data_root) / "cross_sectional"

def write_advanced_feature_context_json(path: Path, item: AdvancedFeatureContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(advanced_feature_context_to_dict(item), f, indent=2)
    return path

def write_advanced_feature_full_review_json(path: Path, item: AdvancedFeatureFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(advanced_feature_full_review_to_dict(item), f, indent=2)
    return path

def write_advanced_feature_specs_jsonl(path: Path, items: List[AdvancedFeatureSpec]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(advanced_feature_spec_to_dict(it)) + "\n")
    return path

def write_advanced_feature_results_jsonl(path: Path, items: List[AdvancedFeatureComputationResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(advanced_feature_computation_result_to_dict(it)) + "\n")
    return path

def write_advanced_feature_table_result_json(path: Path, item: AdvancedFeatureTableResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(advanced_feature_table_result_to_dict(item), f, indent=2)
    return path

def write_advanced_feature_table_csv(path: Path, df: pd.DataFrame, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path

def write_advanced_feature_audits_jsonl(path: Path, items: List[AdvancedFeatureAudit]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(advanced_feature_audit_to_dict(it)) + "\n")
    return path

def read_advanced_feature_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_advanced_feature_reviews(data_root: Path) -> List[Path]:
    rev_dir = advanced_feature_reviews_dir(data_root)
    if not rev_dir.exists():
        return []
    return sorted(list(rev_dir.glob("*.json")))

def get_latest_advanced_feature_review(data_root: Path) -> Optional[Path]:
    files = list_advanced_feature_reviews(data_root)
    return files[-1] if files else None

def advanced_feature_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_advanced_feature_reviews(data_root)),
        "specs_dir_exists": advanced_feature_specs_dir(data_root).exists(),
        "tables_dir_exists": advanced_feature_tables_dir(data_root).exists()
    }
