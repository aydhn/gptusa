import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

def add_cross_sectional_zscore(tables: Dict[str, pd.DataFrame], column: str, output_column: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    if not output_column:
        output_column = f"cs_{column}_zscore"

    symbols = list(tables.keys())

    # We assume tables are perfectly aligned by row index (handled by alignment_engine beforehand)
    # i.e., index 0 corresponds to the same timestamp across all dfs.
    if len(symbols) < 2:
        return tables

    length = len(tables[symbols[0]])

    # Build cross sectional matrix
    matrix = np.zeros((length, len(symbols)))
    for i, sym in enumerate(symbols):
        if column in tables[sym].columns:
            matrix[:, i] = tables[sym][column].values
        else:
            matrix[:, i] = np.nan

    # Compute cross-sectional mean and std ignoring nans
    cs_mean = np.nanmean(matrix, axis=1, keepdims=True)
    cs_std = np.nanstd(matrix, axis=1, keepdims=True)

    cs_zscore = (matrix - cs_mean) / cs_std

    # Assign back
    for i, sym in enumerate(symbols):
        df = tables[sym].copy()
        df[output_column] = cs_zscore[:, i]
        tables[sym] = df

    return tables

def add_cross_sectional_percentile_rank(tables: Dict[str, pd.DataFrame], column: str, output_column: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    if not output_column:
        output_column = f"cs_{column}_percentile"

    symbols = list(tables.keys())
    if len(symbols) < 2:
        return tables

    length = len(tables[symbols[0]])

    matrix = np.zeros((length, len(symbols)))
    for i, sym in enumerate(symbols):
        if column in tables[sym].columns:
            matrix[:, i] = tables[sym][column].values
        else:
            matrix[:, i] = np.nan

    # Rank along axis 1 (cross-section)

    # Use pandas rank across rows for simplicity and NaN handling
    df_matrix = pd.DataFrame(matrix)
    rank_matrix = df_matrix.rank(axis=1, pct=True).values

    for i, sym in enumerate(symbols):
        df = tables[sym].copy()
        df[output_column] = rank_matrix[:, i]
        tables[sym] = df

    return tables

def add_cross_sectional_rank_features(tables: Dict[str, pd.DataFrame], columns: List[str]) -> Dict[str, pd.DataFrame]:
    for col in columns:
        tables = add_cross_sectional_zscore(tables, col)
        tables = add_cross_sectional_percentile_rank(tables, col)
    return tables

def validate_cross_sectional_features(tables: Dict[str, pd.DataFrame]) -> List[str]:
    errors = []
    for sym, df in tables.items():
        cs_cols = [c for c in df.columns if c.startswith('cs_')]
        if not cs_cols:
            errors.append(f'{sym} has no cross-sectional features.')
    return errors

def cross_sectional_features_summary(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    # just look at first table
    if not tables:
        return {}
    first_sym = list(tables.keys())[0]
    cols = [c for c in tables[first_sym].columns if c.startswith("cs_")]
    return {"cross_sectional_columns": cols}
