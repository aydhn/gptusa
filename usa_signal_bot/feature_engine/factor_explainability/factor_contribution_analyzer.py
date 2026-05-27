import datetime
from typing import Any
from collections import defaultdict

from usa_signal_bot.core.enums import AttributionDirection, FactorExplainabilityQuality
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    FeatureAttributionResult,
    FactorContributionProfile,
    create_factor_contribution_profile_id,
    validate_factor_contribution_profile
)

def top_positive_attributions(attributions: list[FeatureAttributionResult], limit: int = 5) -> list[dict[str, Any]]:
    positives = [a for a in attributions if a.attribution_direction == AttributionDirection.POSITIVE_CONTEXT]
    positives.sort(key=lambda x: x.attribution_score, reverse=True)
    return [{"feature": a.feature_column, "score": a.attribution_score} for a in positives[:limit]]

def top_negative_attributions(attributions: list[FeatureAttributionResult], limit: int = 5) -> list[dict[str, Any]]:
    negatives = [a for a in attributions if a.attribution_direction == AttributionDirection.NEGATIVE_CONTEXT]
    negatives.sort(key=lambda x: x.attribution_score, reverse=True)
    return [{"feature": a.feature_column, "score": a.attribution_score} for a in negatives[:limit]]

def build_factor_contribution_profile(symbol: str, factor_name: str, factor_column: str, attributions: list[FeatureAttributionResult]) -> FactorContributionProfile:
    # Filter for the specific factor
    factor_attrs = [a for a in attributions if a.factor_column == factor_column]

    top_pos = top_positive_attributions(factor_attrs)
    top_neg = top_negative_attributions(factor_attrs)

    neutral_attrs = [a for a in factor_attrs if a.attribution_direction in (AttributionDirection.NEUTRAL_CONTEXT, AttributionDirection.MIXED_CONTEXT)]
    neutral = [{"feature": a.feature_column, "score": a.attribution_score} for a in neutral_attrs[:5]]

    total_abs = sum(a.attribution_score for a in factor_attrs)

    profile = FactorContributionProfile(
        contribution_id=create_factor_contribution_profile_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        symbol=symbol,
        factor_name=factor_name,
        factor_column=factor_column,
        top_positive_features=top_pos,
        top_negative_features=top_neg,
        neutral_features=neutral,
        contribution_coverage_ratio=1.0 if factor_attrs else 0.0,
        total_abs_attribution=total_abs,
        attribution_count=len(factor_attrs),
        quality=FactorExplainabilityQuality.ACCEPTABLE,
        explanation_text=f"Contribution profile generated for factor {factor_name}.",
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_contribution_profile(profile)
    return profile

def build_factor_contribution_profiles(attributions: list[FeatureAttributionResult]) -> list[FactorContributionProfile]:
    grouped = defaultdict(list)
    for a in attributions:
        grouped[(a.symbol, a.factor_name, a.factor_column)].append(a)

    profiles = []
    for (symbol, fname, fcol), attrs in grouped.items():
        profiles.append(build_factor_contribution_profile(symbol, fname, fcol, attrs))
    return profiles

def validate_factor_contribution_profiles(profiles: list[FactorContributionProfile]) -> list[str]:
    errors = []
    for p in profiles:
        if p.produces_trade_signal:
            errors.append(f"Profile {p.contribution_id} produces trade signal")
    return errors

def factor_contribution_analyzer_summary(profiles: list[FactorContributionProfile]) -> dict[str, Any]:
    return {"profile_count": len(profiles)}

def factor_contribution_analyzer_to_text(profiles: list[FactorContributionProfile], limit: int = 200) -> str:
    return f"Created {len(profiles)} factor contribution profiles."
