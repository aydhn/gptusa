import datetime
from typing import Optional

from usa_signal_bot.core.enums import (
    DataQualityComponent,
    DataQualityGrade,
    ProviderQualityRiskFlag,
)
from usa_signal_bot.provider_quality.phase109_models import (
    DataQualityScoreComponent,
    create_data_quality_component_id,
)


def freshness_grade(score: float) -> DataQualityGrade:
    if score >= 90:
        return DataQualityGrade.EXCELLENT
    if score >= 75:
        return DataQualityGrade.GOOD
    if score >= 50:
        return DataQualityGrade.ACCEPTABLE
    if score >= 20:
        return DataQualityGrade.WEAK
    return DataQualityGrade.POOR


def freshness_score_from_age(
    age_seconds: Optional[int], ttl_seconds: Optional[int]
) -> float:
    if age_seconds is None or ttl_seconds is None or ttl_seconds <= 0:
        return 50.0  # Default unknown
    if age_seconds < 0:
        return 0.0  # Future time? Invalid.

    ratio = age_seconds / ttl_seconds
    if ratio <= 0.1:
        return 100.0
    if ratio <= 0.5:
        return 90.0 - ((ratio - 0.1) / 0.4) * 15.0  # 75 to 90
    if ratio <= 1.0:
        return 75.0 - ((ratio - 0.5) / 0.5) * 25.0  # 50 to 75
    if ratio <= 2.0:
        return 50.0 - ((ratio - 1.0) / 1.0) * 30.0  # 20 to 50
    return max(0.0, 20.0 - ((ratio - 2.0) / 3.0) * 20.0)  # 0 to 20


def _evaluate_freshness_status(
    fresh: bool,
    stale: bool,
    expired: bool,
    age_seconds: Optional[int],
    ttl_seconds: Optional[int],
) -> tuple[float, list[str], list[ProviderQualityRiskFlag]]:
    if expired:
        return 0.0, ["Data is expired"], [ProviderQualityRiskFlag.CACHE_RECORD_STALE]

    if stale:
        return 40.0, ["Data is stale"], [ProviderQualityRiskFlag.CACHE_RECORD_STALE]

    if fresh:
        return 100.0, [], []

    score = freshness_score_from_age(age_seconds, ttl_seconds)
    warnings = ["Data is relatively old"] if score < 50 else []
    return score, warnings, []


def score_freshness(
    fresh: bool,
    stale: bool,
    expired: bool = False,
    age_seconds: Optional[int] = None,
    ttl_seconds: Optional[int] = None,
    provider_name: str = "UNKNOWN",
    symbol: Optional[str] = None,
) -> DataQualityScoreComponent:
    score, warnings, risk_flags = _evaluate_freshness_status(
        fresh, stale, expired, age_seconds, ttl_seconds
    )

    grade = freshness_grade(score)

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.FRESHNESS,
        raw_value=float(age_seconds) if age_seconds is not None else None,
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Freshness scored {score:.1f} based on status (fresh={fresh}, stale={stale}, expired={expired})",
        risk_flags=risk_flags,
        warnings=warnings,
    )


def freshness_scorer_to_text(component: DataQualityScoreComponent) -> str:
    return f"Freshness: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
