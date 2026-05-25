import datetime
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent, create_data_quality_component_id

def completeness_grade(score: float) -> DataQualityGrade:
    if score >= 95:
        return DataQualityGrade.EXCELLENT
    if score >= 85:
        return DataQualityGrade.GOOD
    if score >= 70:
        return DataQualityGrade.ACCEPTABLE
    if score >= 50:
        return DataQualityGrade.WEAK
    return DataQualityGrade.POOR

def missing_value_rate(records: List[Dict[str, Any]], required_columns: List[str]) -> float:
    if not records:
        return 1.0
    total_expected = len(records) * len(required_columns)
    if total_expected == 0:
        return 0.0
    missing = 0
    for r in records:
        for c in required_columns:
            if c not in r or r[c] is None:
                missing += 1
    return missing / total_expected

def completeness_ratio(records: List[Dict[str, Any]], required_columns: List[str]) -> float:
    return 1.0 - missing_value_rate(records, required_columns)

def score_completeness(records: List[Dict[str, Any]], required_columns: Optional[List[str]] = None, provider_name: str = "UNKNOWN", symbol: Optional[str] = None) -> DataQualityScoreComponent:
    if required_columns is None:
        required_columns = ["open", "high", "low", "close", "volume"]

    risk_flags = []
    warnings = []

    if not records:
        ratio = 0.0
        warnings.append("Empty records list provided")
        risk_flags.append(ProviderQualityRiskFlag.COMPLETENESS_LOW)
    else:
        ratio = completeness_ratio(records, required_columns)
        if ratio < 0.8:
            warnings.append(f"High missing value rate: {1-ratio:.2%}")
            risk_flags.append(ProviderQualityRiskFlag.COMPLETENESS_LOW)

    score = ratio * 100.0
    grade = completeness_grade(score)

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.COMPLETENESS,
        raw_value=ratio,
        score=score,
        weight=0.0, # Will be set by aggregator
        weighted_score=0.0,
        grade=grade,
        explanation=f"Completeness is {score:.1f}% based on {len(records)} records.",
        risk_flags=risk_flags,
        warnings=warnings
    )

def completeness_scorer_to_text(component: DataQualityScoreComponent) -> str:
    return f"Completeness: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
