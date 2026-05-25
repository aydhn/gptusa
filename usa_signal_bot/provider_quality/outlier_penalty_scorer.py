import datetime
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent, create_data_quality_component_id

def outlier_profile_grade(score: float) -> DataQualityGrade:
    if score >= 95:
        return DataQualityGrade.EXCELLENT
    if score >= 80:
        return DataQualityGrade.GOOD
    if score >= 60:
        return DataQualityGrade.ACCEPTABLE
    if score >= 40:
        return DataQualityGrade.WEAK
    return DataQualityGrade.POOR

def detect_basic_ohlcv_outliers(records: List[Dict[str, Any]]) -> List[str]:
    outliers = []
    for i, r in enumerate(records):
        try:
            op = float(r.get('open', 0))
            hi = float(r.get('high', 0))
            lo = float(r.get('low', 0))
            cl = float(r.get('close', 0))
            vol = float(r.get('volume', 0))

            if cl <= 0:
                outliers.append(f"Row {i}: close <= 0 ({cl})")
            if hi < lo:
                outliers.append(f"Row {i}: high < low ({hi} < {lo})")
            if op > hi or op < lo:
                outliers.append(f"Row {i}: open outside high/low range")
            if cl > hi or cl < lo:
                outliers.append(f"Row {i}: close outside high/low range")
            if vol < 0:
                outliers.append(f"Row {i}: volume < 0 ({vol})")
        except (ValueError, TypeError):
            pass # schema errors caught elsewhere
    return outliers

def outlier_score_from_count(outlier_count: int, row_count: int) -> float:
    if row_count == 0:
        return 100.0

    outlier_ratio = outlier_count / row_count
    # 5% outliers => score 0
    return max(0.0, 100.0 - (outlier_ratio * 2000.0))

def score_outlier_profile(records: List[Dict[str, Any]], provider_name: str = "UNKNOWN", symbol: Optional[str] = None) -> DataQualityScoreComponent:
    outliers = detect_basic_ohlcv_outliers(records)

    risk_flags = []
    warnings = []

    if outliers:
        warnings.append(f"Detected {len(outliers)} basic outliers (e.g. high < low, neg prices).")
        risk_flags.append(ProviderQualityRiskFlag.OUTLIER_RISK)

    score = outlier_score_from_count(len(outliers), len(records))
    grade = outlier_profile_grade(score)

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.OUTLIER_PROFILE,
        raw_value=float(len(outliers)),
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Outlier Profile scored {score:.1f} with {len(outliers)} detected basic outliers.",
        risk_flags=risk_flags,
        warnings=warnings
    )

def outlier_penalty_scorer_to_text(component: DataQualityScoreComponent) -> str:
    return f"Outlier Profile: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
