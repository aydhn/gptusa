import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict

from usa_signal_bot.core.enums import SourceTrustLevel, ProviderQualityRiskFlag, DataQualityComponent
from usa_signal_bot.provider_quality.phase109_models import SourceTrustProfile, ProviderDataQualityScore, create_source_trust_profile_id

def source_trust_level_from_score(score: float, blocked: bool = False) -> SourceTrustLevel:
    if blocked:
        return SourceTrustLevel.BLOCKED
    if score >= 85:
        return SourceTrustLevel.HIGH_TRUST
    if score >= 60:
        return SourceTrustLevel.MEDIUM_TRUST
    if score >= 30:
        return SourceTrustLevel.LOW_TRUST
    return SourceTrustLevel.UNTRUSTED

def trust_score_from_quality_scores(scores: List[ProviderDataQualityScore]) -> float:
    if not scores:
        return 50.0 # Unknown

    total = sum(s.total_score for s in scores)
    return total / len(scores)

def build_source_trust_profile(provider_name: str, provider_kind: str = "MARKET_DATA", quality_scores: Optional[List[ProviderDataQualityScore]] = None) -> SourceTrustProfile:
    quality_scores = quality_scores or []

    risk_flags = []
    warnings = []
    errors = []

    trust_score = trust_score_from_quality_scores(quality_scores)
    blocked = any(s.blocked for s in quality_scores)
    scores_dict = defaultdict(list)
    for qs in quality_scores:
        for c in qs.components:
            scores_dict[c.component].append(c.score)

    def _avg(scores_list: List[float]) -> Optional[float]:
        return sum(scores_list) / len(scores_list) if scores_list else None

    schema_rel = _avg(scores_dict.get(DataQualityComponent.SCHEMA_VALIDITY, []))
    fresh_rel = _avg(scores_dict.get(DataQualityComponent.FRESHNESS, []))
    agree_rel = _avg(scores_dict.get(DataQualityComponent.SOURCE_AGREEMENT, []))
    cache_rel = _avg(scores_dict.get(DataQualityComponent.CACHE_RELIABILITY, []))
    safety_rel = _avg(scores_dict.get(DataQualityComponent.SAFETY_COMPLIANCE, []))


    if safety_rel is not None and safety_rel < 100:
        blocked = True
        warnings.append("Safety reliability is below 100, blocking trust.")

    trust_level = source_trust_level_from_score(trust_score, blocked)

    if trust_level in [SourceTrustLevel.LOW_TRUST, SourceTrustLevel.UNTRUSTED]:
        risk_flags.append(ProviderQualityRiskFlag.TRUST_SCORE_LOW)

    return SourceTrustProfile(
        profile_id=create_source_trust_profile_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        provider_kind=provider_kind,
        historical_score=None, # Only available if we read from history db
        schema_reliability_score=schema_rel,
        freshness_reliability_score=fresh_rel,
        agreement_reliability_score=agree_rel,
        cache_reliability_score=cache_rel,
        safety_reliability_score=safety_rel,
        trust_score=trust_score,
        trust_level=trust_level,
        default_use_case="RESEARCH_ONLY",
        warnings=warnings,
        errors=errors,
        risk_flags=risk_flags
    )

def source_trust_profile_summary(profile: SourceTrustProfile) -> Dict[str, Any]:
    return {
        "profile_id": profile.profile_id,
        "provider": profile.provider_name,
        "trust_score": profile.trust_score,
        "trust_level": profile.trust_level.value
    }

def source_trust_profile_to_text(profile: SourceTrustProfile) -> str:
    return f"Source Trust Profile: {profile.provider_name} | Score: {profile.trust_score:.1f} ({profile.trust_level.value})"
