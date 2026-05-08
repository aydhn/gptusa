"""Research Quality Scorecard calculator."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualityReportType
from usa_signal_bot.quality.quality_models import (
    ResearchQualityScorecard,
    QualityDimensionScore,
    QualityIssue,
    create_scorecard_id,
)

from usa_signal_bot.quality.data_quality_evaluator import evaluate_data_quality
from usa_signal_bot.quality.feature_quality_evaluator import evaluate_feature_quality
from usa_signal_bot.quality.signal_quality_evaluator import evaluate_signal_quality
from usa_signal_bot.quality.backtest_quality_evaluator import evaluate_backtest_quality
from usa_signal_bot.quality.robustness_quality_evaluator import evaluate_robustness_quality
from usa_signal_bot.quality.risk_portfolio_quality_evaluator import evaluate_risk_portfolio_quality
from usa_signal_bot.quality.paper_quality_evaluator import evaluate_paper_quality
from usa_signal_bot.quality.comparison_quality_evaluator import evaluate_comparison_quality
from usa_signal_bot.quality.runtime_safety_evaluator import evaluate_runtime_safety_quality
from usa_signal_bot.quality.documentation_quality_evaluator import evaluate_documentation_quality

logger = logging.getLogger(__name__)

def default_quality_weights() -> Dict[QualityDimension, float]:
    return {
        QualityDimension.DATA: 0.10,
        QualityDimension.FEATURE: 0.08,
        QualityDimension.SIGNAL: 0.10,
        QualityDimension.BACKTEST: 0.12,
        QualityDimension.ROBUSTNESS: 0.10,
        QualityDimension.RISK: 0.10,
        QualityDimension.PORTFOLIO: 0.08, # Port/Risk merged in our evaluator
        QualityDimension.PAPER: 0.10,
        QualityDimension.COMPARISON: 0.10,
        QualityDimension.RUNTIME: 0.07,
        QualityDimension.NOTIFICATION: 0.03, # Runtime/Notification merged
        QualityDimension.DOCUMENTATION: 0.02,
    }

def normalize_quality_weights(weights: Dict[QualityDimension, float]) -> Dict[QualityDimension, float]:
    total = sum(v for v in weights.values() if v > 0)
    if total <= 0:
        return default_quality_weights()
    return {k: v / total for k, v in weights.items() if v > 0}

def calculate_overall_quality_score(dimension_scores: List[QualityDimensionScore]) -> Optional[float]:
    valid_scores = [d for d in dimension_scores if d.score is not None]
    if not valid_scores:
        return None

    total_weight = sum(d.weight for d in valid_scores)
    if total_weight <= 0:
        return None

    weighted_sum = sum(d.score * d.weight for d in valid_scores) # type: ignore
    return weighted_sum / total_weight

def classify_quality_status(score: Optional[float], critical_count: int = 0, warning_count: int = 0) -> QualityStatus:
    if score is None:
        return QualityStatus.INSUFFICIENT_DATA
    if critical_count > 0:
        return QualityStatus.FAIL
    if score < 50.0:
        return QualityStatus.FAIL
    if score < 75.0 or warning_count > 0:
        return QualityStatus.WARN
    return QualityStatus.PASS

def merge_quality_issues(dimension_scores: List[QualityDimensionScore]) -> List[QualityIssue]:
    issues = []
    for d in dimension_scores:
        issues.extend(d.issues)
    return issues

def build_research_quality_scorecard(
    artifacts: Dict[str, Any],
    weights: Optional[Dict[QualityDimension, float]] = None
) -> ResearchQualityScorecard:
    weights = normalize_quality_weights(weights or default_quality_weights())

    dimensions = []
    d_data = evaluate_data_quality(artifacts)
    d_data.weight = weights.get(QualityDimension.DATA, 0.0)
    dimensions.append(d_data)

    d_feature = evaluate_feature_quality(artifacts)
    d_feature.weight = weights.get(QualityDimension.FEATURE, 0.0)
    dimensions.append(d_feature)

    d_signal = evaluate_signal_quality(artifacts)
    d_signal.weight = weights.get(QualityDimension.SIGNAL, 0.0)
    dimensions.append(d_signal)

    d_backtest = evaluate_backtest_quality(artifacts)
    d_backtest.weight = weights.get(QualityDimension.BACKTEST, 0.0)
    dimensions.append(d_backtest)

    d_robustness = evaluate_robustness_quality(artifacts)
    d_robustness.weight = weights.get(QualityDimension.ROBUSTNESS, 0.0)
    dimensions.append(d_robustness)

    d_risk = evaluate_risk_portfolio_quality(artifacts)
    d_risk.weight = weights.get(QualityDimension.RISK, 0.0) + weights.get(QualityDimension.PORTFOLIO, 0.0)
    dimensions.append(d_risk)

    d_paper = evaluate_paper_quality(artifacts)
    d_paper.weight = weights.get(QualityDimension.PAPER, 0.0)
    dimensions.append(d_paper)

    d_comparison = evaluate_comparison_quality(artifacts)
    d_comparison.weight = weights.get(QualityDimension.COMPARISON, 0.0)
    dimensions.append(d_comparison)

    d_runtime = evaluate_runtime_safety_quality(artifacts)
    d_runtime.weight = weights.get(QualityDimension.RUNTIME, 0.0) + weights.get(QualityDimension.NOTIFICATION, 0.0)
    dimensions.append(d_runtime)

    import pathlib
    project_root = pathlib.Path(artifacts.get("data_root", "."))
    if project_root.name == "data" and project_root.parent:
        project_root = project_root.parent
    d_doc = evaluate_documentation_quality(project_root)
    d_doc.weight = weights.get(QualityDimension.DOCUMENTATION, 0.0)
    dimensions.append(d_doc)

    issues = merge_quality_issues(dimensions)
    crit_count = sum(1 for d in dimensions for i in d.issues if i.severity.name == "CRITICAL")
    warn_count = sum(1 for d in dimensions for i in d.issues if i.severity.name in ("HIGH", "MODERATE"))

    overall_score = calculate_overall_quality_score(dimensions)
    overall_status = classify_quality_status(overall_score, crit_count, warn_count)

    return ResearchQualityScorecard(
        scorecard_id=create_scorecard_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=QualityReportType.SCORECARD,
        overall_score=overall_score,
        overall_status=overall_status,
        dimensions=dimensions,
        issues=issues,
        warnings=[],
        errors=[]
    )

def scorecard_to_text(scorecard: ResearchQualityScorecard) -> str:
    lines = [
        f"--- Research Quality Scorecard ({scorecard.scorecard_id}) ---",
        f"Overall Score: {scorecard.overall_score:.1f} ({scorecard.overall_status.name})",
        ""
    ]
    for d in scorecard.dimensions:
        score_str = f"{d.score:.1f}" if d.score is not None else "N/A"
        lines.append(f"{d.dimension.name:<15}: {score_str:>5} (Weight: {d.weight:.2f}) [{d.status.name}]")

    if scorecard.issues:
        lines.append("\nIssues:")
        for i in scorecard.issues:
            lines.append(f" - [{i.severity.name}] {i.dimension.name}: {i.title} - {i.message}")

    return "\n".join(lines)
