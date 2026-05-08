from typing import Any, Dict, List, Tuple
from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualitySeverity
from usa_signal_bot.quality.quality_models import QualityDimensionScore, QualityIssue, create_quality_issue_id

def score_backtest_presence(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    index = artifacts.get("index")
    if not index or not getattr(index, "latest_backtest_run_dir", None):
        return 0.0, [QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.BACKTEST,
            severity=QualitySeverity.MODERATE,
            status=QualityStatus.WARN,
            title="Missing Backtest",
            message="No backtest directory found."
        )]
    return 100.0, []

def score_backtest_metrics_validity(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_benchmark_presence(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_trade_count_sufficiency(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def evaluate_backtest_quality(artifacts: Dict[str, Any]) -> QualityDimensionScore:
    issues = []
    s1, i1 = score_backtest_presence(artifacts)
    s2, i2 = score_backtest_metrics_validity(artifacts)
    s3, i3 = score_benchmark_presence(artifacts)
    s4, i4 = score_trade_count_sufficiency(artifacts)

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
        dimension=QualityDimension.BACKTEST,
        score=avg_score,
        weight=0.12,
        status=status,
        issue_count=len(issues),
        critical_count=crit,
        warning_count=warn,
        summary=f"Backtest Quality Score: {avg_score:.1f}",
        issues=issues
    )
