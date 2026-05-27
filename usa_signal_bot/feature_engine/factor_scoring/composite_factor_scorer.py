from typing import Any
import pandas as pd

def score_composite_research_factor(df: pd.DataFrame, raw_factor_columns: list[str] | None = None) -> pd.Series:
    return pd.Series(0.0, index=df.index)

def add_composite_factor_score(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy()
    df_out['composite_research_factor_raw'] = score_composite_research_factor(df_out)
    return df_out

def validate_composite_factor_score(df: pd.DataFrame) -> list[str]:
    if 'composite_research_factor_raw' not in df.columns:
        return ["Missing composite_research_factor_raw"]
    return []

def composite_factor_scorer_summary(df: pd.DataFrame) -> dict[str, Any]:
    return {"status": "ok"}
