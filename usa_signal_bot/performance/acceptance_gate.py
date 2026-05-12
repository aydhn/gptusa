from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any
import uuid

from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineComparisonStatus, RuntimeRegressionStatus
from usa_signal_bot.performance.baseline_models import BaselineComparisonResult
from usa_signal_bot.performance.threshold_models import SLAEvaluationReport

@dataclass
class PerformanceAcceptanceGateResult:
    gate_id: str
    created_at_utc: str
    status: BaselineComparisonStatus
    scope: PerformanceBaselineScope
    comparison_results: List[BaselineComparisonResult]
    threshold_reports: List[SLAEvaluationReport]
    passed_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    required_actions: List[str]
    optional_actions: List[str]
    warnings: List[str]
    errors: List[str]

def create_performance_gate_id(prefix: str = "perf_gate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def decide_performance_gate_status(comparisons: List[BaselineComparisonResult], threshold_reports: List[SLAEvaluationReport]) -> BaselineComparisonStatus:
    has_blocked = any(c.status == BaselineComparisonStatus.BLOCKED for c in comparisons) or \
                  any(r.status == BaselineComparisonStatus.BLOCKED for r in threshold_reports)
    if has_blocked: return BaselineComparisonStatus.BLOCKED

    has_critical_regression = any(c.regression_status == RuntimeRegressionStatus.CRITICAL_REGRESSION for c in comparisons)
    if has_critical_regression: return BaselineComparisonStatus.BLOCKED

    has_fail = any(c.status == BaselineComparisonStatus.FAIL for c in comparisons) or \
               any(r.status == BaselineComparisonStatus.FAIL for r in threshold_reports)
    has_major_regression = any(c.regression_status == RuntimeRegressionStatus.MAJOR_REGRESSION for c in comparisons)
    if has_fail or has_major_regression: return BaselineComparisonStatus.FAIL

    has_warn = any(c.status == BaselineComparisonStatus.WARN for c in comparisons) or \
               any(r.status == BaselineComparisonStatus.WARN for r in threshold_reports)
    has_moderate_regression = any(c.regression_status == RuntimeRegressionStatus.MODERATE_REGRESSION for c in comparisons)
    if has_warn or has_moderate_regression: return BaselineComparisonStatus.WARN

    # Minor regression or insufficient data is generally a PASS for operational gating unless strictly configured
    return BaselineComparisonStatus.PASS

def build_performance_required_actions(comparisons: List[BaselineComparisonResult], threshold_reports: List[SLAEvaluationReport]) -> List[str]:
    actions = []
    status = decide_performance_gate_status(comparisons, threshold_reports)
    if status in [BaselineComparisonStatus.BLOCKED, BaselineComparisonStatus.FAIL]:
        actions.append("Review blocked/failed SLA thresholds.")
        actions.append("Investigate major/critical runtime regressions before releasing.")
    return actions

def build_performance_optional_actions(comparisons: List[BaselineComparisonResult], threshold_reports: List[SLAEvaluationReport]) -> List[str]:
    actions = []
    status = decide_performance_gate_status(comparisons, threshold_reports)
    if status == BaselineComparisonStatus.WARN:
        actions.append("Consider investigating moderate runtime regressions.")
        actions.append("Monitor warning-level SLA threshold breaches.")
    return actions

def evaluate_performance_acceptance_gate(scope: PerformanceBaselineScope, comparisons: List[BaselineComparisonResult], threshold_reports: List[SLAEvaluationReport]) -> PerformanceAcceptanceGateResult:
    status = decide_performance_gate_status(comparisons, threshold_reports)

    passed_count = sum(1 for c in comparisons if c.status == BaselineComparisonStatus.PASS) + sum(1 for r in threshold_reports if r.status == BaselineComparisonStatus.PASS)
    warning_count = sum(1 for c in comparisons if c.status == BaselineComparisonStatus.WARN) + sum(1 for r in threshold_reports if r.status == BaselineComparisonStatus.WARN)
    failed_count = sum(1 for c in comparisons if c.status == BaselineComparisonStatus.FAIL) + sum(1 for r in threshold_reports if r.status == BaselineComparisonStatus.FAIL)
    blocked_count = sum(1 for c in comparisons if c.status == BaselineComparisonStatus.BLOCKED) + sum(1 for r in threshold_reports if r.status == BaselineComparisonStatus.BLOCKED)

    return PerformanceAcceptanceGateResult(
        gate_id=create_performance_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        scope=scope,
        comparison_results=comparisons,
        threshold_reports=threshold_reports,
        passed_count=passed_count,
        warning_count=warning_count,
        failed_count=failed_count,
        blocked_count=blocked_count,
        required_actions=build_performance_required_actions(comparisons, threshold_reports),
        optional_actions=build_performance_optional_actions(comparisons, threshold_reports),
        warnings=[],
        errors=[]
    )

def performance_acceptance_gate_result_to_dict(result: PerformanceAcceptanceGateResult) -> Dict[str, Any]:
    from usa_signal_bot.performance.baseline_models import baseline_comparison_result_to_dict
    from usa_signal_bot.performance.threshold_models import sla_evaluation_report_to_dict
    return {
        "gate_id": result.gate_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "scope": result.scope.value,
        "comparison_results": [baseline_comparison_result_to_dict(c) for c in result.comparison_results],
        "threshold_reports": [sla_evaluation_report_to_dict(r) for r in result.threshold_reports],
        "passed_count": result.passed_count,
        "warning_count": result.warning_count,
        "failed_count": result.failed_count,
        "blocked_count": result.blocked_count,
        "required_actions": result.required_actions,
        "optional_actions": result.optional_actions,
        "warnings": result.warnings,
        "errors": result.errors
    }

def performance_acceptance_gate_result_to_text(result: PerformanceAcceptanceGateResult, limit: int = 50) -> str:
    lines = [
        f"Performance Acceptance Gate: {result.status.value} (Scope: {result.scope.value})",
        f"Passed: {result.passed_count}, Warnings: {result.warning_count}, Failed: {result.failed_count}, Blocked: {result.blocked_count}"
    ]
    if result.required_actions:
        lines.append("\nRequired Actions:")
        for a in result.required_actions:
            lines.append(f" - {a}")
    if result.optional_actions:
        lines.append("\nOptional Actions:")
        for a in result.optional_actions:
            lines.append(f" - {a}")

    lines.append("\nNote: PASS indicates acceptable local operational performance. It does NOT constitute live trading approval.")
    return "\n".join(lines)
