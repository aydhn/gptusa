import datetime
from typing import Optional

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent, create_data_quality_component_id

def cache_reliability_grade(score: float) -> DataQualityGrade:
    if score >= 90:
        return DataQualityGrade.EXCELLENT
    if score >= 70:
        return DataQualityGrade.GOOD
    if score >= 50:
        return DataQualityGrade.ACCEPTABLE
    if score >= 30:
        return DataQualityGrade.WEAK
    return DataQualityGrade.POOR

def cache_reliability_score_from_status(status: Optional[str], checksum_present: bool, schema_valid: bool) -> float:
    score = 100.0

    if status in ["MISSING", "CACHE_MISS"]:
        score = 0.0
    elif status in ["CORRUPT"]:
        score = 0.0
    elif status in ["STALE"]:
        score -= 20.0

    if not checksum_present:
        score -= 10.0

    if not schema_valid:
        score -= 50.0

    return max(0.0, score)

def score_cache_reliability(cache_record_status: Optional[str], checksum_present: bool = False, schema_valid: bool = True, provider_name: str = "UNKNOWN", symbol: Optional[str] = None) -> DataQualityScoreComponent:
    risk_flags = []
    warnings = []

    if cache_record_status in ["MISSING", "CACHE_MISS", None]:
        warnings.append("Cache record is missing")
        risk_flags.append(ProviderQualityRiskFlag.PROVIDER_CACHE_MISSING)

    if not checksum_present:
        warnings.append("Cache record missing checksum")

    if not schema_valid:
        warnings.append("Cache schema is invalid")
        risk_flags.append(ProviderQualityRiskFlag.PROVIDER_CACHE_INVALID)

    score = cache_reliability_score_from_status(cache_record_status, checksum_present, schema_valid)
    grade = cache_reliability_grade(score)

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.CACHE_RELIABILITY,
        raw_value=None,
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Cache Reliability scored {score:.1f} based on status {cache_record_status}, checksum={checksum_present}, schema_valid={schema_valid}.",
        risk_flags=risk_flags,
        warnings=warnings
    )

def cache_reliability_scorer_to_text(component: DataQualityScoreComponent) -> str:
    return f"Cache Reliability: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
