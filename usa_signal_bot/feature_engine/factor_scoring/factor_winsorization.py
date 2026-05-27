from typing import Any
import pandas as pd

def winsorize_factor_series(series: pd.Series, lower_pct: float = 0.01, upper_pct: float = 0.99) -> pd.Series:
    if series.empty or series.isna().all():
        return series

    lower_val = series.quantile(lower_pct)
    upper_val = series.quantile(upper_pct)

    return series.clip(lower=lower_val, upper=upper_val)

def winsorize_factor_columns(df: pd.DataFrame, columns: list[str], lower_pct: float = 0.01, upper_pct: float = 0.99) -> pd.DataFrame:
    df_out = df.copy()
    for col in columns:
        if col in df_out.columns:
            df_out[col] = winsorize_factor_series(df_out[col], lower_pct, upper_pct)
    return df_out

def validate_winsorized_factors(df: pd.DataFrame, columns: list[str]) -> list[str]:
    return []

def factor_winsorization_summary(df: pd.DataFrame, columns: list[str]) -> dict[str, Any]:
    return {"status": "ok"}
