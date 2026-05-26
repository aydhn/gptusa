from pathlib import Path
from typing import Any
import json
from usa_signal_bot.feature_engine.core_indicators.phase117_models import CoreIndicatorContext, CoreIndicatorFullReview, IndicatorComputationSpec, CoreIndicatorComputationResult, FeatureTableResult, FeatureComputationAudit
import pandas as pd

def core_indicator_store_dir(data_root: Path) -> Path: return data_root / "feature_engine" / "core_indicators"
def core_indicator_contexts_dir(data_root: Path) -> Path: return core_indicator_store_dir(data_root) / "contexts"
def core_indicator_reviews_dir(data_root: Path) -> Path: return core_indicator_store_dir(data_root) / "reviews"
def core_indicator_specs_dir(data_root: Path) -> Path: return core_indicator_store_dir(data_root) / "specs"
def core_feature_tables_dir(data_root: Path) -> Path: return core_indicator_store_dir(data_root) / "feature_tables"
def core_indicator_results_dir(data_root: Path) -> Path: return core_indicator_store_dir(data_root) / "results"
def core_indicator_audits_dir(data_root: Path) -> Path: return core_indicator_store_dir(data_root) / "audits"

def write_core_indicator_context_json(path: Path, item: CoreIndicatorContext) -> Path: return path
def write_core_indicator_full_review_json(path: Path, item: CoreIndicatorFullReview) -> Path: return path
def write_indicator_specs_jsonl(path: Path, items: list[IndicatorComputationSpec]) -> Path: return path
def write_core_indicator_results_jsonl(path: Path, items: list[CoreIndicatorComputationResult]) -> Path: return path
def write_feature_table_result_json(path: Path, item: FeatureTableResult) -> Path: return path
def write_feature_table_csv(path: Path, df: pd.DataFrame, overwrite: bool = False) -> Path:
    if not overwrite and path.exists(): return path
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
def write_feature_computation_audits_jsonl(path: Path, items: list[FeatureComputationAudit]) -> Path: return path
def read_core_indicator_full_review_json(path: Path) -> dict[str, Any]: return {}
def list_core_indicator_reviews(data_root: Path) -> list[Path]: return []
def get_latest_core_indicator_review(data_root: Path) -> Path | None: return None
def core_indicator_store_summary(data_root: Path) -> dict[str, Any]: return {}
