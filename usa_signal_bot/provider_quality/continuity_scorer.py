import datetime
from typing import List, Dict, Any, Optional
import pandas as pd

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent, create_data_quality_component_id

def continuity_grade(score: float) -> DataQualityGrade:
    if score >= 95:
        return DataQualityGrade.EXCELLENT
    if score >= 85:
        return DataQualityGrade.GOOD
    if score >= 70:
        return DataQualityGrade.ACCEPTABLE
    if score >= 50:
        return DataQualityGrade.WEAK
    return DataQualityGrade.POOR

def detect_timestamp_gaps(records: List[Dict[str, Any]], expected_interval: str = "1d") -> List[str]:
    if len(records) < 2:
        return []

    try:
        # Note: This is a basic heuristic. For a real bursa calendar, we'd need trading-calendar integration.
        # Here we just look for large gaps as warnings.
        df = pd.DataFrame(records)
        if 'timestamp' not in df.columns:
            return ["Missing 'timestamp' column"]

        df['dt'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('dt')
        diffs = df['dt'].diff().dt.days

        gaps = []
        if expected_interval == "1d":
            # Weekend is 2-3 days, so > 4 days is a suspicious gap
            large_gaps = diffs[diffs > 4]
            if not large_gaps.empty:
                gaps.append(f"Found {len(large_gaps)} large gaps (>4 days)")
        return gaps
    except Exception as e:
        return [f"Error calculating gaps: {e}"]

def continuity_score_from_gaps(gap_count: int, row_count: int) -> float:
    if row_count < 2:
        return 100.0 # Can't have gaps

    # 1 gap in 100 rows is bad.
    gap_ratio = gap_count / row_count
    score = max(0.0, 100.0 - (gap_ratio * 1000.0)) # 1% gaps = 10% penalty
    return score

def score_continuity(records: List[Dict[str, Any]], expected_interval: str = "1d", provider_name: str = "UNKNOWN", symbol: Optional[str] = None) -> DataQualityScoreComponent:
    gaps = detect_timestamp_gaps(records, expected_interval)

    risk_flags = []
    warnings = []

    if gaps:
        warnings.extend(gaps)
        risk_flags.append(ProviderQualityRiskFlag.CONTINUITY_GAP)

    score = continuity_score_from_gaps(len(gaps), len(records))
    grade = continuity_grade(score)

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.CONTINUITY,
        raw_value=float(len(gaps)),
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Continuity scored {score:.1f} with {len(gaps)} detected gap warnings.",
        risk_flags=risk_flags,
        warnings=warnings
    )

def continuity_scorer_to_text(component: DataQualityScoreComponent) -> str:
    return f"Continuity: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
