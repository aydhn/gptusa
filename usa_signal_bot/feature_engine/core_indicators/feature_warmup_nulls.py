import pandas as pd
from typing import Any
from usa_signal_bot.feature_engine.core_indicators.phase117_models import FeatureNullPolicy

def count_warmup_nulls(df: pd.DataFrame, feature_columns: list[str]) -> int:
    if not feature_columns or df.empty: return 0
    return df[feature_columns].isna().sum().sum()

def feature_null_summary(df: pd.DataFrame, feature_columns: list[str]) -> dict[str, Any]: return {}
def validate_feature_null_policy(df: pd.DataFrame, feature_columns: list[str], null_policy: FeatureNullPolicy = FeatureNullPolicy.PRESERVE_WARMUP_NULLS) -> list[str]: return []
def drop_warmup_rows(df: pd.DataFrame, feature_columns: list[str], min_non_null_ratio: float = 0.8) -> pd.DataFrame: return df.dropna(subset=feature_columns)
def feature_warmup_nulls_to_text(summary: dict[str, Any]) -> str: return ""
