from typing import Any, Dict, List, Tuple
from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualitySeverity
from usa_signal_bot.quality.quality_models import QualityDimensionScore, QualityIssue, create_quality_issue_id
from pathlib import Path
from usa_signal_bot.quality.artifact_collectors import QualityArtifactIndex

def score_data_cache_presence(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    issues = []
    has_cache = artifacts.get("data_root") is not None
    if not has_cache:
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.DATA,
            severity=QualitySeverity.MODERATE,
            status=QualityStatus.WARN,
            title="Missing Cache",
            message="No cache files found."
        ))
        return 0.0, issues
    return 100.0, issues

def score_universe_readiness(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_data_freshness(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_missing_data_warnings(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []


def score_calendar_alignment(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_corporate_action_guard(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def evaluate_data_quality(artifacts: Dict[str, Any]) -> QualityDimensionScore:
    issues = []
    s1, i1 = score_data_cache_presence(artifacts)
    s2, i2 = score_universe_readiness(artifacts)
    s3, i3 = score_data_freshness(artifacts)
    s4, i4 = score_missing_data_warnings(artifacts)

    issues.extend(i1 + i2 + i3 + i4)
    avg_score = (s1 + s2 + s3 + s4) / 4.0

    crit = sum(1 for i in issues if i.severity == QualitySeverity.CRITICAL)
    warn = sum(1 for i in issues if i.severity in [QualitySeverity.MODERATE, QualitySeverity.HIGH])

    status = QualityStatus.PASS
    if crit > 0:
        status = QualityStatus.FAIL
    elif warn > 0:
        status = QualityStatus.WARN

    return QualityDimensionScore(
        dimension=QualityDimension.DATA,
        score=avg_score,
        weight=0.10,
        status=status,
        issue_count=len(issues),
        critical_count=crit,
        warning_count=warn,
        summary=f"Data Quality Score: {avg_score:.1f}",
        issues=issues
    )
