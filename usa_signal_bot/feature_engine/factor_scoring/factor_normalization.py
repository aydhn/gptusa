from typing import Any
import pandas as pd
from datetime import datetime, timezone
import uuid

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringSpec,
    FactorNormalizationMethod,
    FactorNormalizationResult,
    create_factor_normalization_result_id
)

def factor_zscore(series: pd.Series) -> pd.Series:
    if series.empty or series.isna().all():
        return series
    mean = series.mean()
    std = series.std()
    if pd.isna(std) or std == 0:
        return pd.Series(0.0, index=series.index)
    return (series - mean) / std

def factor_robust_zscore(series: pd.Series) -> pd.Series:
    if series.empty or series.isna().all():
        return series
    median = series.median()
    mad = (series - median).abs().median()
    if pd.isna(mad) or mad == 0:
        return pd.Series(0.0, index=series.index)
    return (series - median) / (1.4826 * mad)

def factor_minmax(series: pd.Series) -> pd.Series:
    if series.empty or series.isna().all():
        return series
    min_val = series.min()
    max_val = series.max()
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series(0.5, index=series.index)
    return (series - min_val) / (max_val - min_val)

def factor_percentile_rank(series: pd.Series) -> pd.Series:
    if series.empty or series.isna().all():
        return series
    return series.rank(pct=True)

def normalize_factor_column(df: pd.DataFrame, input_column: str, output_column: str, method: FactorNormalizationMethod) -> tuple[pd.DataFrame, FactorNormalizationResult]:
    df_out = df.copy()
    if input_column not in df_out.columns:
        result = FactorNormalizationResult(
            normalization_id=create_factor_normalization_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            symbol=None,
            factor_name=input_column,
            method=method,
            input_column=input_column,
            output_column=output_column,
            row_count=len(df),
            null_count=len(df),
            finite_value_count=0,
            min_value=None,
            max_value=None,
            mean_value=None,
            std_value=None,
            warnings=[f"Column {input_column} not found"],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        return df_out, result

    series = df_out[input_column]
    if method == FactorNormalizationMethod.Z_SCORE:
        df_out[output_column] = factor_zscore(series)
    elif method == FactorNormalizationMethod.ROBUST_Z_SCORE:
        df_out[output_column] = factor_robust_zscore(series)
    elif method == FactorNormalizationMethod.PERCENTILE_RANK:
        df_out[output_column] = factor_percentile_rank(series)
    elif method == FactorNormalizationMethod.MIN_MAX:
        df_out[output_column] = factor_minmax(series)
    else:
        df_out[output_column] = series

    out_s = df_out[output_column]
    result = FactorNormalizationResult(
        normalization_id=create_factor_normalization_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=None,
        factor_name=input_column,
        method=method,
        input_column=input_column,
        output_column=output_column,
        row_count=len(out_s),
        null_count=int(out_s.isna().sum()),
        finite_value_count=int(out_s.notna().sum()),
        min_value=float(out_s.min()) if not out_s.isna().all() else None,
        max_value=float(out_s.max()) if not out_s.isna().all() else None,
        mean_value=float(out_s.mean()) if not out_s.isna().all() else None,
        std_value=float(out_s.std()) if not out_s.isna().all() else None,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    return df_out, result

def normalize_factor_columns(df: pd.DataFrame, specs: list[FactorScoringSpec]) -> tuple[pd.DataFrame, list[FactorNormalizationResult]]:
    df_out = df.copy()
    results = []
    for spec in specs:
        df_out, res1 = normalize_factor_column(df_out, spec.output_raw_column, spec.output_normalized_column, spec.normalization_method)
        results.append(res1)
        df_out, res2 = normalize_factor_column(df_out, spec.output_raw_column, spec.output_percentile_column, FactorNormalizationMethod.PERCENTILE_RANK)
        results.append(res2)
    return df_out, results

def validate_factor_normalization(df: pd.DataFrame, columns: list[str]) -> list[str]:
    return []

def factor_normalization_summary(results: list[FactorNormalizationResult]) -> dict[str, Any]:
    return {"status": "ok"}
