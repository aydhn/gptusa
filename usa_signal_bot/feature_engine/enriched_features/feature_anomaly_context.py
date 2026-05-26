import pandas as pd
from typing import Any

def add_feature_anomaly_context(df: pd.DataFrame, calendar_payload: dict[str, Any] | None = None, symbol: str | None = None) -> pd.DataFrame:
    df = df.copy()
    df["feature_anomaly_penalty"] = compute_feature_anomaly_penalty(df)
    df["explained_unexplained_anomaly_ratio"] = compute_explained_vs_unexplained_anomaly_ratio(df)
    df["anomaly_context_score"] = pd.Series(100.0, index=df.index)
    return df

def compute_feature_anomaly_penalty(df: pd.DataFrame) -> pd.Series:
    return pd.Series(0.0, index=df.index)

def compute_explained_vs_unexplained_anomaly_ratio(df: pd.DataFrame) -> pd.Series:
    return pd.Series(0.0, index=df.index)

def validate_feature_anomaly_context(df: pd.DataFrame) -> list[str]:
    return []

def feature_anomaly_context_summary(df: pd.DataFrame) -> dict[str, Any]:
    return {"columns": list(df.columns)}
