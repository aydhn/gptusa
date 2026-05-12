from typing import Dict, Any, Optional
from usa_signal_bot.core.enums import BaselineComparisonStatus
from usa_signal_bot.performance.baseline_models import BaselineComparisonResult, PerformanceReviewResult
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult

def quality_issue_from_performance_gate(result: PerformanceAcceptanceGateResult) -> Dict[str, Any]:
    if result.status == BaselineComparisonStatus.PASS:
        return {}

    return {
        "issue_type": "PERFORMANCE_DEGRADATION",
        "severity": "HIGH" if result.status in [BaselineComparisonStatus.FAIL, BaselineComparisonStatus.BLOCKED] else "MEDIUM",
        "description": f"Performance gate status is {result.status.value}",
        "failed_count": result.failed_count,
        "blocked_count": result.blocked_count
    }

def quality_dimension_score_from_performance_review(review: PerformanceReviewResult) -> Dict[str, Any]:
    score = 100.0
    if review.acceptance_status == BaselineComparisonStatus.WARN:
        score = 80.0
    elif review.acceptance_status == BaselineComparisonStatus.FAIL:
        score = 40.0
    elif review.acceptance_status == BaselineComparisonStatus.BLOCKED:
        score = 0.0

    return {
        "dimension": "runtime_performance",
        "score": score,
        "status": review.acceptance_status.value
    }

def acceptance_warning_from_runtime_regression(result: BaselineComparisonResult) -> Optional[str]:
    from usa_signal_bot.core.enums import RuntimeRegressionStatus
    if result.regression_status in [RuntimeRegressionStatus.MAJOR_REGRESSION, RuntimeRegressionStatus.CRITICAL_REGRESSION]:
        return f"Warning: {result.regression_status.value} detected in baseline performance metrics."
    return None

def quality_adapter_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Quality Performance Adapter Summary:\n{summary}"
