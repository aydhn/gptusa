import datetime
from typing import Optional

from usa_signal_bot.core.enums import ProviderSelectionScoreStatus, ProviderRankingDecision, ProviderQualityRiskFlag, DataQualityComponent
from usa_signal_bot.provider_quality.phase109_models import ProviderSelectionScore, ProviderDataQualityScore, SourceTrustProfile, create_provider_selection_score_id

def final_provider_selection_score(quality_score: float, trust_score: float, freshness_score: float, safety_score: float, availability_score: float) -> float:
    # 40% quality, 25% trust, 15% freshness, 15% safety, 5% availability
    if safety_score < 100:
        return 0.0 # Strict safety block

    w_q = 0.40
    w_t = 0.25
    w_f = 0.15
    w_s = 0.15
    w_a = 0.05

    return (quality_score * w_q) + (trust_score * w_t) + (freshness_score * w_f) + (safety_score * w_s) + (availability_score * w_a)

def provider_selection_status_from_score(score: float, blocked: bool = False) -> ProviderSelectionScoreStatus:
    if blocked:
        return ProviderSelectionScoreStatus.BLOCKED
    if score >= 75:
        return ProviderSelectionScoreStatus.SELECTABLE_FOR_RESEARCH
    if score >= 50:
        return ProviderSelectionScoreStatus.USE_WITH_WARNING
    return ProviderSelectionScoreStatus.NOT_RECOMMENDED_FOR_DATA_USE

def provider_ranking_decision_from_score(score: float, blocked: bool = False) -> ProviderRankingDecision:
    if blocked:
        return ProviderRankingDecision.BLOCK
    if score >= 75:
        return ProviderRankingDecision.PREFER_FOR_RESEARCH_DATA
    if score >= 50:
        return ProviderRankingDecision.USE_AS_FALLBACK_DATA
    if score >= 30:
        return ProviderRankingDecision.USE_WITH_DATA_WARNING
    return ProviderRankingDecision.DO_NOT_USE_FOR_CURRENT_DATASET

def build_provider_selection_score(
    provider_name: str,
    symbol: Optional[str],
    capability: str,
    quality_score: Optional[ProviderDataQualityScore] = None,
    trust_profile: Optional[SourceTrustProfile] = None,
    freshness_score: Optional[float] = None,
    safety_score: Optional[float] = None,
    availability_score: Optional[float] = None
) -> ProviderSelectionScore:

    risk_flags = []
    warnings = []
    errors = []

    q_val = quality_score.total_score if quality_score else 50.0
    t_val = trust_profile.trust_score if trust_profile else 50.0

    # Try to extract freshness from quality score components if not provided
    if freshness_score is None and quality_score:
        for c in quality_score.components:
            if c.component == DataQualityComponent.FRESHNESS:
                freshness_score = c.score
                break
    f_val = freshness_score if freshness_score is not None else 50.0

    # Try to extract safety from quality score components if not provided
    if safety_score is None and quality_score:
        for c in quality_score.components:
            if c.component == DataQualityComponent.SAFETY_COMPLIANCE:
                safety_score = c.score
                break
    s_val = safety_score if safety_score is not None else 100.0

    a_val = availability_score if availability_score is not None else 100.0

    blocked = False
    if s_val < 100:
        blocked = True
        warnings.append("Safety score below 100 blocks selection.")
    if quality_score and quality_score.blocked:
        blocked = True
    if trust_profile and trust_profile.trust_level.value == "BLOCKED":
        blocked = True

    final_score = final_provider_selection_score(q_val, t_val, f_val, s_val, a_val)
    status = provider_selection_status_from_score(final_score, blocked)
    decision = provider_ranking_decision_from_score(final_score, blocked)

    if status in [ProviderSelectionScoreStatus.NOT_RECOMMENDED_FOR_DATA_USE, ProviderSelectionScoreStatus.BLOCKED]:
        risk_flags.append(ProviderQualityRiskFlag.PROVIDER_SELECTION_UNSAFE)

    return ProviderSelectionScore(
        selection_score_id=create_provider_selection_score_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        capability=capability,
        data_quality_score_id=quality_score.score_id if quality_score else None,
        trust_profile_id=trust_profile.profile_id if trust_profile else None,
        quality_score=q_val,
        trust_score=t_val,
        freshness_score=f_val,
        safety_score=s_val,
        availability_score=a_val,
        final_selection_score=final_score,
        status=status,
        decision=decision,
        rank=None, # Assigned by ranking engine
        selectable_for_research=not blocked and final_score >= 50,
        use_as_fallback=not blocked and final_score >= 30,
        blocked=blocked,
        explanation=f"Selection score {final_score:.1f} (Q:{q_val:.1f}, T:{t_val:.1f}, F:{f_val:.1f}, S:{s_val:.1f}, A:{a_val:.1f})",
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors
    )

def provider_selection_score_to_text(score: ProviderSelectionScore) -> str:
    return f"Provider Selection Score: {score.provider_name} | {score.final_selection_score:.1f} ({score.decision.value})"
