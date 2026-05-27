from typing import Any
import pandas as pd
from usa_signal_bot.feature_engine.factor_scoring.factor_normalization import factor_zscore, factor_percentile_rank

def add_cross_sectional_factor_zscores(tables: dict[str, pd.DataFrame], factor_columns: list[str]) -> dict[str, pd.DataFrame]:
    if not tables or not factor_columns:
        return tables

    # Simple mock that doesn't actually align, for phase 121 placeholder
    # Real cross sectional requires outer joining by timestamp, computing, then returning
    res = {}
    for sym, df in tables.items():
        df_out = df.copy()
        for col in factor_columns:
            if col in df_out.columns:
                df_out[f"cs_{col}_zscore"] = factor_zscore(df_out[col])
        res[sym] = df_out
    return res

def add_cross_sectional_factor_percentiles(tables: dict[str, pd.DataFrame], factor_columns: list[str]) -> dict[str, pd.DataFrame]:
    if not tables or not factor_columns:
        return tables
    res = {}
    for sym, df in tables.items():
        df_out = df.copy()
        for col in factor_columns:
            if col in df_out.columns:
                df_out[f"cs_{col}_percentile"] = factor_percentile_rank(df_out[col])
        res[sym] = df_out
    return res

def add_cross_sectional_factor_ranks(tables: dict[str, pd.DataFrame], factor_columns: list[str]) -> dict[str, pd.DataFrame]:
    if not tables or not factor_columns:
        return tables
    res = {}
    for sym, df in tables.items():
        df_out = df.copy()
        for col in factor_columns:
            if col in df_out.columns:
                df_out[f"cs_{col}_rank"] = df_out[col].rank()
        res[sym] = df_out
    return res

def validate_cross_sectional_factor_outputs(tables: dict[str, pd.DataFrame]) -> list[str]:
    return []

def cross_sectional_factor_ranks_summary(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    return {"status": "ok"}
