import pandas as pd
from typing import Any

def add_event_aware_features(df: pd.DataFrame, event_payload: dict[str, Any] | None = None, symbol: str | None = None) -> pd.DataFrame:
    df = df.copy()

    events = event_payload.get(symbol, []) if event_payload and symbol else []

    df["event_day_flag"] = compute_event_day_flag(df, events)

    windows = compute_event_window_flags(df, events, 5, 5)
    for col in windows.columns:
        df[col] = windows[col]

    df["event_importance_score"] = compute_event_importance_score(df, events)
    df["event_impact_confidence_score"] = compute_event_impact_confidence_score(df, events)

    # Placeholder for contexts
    df["earnings_context_flag"] = 0
    df["macro_context_flag"] = 0
    df["corporate_action_context_flag"] = 0
    df["news_metadata_context_flag"] = 0

    return df

def compute_event_day_flag(df: pd.DataFrame, events: list[dict[str, Any]]) -> pd.Series:
    # Minimal implementation for dry-run
    return pd.Series(0, index=df.index)

def compute_event_window_flags(df: pd.DataFrame, events: list[dict[str, Any]], pre_days: int = 5, post_days: int = 5) -> pd.DataFrame:
    res = pd.DataFrame(index=df.index)
    res["pre_event_1d_flag"] = 0
    res["pre_event_5d_flag"] = 0
    res["post_event_1d_flag"] = 0
    res["post_event_5d_flag"] = 0
    return res

def compute_event_importance_score(df: pd.DataFrame, events: list[dict[str, Any]]) -> pd.Series:
    return pd.Series(0.0, index=df.index)

def compute_event_impact_confidence_score(df: pd.DataFrame, events: list[dict[str, Any]]) -> pd.Series:
    return pd.Series(0.0, index=df.index)

def validate_event_aware_features(df: pd.DataFrame) -> list[str]:
    return []

def event_aware_features_summary(df: pd.DataFrame) -> dict[str, Any]:
    return {"columns": list(df.columns)}
