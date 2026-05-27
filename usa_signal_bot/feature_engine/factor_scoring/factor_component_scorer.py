from typing import Any
import pandas as pd
import numpy as np

def score_component_mean(df: pd.DataFrame, columns: list[str], output_column: str) -> pd.Series:
    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return pd.Series(index=df.index, dtype=float)
    return df[valid_cols].mean(axis=1)

def score_component_weighted_mean(df: pd.DataFrame, columns: list[str], weights: dict[str, float] | None, output_column: str) -> pd.Series:
    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return pd.Series(index=df.index, dtype=float)

    if not weights:
        return score_component_mean(df, valid_cols, output_column)

    w = []
    for c in valid_cols:
        w.append(weights.get(c, 1.0))

    w_series = pd.Series(w, index=valid_cols)
    w_sum = w_series.sum()
    if w_sum == 0:
        return pd.Series(index=df.index, dtype=float)

    return (df[valid_cols] * w_series).sum(axis=1) / w_sum

def score_component_directional(df: pd.DataFrame, columns: list[str], directions: dict[str, float] | None = None) -> pd.Series:
    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return pd.Series(index=df.index, dtype=float)

    if not directions:
        return score_component_mean(df, valid_cols, "temp")

    res = pd.Series(0.0, index=df.index)
    for c in valid_cols:
        d = directions.get(c, 1.0)
        res += df[c] * d

    return res / len(valid_cols)

def validate_component_input_columns(df: pd.DataFrame, columns: list[str]) -> list[str]:
    missing = [c for c in columns if c not in df.columns]
    return [f"Missing component input: {c}" for c in missing]

def factor_component_scorer_summary(df: pd.DataFrame, columns: list[str]) -> dict[str, Any]:
    return {
        "input_columns": columns,
        "valid_columns": [c for c in columns if c in df.columns]
    }
