from typing import Any
import pandas as pd

def compute_feature_missingness_ratio(series: pd.Series) -> float:
    if len(series) == 0:
        return 1.0
    return float(series.isna().mean())

def feature_missingness_by_column(df: pd.DataFrame, columns: list[str]) -> dict[str, float]:
    result = {}
    for col in columns:
        if col in df.columns:
            result[col] = compute_feature_missingness_ratio(df[col])
        else:
            result[col] = 1.0
    return result

def high_missingness_features(df: pd.DataFrame, columns: list[str], threshold: float = 0.3) -> list[str]:
    high_miss = []
    missing_dict = feature_missingness_by_column(df, columns)
    for col, ratio in missing_dict.items():
        if ratio > threshold:
            high_miss.append(col)
    return high_miss

def feature_missingness_summary(df: pd.DataFrame, columns: list[str]) -> dict[str, Any]:
    missing_dict = feature_missingness_by_column(df, columns)
    avg_miss = sum(missing_dict.values()) / len(missing_dict) if missing_dict else 1.0
    return {
        "columns_checked": len(columns),
        "average_missingness": avg_miss,
        "high_missing_count": len([v for v in missing_dict.values() if v > 0.3])
    }

def feature_missingness_to_text(summary: dict[str, Any]) -> str:
    lines = [
        f"Missingness Summary:",
        f"  Columns checked: {summary['columns_checked']}",
        f"  Average missingness: {summary['average_missingness']:.2%}",
        f"  High missing count (>30%): {summary['high_missing_count']}"
    ]
    return "\n".join(lines)
