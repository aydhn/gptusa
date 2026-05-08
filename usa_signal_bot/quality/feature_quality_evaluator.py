from typing import Any, Dict, List, Tuple
from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualitySeverity
from usa_signal_bot.quality.quality_models import QualityDimensionScore, QualityIssue, create_quality_issue_id

def score_feature_pipeline_outputs(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    index = artifacts.get("index")
    if not index or not getattr(index, "latest_scan_run_dir", None):
        return 0.0, [QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.FEATURE,
            severity=QualitySeverity.MODERATE,
            status=QualityStatus.WARN,
            title="Missing Feature Outputs",
            message="No recent scan directory found, cannot verify features."
        )]
    return 100.0, []

def score_feature_warning_rate(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_composite_feature_coverage(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def evaluate_feature_quality(artifacts: Dict[str, Any]) -> QualityDimensionScore:
    issues = []
    s1, i1 = score_feature_pipeline_outputs(artifacts)
    s2, i2 = score_feature_warning_rate(artifacts)
    s3, i3 = score_composite_feature_coverage(artifacts)

    issues.extend(i1 + i2 + i3)
    avg_score = (s1 + s2 + s3) / 3.0

    crit = sum(1 for i in issues if i.severity == QualitySeverity.CRITICAL)
    warn = sum(1 for i in issues if i.severity in [QualitySeverity.MODERATE, QualitySeverity.HIGH])

    status = QualityStatus.PASS
    if crit > 0:
        status = QualityStatus.FAIL
    elif warn > 0:
        status = QualityStatus.WARN

    return QualityDimensionScore(
        dimension=QualityDimension.FEATURE,
        score=avg_score,
        weight=0.08,
        status=status,
        issue_count=len(issues),
        critical_count=crit,
        warning_count=warn,
        summary=f"Feature Quality Score: {avg_score:.1f}",
        issues=issues
    )
