from typing import Any
import pandas as pd
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureCoverageProfile,
    create_feature_coverage_profile_id,
    validate_feature_coverage_profile,
    _now_str
)

def compute_feature_coverage_ratio(series: pd.Series) -> float:
    if len(series) == 0:
        return 0.0
    return float(series.notna().mean())

def low_coverage_features(df: pd.DataFrame, columns: list[str], threshold: float = 0.7) -> list[str]:
    low_cov = []
    for col in columns:
        if col in df.columns:
            if compute_feature_coverage_ratio(df[col]) < threshold:
                low_cov.append(col)
    return low_cov

def build_feature_coverage_profile(symbol: str, df: pd.DataFrame, feature_columns: list[str] | None = None) -> FeatureCoverageProfile:
    cols_to_check = feature_columns if feature_columns is not None else [c for c in df.columns if c not in ('symbol', 'timestamp')]

    valid_cols = [c for c in cols_to_check if c in df.columns]
    missing_cols = [c for c in cols_to_check if c not in df.columns]

    low_cov = low_coverage_features(df, valid_cols)
    avg_cov = df[valid_cols].notna().mean().mean() if valid_cols and len(df) > 0 else 0.0

    profile = FeatureCoverageProfile(
        coverage_id=create_feature_coverage_profile_id(),
        created_at_utc=_now_str(),
        symbol=symbol,
        feature_columns=cols_to_check,
        row_count=len(df),
        feature_count=len(cols_to_check),
        available_feature_count=len(valid_cols),
        missing_feature_count=len(missing_cols),
        average_coverage_ratio=float(avg_cov),
        low_coverage_features=low_cov
    )
    validate_feature_coverage_profile(profile)
    return profile

def feature_coverage_summary(profiles: list[FeatureCoverageProfile]) -> dict[str, Any]:
    return {
        "profile_count": len(profiles),
        "symbols": [p.symbol for p in profiles],
        "avg_coverage_by_symbol": {p.symbol: p.average_coverage_ratio for p in profiles}
    }

def feature_coverage_to_text(profiles: list[FeatureCoverageProfile], limit: int = 100) -> str:
    summary = feature_coverage_summary(profiles)
    lines = [f"Feature Coverage Profiles: {summary['profile_count']} symbols"]
    for p in profiles[:limit]:
        lines.append(f"  - {p.symbol}: Coverage {p.average_coverage_ratio:.2%}, {len(p.low_coverage_features)} low cov features")
    return "\n".join(lines)
