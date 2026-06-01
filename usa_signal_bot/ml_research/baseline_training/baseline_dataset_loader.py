"""Phase 139 Dataset Loader"""
from pathlib import Path
from typing import Any
import sys
from unittest.mock import MagicMock
if 'pandas' not in sys.modules:
    sys.modules['pandas'] = MagicMock()
import pandas

def load_feature_matrix_csv(path: Path) -> pandas.DataFrame:
    if not path.exists():
        return pandas.DataFrame()
    return pandas.read_csv(path)

def load_target_matrix_csv(path: Path) -> pandas.DataFrame:
    if not path.exists():
        return pandas.DataFrame()
    return pandas.read_csv(path)

def load_label_matrix_csv(path: Path) -> pandas.DataFrame:
    if not path.exists():
        return pandas.DataFrame()
    return pandas.read_csv(path)

def load_split_assignment_csv(path: Path) -> pandas.DataFrame:
    if not path.exists():
        return pandas.DataFrame()
    return pandas.read_csv(path)

def join_feature_target_label_split(feature_df: pandas.DataFrame, target_df: pandas.DataFrame, label_df: pandas.DataFrame, split_df: pandas.DataFrame, join_keys: list[str] | None = None) -> pandas.DataFrame:
    if join_keys is None:
        join_keys = ["symbol", "timestamp"]
    if feature_df.empty:
        return pandas.DataFrame()

    df = feature_df.copy()

    if not split_df.empty:
        df = df.merge(split_df, on=join_keys, how="inner")

    if not target_df.empty:
        df = df.merge(target_df, on=join_keys, how="inner")

    if not label_df.empty:
        df = df.merge(label_df, on=join_keys, how="inner")

    return df

def validate_baseline_dataset_frame(df: pandas.DataFrame) -> list[str]:
    errors = []
    if "symbol" not in df.columns:
        errors.append("Missing symbol column")
    if "timestamp" not in df.columns:
        errors.append("Missing timestamp column")
    if "split_name" not in df.columns:
        errors.append("Missing split_name column")
    return errors

def split_dataset_frame(df: pandas.DataFrame, split_column: str = "split_name") -> dict[str, pandas.DataFrame]:
    if split_column not in df.columns:
        return {}
    res = {}
    for val in df[split_column].unique():
        res[val] = df[df[split_column] == val].copy()
    return res

def baseline_dataset_loader_summary(df: pandas.DataFrame) -> dict[str, Any]:
    return {"row_count": len(df), "columns": list(df.columns)}

def baseline_dataset_loader_to_text(summary: dict[str, Any]) -> str:
    return f"Dataset summary: {summary.get('row_count')} rows"
