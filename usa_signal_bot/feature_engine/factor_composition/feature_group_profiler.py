from typing import Any
import pandas as pd

from usa_signal_bot.core.enums import FactorCompositionQuality
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureGroupDefinition,
    FeatureGroupProfile,
    create_feature_group_profile_id,
    _now_str
)

def compute_group_coverage_ratio(df: pd.DataFrame, columns: list[str]) -> float:
    if not columns or len(df) == 0:
        return 0.0
    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return 0.0
    # Average coverage of non-null values across these columns
    coverage = df[valid_cols].notna().mean().mean()
    return float(coverage)

def compute_group_average_missingness(df: pd.DataFrame, columns: list[str]) -> float:
    if not columns or len(df) == 0:
        return 1.0
    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return 1.0
    missingness = df[valid_cols].isna().mean().mean()
    return float(missingness)

def compute_group_quality(profile: FeatureGroupProfile) -> FactorCompositionQuality:
    if profile.coverage_ratio > 0.95 and profile.average_missingness < 0.05:
        return FactorCompositionQuality.HIGH
    if profile.coverage_ratio > 0.70 and profile.average_missingness < 0.30:
        return FactorCompositionQuality.ACCEPTABLE
    if profile.coverage_ratio > 0.40:
        return FactorCompositionQuality.WARNING
    return FactorCompositionQuality.LOW

def profile_feature_group(df: pd.DataFrame, group: FeatureGroupDefinition) -> FeatureGroupProfile:
    valid_cols = [c for c in group.feature_columns if c in df.columns]
    missing_cols = [c for c in group.feature_columns if c not in df.columns]

    coverage = compute_group_coverage_ratio(df, valid_cols)
    missingness = compute_group_average_missingness(df, valid_cols)

    profile = FeatureGroupProfile(
        profile_id=create_feature_group_profile_id(),
        created_at_utc=_now_str(),
        group_id=group.group_id,
        group_name=group.group_name,
        group_kind=group.group_kind,
        available_features=valid_cols,
        missing_features=missing_cols,
        coverage_ratio=coverage,
        average_missingness=missingness,
        average_stability_score=0.0, # Will be filled by stability analyzer later
        average_redundancy_score=0.0, # Will be filled by redundancy analyzer later
        average_confidence_score=0.0,
        selected_feature_count=0
    )

    profile.group_quality = compute_group_quality(profile)
    return profile

def profile_feature_groups(df: pd.DataFrame, groups: list[FeatureGroupDefinition]) -> list[FeatureGroupProfile]:
    return [profile_feature_group(df, group) for group in groups]

def feature_group_profiler_summary(profiles: list[FeatureGroupProfile]) -> dict[str, Any]:
    return {
        "profile_count": len(profiles),
        "group_qualities": {p.group_name: p.group_quality.value for p in profiles},
        "average_coverage": sum(p.coverage_ratio for p in profiles) / len(profiles) if profiles else 0.0
    }

def feature_group_profiler_to_text(profiles: list[FeatureGroupProfile], limit: int = 200) -> str:
    summary = feature_group_profiler_summary(profiles)
    lines = [
        f"Feature Group Profiles: {summary['profile_count']} groups",
        f"Average Coverage: {summary['average_coverage']:.2%}"
    ]
    for p in profiles[:limit]:
        lines.append(f"  - {p.group_name}: {p.group_quality.value} (Coverage: {p.coverage_ratio:.2%}, Missing: {p.average_missingness:.2%})")
    return "\n".join(lines)
