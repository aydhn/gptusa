from typing import Any
import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureStabilityProfile,
    create_feature_stability_profile_id,
    validate_feature_stability_profile,
    _now_str
)

def compute_feature_stability_score(series: pd.Series) -> float:
    if len(series) < 10:
        return 0.0

    # Simple deterministic heuristic:
    # score = 100 * (non_missing_ratio) * (1 - (zero_count / total_valid_count))
    # Note: real stability would check variance, distinct count, distribution shifts.
    s = series.dropna()
    if len(s) == 0: return 0.0

    missing_penalty = len(s) / len(series)
    unique_ratio = len(s.unique()) / len(s)

    # If all values are identical, stability is low unless it's a known categorical flag
    if unique_ratio < 0.2 and len(s) > 5:
        base_score = 20.0
    else:
        base_score = 100.0

    score = base_score * missing_penalty
    return float(max(0.0, min(100.0, score)))

def compute_stability_scores(df: pd.DataFrame, columns: list[str]) -> dict[str, float]:
    scores = {}
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            scores[col] = compute_feature_stability_score(df[col])
        else:
            scores[col] = 0.0
    return scores

def low_stability_features(scores: dict[str, float], threshold: float = 40.0) -> list[str]:
    return [col for col, score in scores.items() if score < threshold]

def build_feature_stability_profile(symbol: str, df: pd.DataFrame, feature_columns: list[str] | None = None) -> FeatureStabilityProfile:
    cols_to_check = feature_columns if feature_columns is not None else [c for c in df.columns if c not in ('symbol', 'timestamp')]

    scores = compute_stability_scores(df, cols_to_check)
    low_stab = low_stability_features(scores)

    avg_score = sum(scores.values()) / len(scores) if scores else 0.0

    profile = FeatureStabilityProfile(
        stability_id=create_feature_stability_profile_id(),
        created_at_utc=_now_str(),
        symbol=symbol,
        feature_columns=cols_to_check,
        stability_scores=scores,
        low_stability_features=low_stab,
        average_stability_score=avg_score
    )
    validate_feature_stability_profile(profile)
    return profile

def feature_stability_summary(profiles: list[FeatureStabilityProfile]) -> dict[str, Any]:
    return {
        "profile_count": len(profiles),
        "symbols": [p.symbol for p in profiles],
        "avg_stability_by_symbol": {p.symbol: p.average_stability_score for p in profiles}
    }

def feature_stability_to_text(profiles: list[FeatureStabilityProfile], limit: int = 100) -> str:
    summary = feature_stability_summary(profiles)
    lines = [f"Feature Stability Profiles: {summary['profile_count']} symbols"]
    for p in profiles[:limit]:
        lines.append(f"  - {p.symbol}: Avg Score {p.average_stability_score:.1f}, {len(p.low_stability_features)} low stab features")
    return "\n".join(lines)
