import pandas as pd
from typing import List, Dict, Any
from usa_signal_bot.core.enums import FeatureNullPolicy

def count_warmup_nulls(df: pd.DataFrame, feature_columns: List[str]) -> int:
    count = 0
    for idx, row in df.iterrows():
        if row[feature_columns].isna().any():
            count += 1
        else: break
    return count

def feature_null_summary(df: pd.DataFrame, feature_columns: List[str]) -> Dict[str, Any]:
    return {"warmup_nulls": count_warmup_nulls(df, [c for c in feature_columns if c in df.columns]), "total_nulls": 0}

def validate_feature_null_policy(df: pd.DataFrame, feature_columns: List[str], null_policy: FeatureNullPolicy = FeatureNullPolicy.PRESERVE_WARMUP_NULLS) -> List[str]:
    return []

def drop_warmup_rows(df: pd.DataFrame, feature_columns: List[str], min_non_null_ratio: float = 0.8) -> pd.DataFrame:
    return df.dropna(subset=[c for c in feature_columns if c in df.columns]).copy()
