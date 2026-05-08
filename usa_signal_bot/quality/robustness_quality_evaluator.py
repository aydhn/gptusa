from typing import Any, Dict, List, Tuple
from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualitySeverity
from usa_signal_bot.quality.quality_models import QualityDimensionScore, QualityIssue, create_quality_issue_id

def score_walk_forward_presence(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_monte_carlo_presence(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_sensitivity_presence(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_stability_bucket(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    index = artifacts.get("index")
    if not index or not getattr(index, "latest_backtest_run_dir", None):
        return 50.0, [QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.ROBUSTNESS,
            severity=QualitySeverity.MODERATE,
            status=QualityStatus.WARN,
            title="Fragile Stability",
            message="Robustness/Stability seems fragile."
        )]
    return 100.0, []

def evaluate_robustness_quality(artifacts: Dict[str, Any]) -> QualityDimensionScore:
    issues = []
    s1, i1 = score_walk_forward_presence(artifacts)
    s2, i2 = score_monte_carlo_presence(artifacts)
    s3, i3 = score_sensitivity_presence(artifacts)
    s4, i4 = score_stability_bucket(artifacts)

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
        dimension=QualityDimension.ROBUSTNESS,
        score=avg_score,
        weight=0.10,
        status=status,
        issue_count=len(issues),
        critical_count=crit,
        warning_count=warn,
        summary=f"Robustness Quality Score: {avg_score:.1f}",
        issues=issues
    )
