from typing import Any
import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureRedundancyProfile,
    create_feature_redundancy_profile_id,
    validate_feature_redundancy_profile,
    _now_str
)

def compute_feature_correlation_pairs(df: pd.DataFrame, columns: list[str], threshold: float = 0.95) -> list[dict[str, Any]]:
    valid_cols = [c for c in columns if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    if len(valid_cols) < 2:
        return []

    corr_matrix = df[valid_cols].corr(method='pearson')
    pairs = []

    for i in range(len(valid_cols)):
        for j in range(i + 1, len(valid_cols)):
            col1 = valid_cols[i]
            col2 = valid_cols[j]
            val = corr_matrix.iloc[i, j]
            if pd.notna(val) and abs(val) >= threshold:
                pairs.append({
                    "feature_1": col1,
                    "feature_2": col2,
                    "correlation": float(val),
                    "abs_correlation": float(abs(val))
                })
    return pairs

def compute_redundancy_score(high_redundancy_pairs: list[dict[str, Any]], feature_count: int) -> float:
    if feature_count < 2: return 0.0
    max_possible_pairs = (feature_count * (feature_count - 1)) / 2
    if max_possible_pairs == 0: return 0.0

    ratio = len(high_redundancy_pairs) / max_possible_pairs
    # Score is 0 if no redundancy, 100 if all redundant
    return float(min(100.0, ratio * 100.0))

def build_feature_redundancy_profile(symbol: str, df: pd.DataFrame, feature_columns: list[str] | None = None, correlation_threshold: float = 0.95) -> FeatureRedundancyProfile:
    cols_to_check = feature_columns if feature_columns is not None else [c for c in df.columns if c not in ('symbol', 'timestamp')]

    pairs = compute_feature_correlation_pairs(df, cols_to_check, correlation_threshold)
    score = compute_redundancy_score(pairs, len(cols_to_check))

    avg_abs_corr = None
    max_abs_corr = None
    if pairs:
        abs_corrs = [p["abs_correlation"] for p in pairs]
        avg_abs_corr = sum(abs_corrs) / len(abs_corrs)
        max_abs_corr = max(abs_corrs)

    profile = FeatureRedundancyProfile(
        redundancy_id=create_feature_redundancy_profile_id(),
        created_at_utc=_now_str(),
        symbol=symbol,
        feature_columns=cols_to_check,
        high_redundancy_pairs=pairs,
        average_abs_correlation=avg_abs_corr,
        max_abs_correlation=max_abs_corr,
        redundancy_score=score
    )
    validate_feature_redundancy_profile(profile)
    return profile

def feature_redundancy_summary(profiles: list[FeatureRedundancyProfile]) -> dict[str, Any]:
    return {
        "profile_count": len(profiles),
        "symbols": [p.symbol for p in profiles],
        "avg_redundancy_by_symbol": {p.symbol: p.redundancy_score for p in profiles}
    }

def feature_redundancy_to_text(profiles: list[FeatureRedundancyProfile], limit: int = 100) -> str:
    summary = feature_redundancy_summary(profiles)
    lines = [f"Feature Redundancy Profiles: {summary['profile_count']} symbols"]
    for p in profiles[:limit]:
        lines.append(f"  - {p.symbol}: Redundancy Score {p.redundancy_score:.1f}, {len(p.high_redundancy_pairs)} highly correlated pairs")
    return "\n".join(lines)
