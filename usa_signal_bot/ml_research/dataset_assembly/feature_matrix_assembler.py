import pandas as pd
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timezone
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLMatrixAssemblySpec,
    MLMatrixAssemblyResult,
    MLDatasetSourceReference,
    MLMatrixKind,
    MLAssemblyMode,
    MLDatasetAssemblyQuality,
    create_ml_matrix_assembly_spec_id,
    create_ml_matrix_assembly_result_id
)
import json

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_feature_matrix_assembly_spec(dataset_contract: Dict[str, Any], source_refs: List[MLDatasetSourceReference]) -> MLMatrixAssemblySpec:
    feature_config = dataset_contract.get("feature_matrix_config", {})
    return MLMatrixAssemblySpec(
        spec_id=create_ml_matrix_assembly_spec_id(),
        created_at_utc=_now(),
        matrix_kind=MLMatrixKind.FEATURE_MATRIX,
        assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT,
        source_refs=source_refs,
        required_columns=feature_config.get("required_columns", []),
        excluded_columns=feature_config.get("excluded_columns", []),
        join_keys=feature_config.get("join_keys", ["symbol", "timestamp"]),
        time_column=feature_config.get("time_column", "timestamp"),
        identifier_columns=feature_config.get("identifier_columns", ["symbol"])
    )

def select_feature_columns(df: pd.DataFrame, allowed_columns: List[str], excluded_columns: List[str]) -> pd.DataFrame:
    cols = [c for c in df.columns if c not in excluded_columns]
    if allowed_columns:
        cols = [c for c in cols if c in allowed_columns or c in ["symbol", "timestamp"]]
    return df[cols]

def assemble_feature_matrix_from_sources(spec: MLMatrixAssemblySpec) -> Tuple[pd.DataFrame, MLMatrixAssemblyResult]:
    result = MLMatrixAssemblyResult(
        result_id=create_ml_matrix_assembly_result_id(),
        created_at_utc=_now(),
        matrix_kind=MLMatrixKind.FEATURE_MATRIX,
        assembly_mode=spec.assembly_mode,
        row_count=0, column_count=0,
        source_ref_ids=[r.source_ref_id for r in spec.source_refs]
    )
    dfs = []
    for ref in spec.source_refs:
        if ref.source_path:
            try:
                df = pd.read_csv(ref.source_path)
                df = select_feature_columns(df, spec.required_columns, spec.excluded_columns)
                dfs.append(df)
            except Exception as e:
                result.errors.append(f"Failed to read source {ref.source_path}: {e}")
    if not dfs:
        return pd.DataFrame(), result
    try:
        merged = dfs[0]
        if len(dfs) > 1:
            for df in dfs[1:]:
                merged = pd.merge(merged, df, on=spec.join_keys, how="outer")
        result.row_count = len(merged)
        result.column_count = len(merged.columns)
        result.columns = list(merged.columns)
        result.identifier_columns = spec.identifier_columns
        result.time_column = spec.time_column
        result.missing_value_summary = merged.isnull().sum().to_dict()
        result.duplicate_row_count = int(merged.duplicated(subset=spec.join_keys).sum()) if spec.join_keys else 0
        errors = validate_feature_matrix(merged, spec)
        if not errors:
            result.assembly_valid = True
            result.quality = MLDatasetAssemblyQuality.ACCEPTABLE
        else:
            result.errors.extend(errors)
        return merged, result
    except Exception as e:
        result.errors.append(f"Failed to assemble matrix: {e}")
        return pd.DataFrame(), result

def validate_feature_matrix(df: pd.DataFrame, spec: MLMatrixAssemblySpec) -> List[str]:
    errors = []
    for jk in spec.join_keys:
        if jk not in df.columns:
            errors.append(f"Missing join key: {jk}")
    forbidden = ["buy", "sell", "order", "portfolio_weight", "target_weight", "allocation", "paper", "live_order"]
    for c in df.columns:
        if any(f in c.lower() for f in forbidden):
            if c.lower() == "macd_signal_9": continue
            errors.append(f"Forbidden column in feature matrix: {c}")
    return errors

def write_feature_matrix_csv(path: Path, df: pd.DataFrame, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists")
    df.to_csv(path, index=False)
    return path

def feature_matrix_summary(result: MLMatrixAssemblyResult) -> Dict[str, Any]:
    return {"result_id": result.result_id, "row_count": result.row_count, "column_count": result.column_count, "valid": result.assembly_valid, "errors": result.errors}

def feature_matrix_to_text(result: MLMatrixAssemblyResult, limit: int = 300) -> str:
    s = json.dumps(feature_matrix_summary(result), indent=2)
    return s[:limit] + "..." if len(s) > limit else s
