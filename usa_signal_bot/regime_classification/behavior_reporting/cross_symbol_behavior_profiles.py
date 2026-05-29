from typing import Any

from usa_signal_bot.core.enums import MarketBehaviorProfileKind
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorProfile

def build_cross_symbol_behavior_profile(profiles: list[MarketBehaviorProfile]) -> MarketBehaviorProfile:
    prof = MarketBehaviorProfile()
    prof.profile_name = "cross_symbol_behavior_profile"
    prof.profile_kind = MarketBehaviorProfileKind.CROSS_SYMBOL_BEHAVIOR
    prof.summary = "Cross-symbol regime behavior summary. Does not provide portfolio allocation or symbol ranking."

    dist = compute_cross_symbol_behavior_distribution(profiles)
    conc = compute_cross_symbol_behavior_concentration(profiles)

    prof.metric_snapshot = {
        "distribution": dist,
        "concentration": conc
    }
    return prof

def compute_cross_symbol_behavior_distribution(profiles: list[MarketBehaviorProfile]) -> dict[str, Any]:
    dist = {}
    for p in profiles:
        if p.dominant_regime_label:
            dist[p.dominant_regime_label] = dist.get(p.dominant_regime_label, 0) + 1
    return dist

def compute_cross_symbol_behavior_concentration(profiles: list[MarketBehaviorProfile]) -> float | None:
    dist = compute_cross_symbol_behavior_distribution(profiles)
    if not dist: return None
    total = sum(dist.values())
    max_val = max(dist.values())
    return max_val / total if total > 0 else 0.0

def validate_cross_symbol_behavior_profile(profile: MarketBehaviorProfile) -> list[str]:
    errs = []
    if not profile.research_metadata_only: errs.append("research_metadata_only must be true")
    if profile.produces_portfolio_weights: errs.append("produces_portfolio_weights must be false")
    if "ranking" in profile.summary.lower() and "does not provide" not in profile.summary.lower():
        errs.append("Invalid symbol ranking language.")
    if "allocation" in profile.summary.lower() and "does not provide" not in profile.summary.lower():
        errs.append("Invalid portfolio allocation language.")
    return errs

def cross_symbol_behavior_profiles_summary(profile: MarketBehaviorProfile) -> dict[str, Any]:
    return {"metrics": profile.metric_snapshot}

def cross_symbol_behavior_profiles_to_text(profile: MarketBehaviorProfile) -> str:
    return f"Cross Symbol Profile: {profile.summary}"
