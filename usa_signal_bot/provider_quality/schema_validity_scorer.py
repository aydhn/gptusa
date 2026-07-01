import datetime
from typing import List, Optional

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent, create_data_quality_component_id

def schema_validity_grade(score: float) -> DataQualityGrade:
    if score >= 99:
        return DataQualityGrade.EXCELLENT
    if score >= 80:
        return DataQualityGrade.ACCEPTABLE
    if score >= 50:
        return DataQualityGrade.WEAK
    if score > 0:
        return DataQualityGrade.POOR
    return DataQualityGrade.BLOCKED

def schema_validity_score_from_errors(errors: List[str]) -> float:
    if not errors:
        return 100.0
    # Even a single error is a significant penalty
    return max(0.0, 100.0 - (len(errors) * 20.0))

def score_schema_validity(schema_errors: List[str], provider_name: str = "UNKNOWN", symbol: Optional[str] = None) -> DataQualityScoreComponent:
    risk_flags = []
    warnings = []

    score = schema_validity_score_from_errors(schema_errors)

    if schema_errors:
        warnings.extend(schema_errors)
        risk_flags.append(ProviderQualityRiskFlag.SCHEMA_INVALID)

    grade = schema_validity_grade(score)

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.SCHEMA_VALIDITY,
        raw_value=float(len(schema_errors)),
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Schema validity is {score:.1f} with {len(schema_errors)} errors.",
        risk_flags=risk_flags,
        warnings=warnings
    )

def schema_validity_scorer_to_text(component: DataQualityScoreComponent) -> str:
    return f"Schema Validity: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
