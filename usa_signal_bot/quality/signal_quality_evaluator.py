from typing import Any, Dict, List, Tuple
from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualitySeverity
from usa_signal_bot.quality.quality_models import QualityDimensionScore, QualityIssue, create_quality_issue_id

def score_signal_count(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    index = artifacts.get("index")
    if not index or not getattr(index, "latest_scan_run_dir", None):
        return 0.0, [QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.SIGNAL,
            severity=QualitySeverity.CRITICAL,
            status=QualityStatus.FAIL,
            title="Missing Signals",
            message="No scan directory found."
        )]
    return 100.0, []

def score_candidate_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_signal_ranking_outputs(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_signal_risk_flags(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def evaluate_signal_quality(artifacts: Dict[str, Any]) -> QualityDimensionScore:
    issues = []
    s1, i1 = score_signal_count(artifacts)
    s2, i2 = score_candidate_quality(artifacts)
    s3, i3 = score_signal_ranking_outputs(artifacts)
    s4, i4 = score_signal_risk_flags(artifacts)

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
        dimension=QualityDimension.SIGNAL,
        score=avg_score,
        weight=0.10,
        status=status,
        issue_count=len(issues),
        critical_count=crit,
        warning_count=warn,
        summary=f"Signal Quality Score: {avg_score:.1f}",
        issues=issues
    )
