import datetime
from typing import Optional

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent, create_data_quality_component_id

def source_agreement_grade(score: float) -> DataQualityGrade:
    if score >= 90:
        return DataQualityGrade.EXCELLENT
    if score >= 75:
        return DataQualityGrade.GOOD
    if score >= 50:
        return DataQualityGrade.ACCEPTABLE
    if score >= 30:
        return DataQualityGrade.WEAK
    return DataQualityGrade.POOR

def source_agreement_score_from_disagreement(disagreement_score: Optional[float]) -> float:
    if disagreement_score is None:
        return 50.0 # Neutral if missing

    # Assuming disagreement_score is a percentage (e.g., 2.5 means 2.5% diff)
    if disagreement_score <= 0.5:
        return 100.0
    if disagreement_score <= 1.0:
        return 90.0
    if disagreement_score <= 2.0:
        return 75.0
    if disagreement_score <= 5.0:
        return 50.0
    return max(0.0, 50.0 - (disagreement_score - 5.0) * 10.0)

def score_source_agreement(disagreement_score: Optional[float], status: Optional[str] = None, provider_name: str = "UNKNOWN", symbol: Optional[str] = None) -> DataQualityScoreComponent:
    risk_flags = []
    warnings = []

    if disagreement_score is None:
        warnings.append("No source comparison disagreement score available")
    elif disagreement_score > 5.0:
        warnings.append(f"High disagreement score: {disagreement_score}%")
        risk_flags.append(ProviderQualityRiskFlag.SOURCE_DISAGREEMENT_HIGH)

    score = source_agreement_score_from_disagreement(disagreement_score)
    grade = source_agreement_grade(score)

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.SOURCE_AGREEMENT,
        raw_value=disagreement_score,
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Source Agreement scored {score:.1f} based on {disagreement_score if disagreement_score is not None else 'unknown'}% disagreement.",
        risk_flags=risk_flags,
        warnings=warnings
    )

def source_disagreement_scorer_to_text(component: DataQualityScoreComponent) -> str:
    return f"Source Agreement: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
