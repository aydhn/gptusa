from typing import List
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderDataQualityScore,
    SourceTrustProfile,
    ProviderSelectionScore,
    ProviderRanking
)
from usa_signal_bot.core.enums import ProviderQualityRiskFlag

def score_explanation_safety_check(text: str) -> List[str]:
    unsafe_terms = [
        "trade signal", "buy signal", "sell signal",
        "order", "execution", "paper mutation", "guarantee",
        "kesin al", "kesin sat", "garanti", "broker", "telegram send",
        "investment advice", "portfolio"
    ]
    errors = []
    text_lower = text.lower()
    for term in unsafe_terms:
        if term in text_lower:
            errors.append(f"Unsafe term detected in explanation: '{term}'")
    return errors

def explain_quality_score(score: ProviderDataQualityScore) -> str:
    parts = []
    parts.append(f"Data Quality Score for {score.provider_name} ({score.symbol}) is {score.total_score:.1f} ({score.grade.value}).")
    if score.blocked:
        parts.append("The provider is BLOCKED for data quality issues.")
    elif score.usable_for_research:
        parts.append("The provider data is deemed USABLE FOR RESEARCH.")
    else:
        parts.append("The provider data is NOT USABLE FOR RESEARCH without major caveats.")

    for comp in score.components:
        if comp.score < 50:
            parts.append(f"Weakness: {comp.component.value} scored {comp.score:.1f}. {comp.explanation}")

    explanation = " ".join(parts)
    errors = score_explanation_safety_check(explanation)
    if errors:
        return "Explanation blocked due to unsafe language."
    return explanation

def explain_source_trust(profile: SourceTrustProfile) -> str:
    parts = [f"Source Trust Profile for {profile.provider_name} indicates {profile.trust_level.value} with a score of {profile.trust_score:.1f}."]
    if profile.trust_level.value == "BLOCKED":
        parts.append("Source is blocked due to severe reliability or safety failures.")
    elif profile.trust_level.value == "UNTRUSTED":
        parts.append("Source is heavily untrusted and should generally be avoided.")

    explanation = " ".join(parts)
    errors = score_explanation_safety_check(explanation)
    if errors:
        return "Explanation blocked due to unsafe language."
    return explanation

def explain_provider_selection(score: ProviderSelectionScore) -> str:
    parts = [f"Provider Selection Score for {score.provider_name} is {score.final_selection_score:.1f} ({score.status.value})."]
    parts.append(f"Decision logic assigned: {score.decision.value}.")
    if score.blocked:
        parts.append("Selection is explicitly blocked.")

    explanation = " ".join(parts)
    errors = score_explanation_safety_check(explanation)
    if errors:
        return "Explanation blocked due to unsafe language."
    return explanation

def explain_provider_ranking(ranking: ProviderRanking) -> str:
    parts = [f"Provider Ranking for {ranking.symbol} is prepared strictly for research data sourcing."]
    if ranking.preferred_provider:
        parts.append(f"Preferred data source: {ranking.preferred_provider}.")
    if ranking.fallback_providers:
        parts.append(f"Available fallbacks: {', '.join(ranking.fallback_providers)}.")
    if ranking.blocked_providers:
        parts.append(f"Blocked sources: {', '.join(ranking.blocked_providers)}.")

    parts.append("Notice: This ranking does not produce trade signals or execution orders.")

    explanation = " ".join(parts)
    errors = score_explanation_safety_check(explanation)
    if errors:
        return "Explanation blocked due to unsafe language."
    return explanation
