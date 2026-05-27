from typing import Any
from pathlib import Path
import json
import pandas as pd

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringContext,
    FactorScoringFullReview,
    FactorScoringSpec,
    FactorScoringResult,
    FactorTableResult,
    FactorDiagnosticsProfile,
    FactorComputationAudit,
    factor_scoring_context_to_dict,
    factor_scoring_full_review_to_dict,
    factor_scoring_spec_to_dict,
    factor_scoring_result_to_dict,
    factor_table_result_to_dict,
    factor_diagnostics_profile_to_dict,
    factor_computation_audit_to_dict
)

def factor_scoring_store_dir(data_root: Path) -> Path:
    return data_root / "feature_engine" / "factor_scoring"

def factor_scoring_contexts_dir(data_root: Path) -> Path:
    d = factor_scoring_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def factor_scoring_reviews_dir(data_root: Path) -> Path:
    d = factor_scoring_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def factor_scoring_specs_dir(data_root: Path) -> Path:
    d = factor_scoring_store_dir(data_root) / "specs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def factor_scoring_results_dir(data_root: Path) -> Path:
    d = factor_scoring_store_dir(data_root) / "results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def factor_tables_dir(data_root: Path) -> Path:
    d = factor_scoring_store_dir(data_root) / "factor_tables"
    d.mkdir(parents=True, exist_ok=True)
    return d

def factor_diagnostics_dir(data_root: Path) -> Path:
    d = factor_scoring_store_dir(data_root) / "diagnostics"
    d.mkdir(parents=True, exist_ok=True)
    return d

def factor_scoring_audits_dir(data_root: Path) -> Path:
    d = factor_scoring_store_dir(data_root) / "audits"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_factor_scoring_context_json(path: Path, item: FactorScoringContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(factor_scoring_context_to_dict(item), f, indent=2)
    return path

def write_factor_scoring_full_review_json(path: Path, item: FactorScoringFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(factor_scoring_full_review_to_dict(item), f, indent=2)
    return path

def write_factor_scoring_specs_jsonl(path: Path, items: list[FactorScoringSpec]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(factor_scoring_spec_to_dict(item)) + "\n")
    return path

def write_factor_scoring_results_jsonl(path: Path, items: list[FactorScoringResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(factor_scoring_result_to_dict(item)) + "\n")
    return path

def write_factor_table_result_json(path: Path, item: FactorTableResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(factor_table_result_to_dict(item), f, indent=2)
    return path

def write_factor_table_csv(path: Path, df: pd.DataFrame, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path

def write_factor_diagnostics_jsonl(path: Path, items: list[FactorDiagnosticsProfile]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(factor_diagnostics_profile_to_dict(item)) + "\n")
    return path

def write_factor_computation_audits_jsonl(path: Path, items: list[FactorComputationAudit]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(factor_computation_audit_to_dict(item)) + "\n")
    return path

def read_factor_scoring_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_factor_scoring_reviews(data_root: Path) -> list[Path]:
    return list(factor_scoring_reviews_dir(data_root).glob("*.json"))

def get_latest_factor_scoring_review(data_root: Path) -> Path | None:
    files = list_factor_scoring_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)

def factor_scoring_store_summary(data_root: Path) -> dict[str, Any]:
    return {"status": "ok"}
