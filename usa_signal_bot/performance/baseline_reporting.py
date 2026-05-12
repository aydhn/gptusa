import json
from pathlib import Path
from typing import Dict, Any, Optional

from usa_signal_bot.performance.baseline_models import (
    PerformanceMetricBaseline,
    PerformanceBaseline,
    CurrentPerformanceSample,
    BaselineComparisonResult,
    PerformanceReviewResult
)
from usa_signal_bot.performance.threshold_models import SLAThreshold, SLAEvaluationReport
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult
from usa_signal_bot.performance.alert_rules import PerformanceAlert
from usa_signal_bot.performance.baseline_validation import PerformanceValidationReport
from usa_signal_bot.performance.baseline_store import write_performance_review_result_json


def performance_metric_baseline_to_text(metric: PerformanceMetricBaseline) -> str:
    parts = [f"{metric.name.value}:"]
    if metric.p90_value is not None:
        parts.append(f"p90={metric.p90_value:.2f}")
    if metric.mean_value is not None:
        parts.append(f"mean={metric.mean_value:.2f}")
    if metric.max_value is not None:
        parts.append(f"max={metric.max_value:.2f}")
    return " ".join(parts)

def performance_baseline_to_text(baseline: PerformanceBaseline, limit: int = 50) -> str:
    lines = [f"Performance Baseline: {baseline.scope.value} (v: {baseline.version})"]
    lines.append(f"Status: {baseline.status.value}, Sources: {baseline.source_count}")
    for m in baseline.metrics[:limit]:
        lines.append(f" - {performance_metric_baseline_to_text(m)}")
    return "\n".join(lines)

def current_performance_sample_to_text(sample: CurrentPerformanceSample) -> str:
    lines = [f"Current Performance Sample: {sample.scope.value}"]
    for k, v in sample.metrics.items():
        val_str = f"{v:.2f}" if isinstance(v, float) else str(v)
        lines.append(f" - {k}: {val_str}")
    return "\n".join(lines)

def baseline_comparison_result_to_text(result: BaselineComparisonResult, limit: int = 50) -> str:
    lines = [f"Baseline Comparison [{result.status.value}]"]
    for r in result.metric_results[:limit]:
        delta_str = f"{r['delta_pct']:.1f}%" if r['delta_pct'] is not None else "N/A"
        lines.append(f" - {r['metric_name']}: obs={r['observed']}, base_p90={r['baseline_p90']} (Delta: {delta_str}) -> {r['status']}")
    lines.append(f"Drift Direction: {result.drift_direction.value}")
    lines.append(f"Regression Status: {result.regression_status.value}")
    return "\n".join(lines)

def sla_threshold_to_text(threshold: SLAThreshold) -> str:
    return f"{threshold.name} [{threshold.threshold_type.value}]: Warn={threshold.warning_value}, Crit={threshold.critical_value}, Block={threshold.blocker_value} (Sev: {threshold.severity.value})"

def sla_evaluation_report_to_text(report: SLAEvaluationReport, limit: int = 50) -> str:
    lines = [f"SLA Evaluation Report [{report.status.value}]"]
    lines.append(f"Pass: {report.pass_count}, Warn: {report.warn_count}, Fail: {report.fail_count}, Blocked: {report.blocked_count}")
    for e in report.evaluations[:limit]:
        lines.append(f" - {e.metric_name.value}: {e.status.value} ({e.message})")
    lines.append("\nNote: SLA PASS is not an approval for live trading. This is a local operational baseline.")
    return "\n".join(lines)

def performance_acceptance_gate_result_to_text(result: PerformanceAcceptanceGateResult, limit: int = 50) -> str:
    lines = [
        f"Performance Acceptance Gate: {result.status.value} (Scope: {result.scope.value})",
        f"Passed: {result.passed_count}, Warnings: {result.warning_count}, Failed: {result.failed_count}, Blocked: {result.blocked_count}"
    ]
    if result.required_actions:
        lines.append("\nRequired Actions:")
        for a in result.required_actions[:limit]:
            lines.append(f" - {a}")
    if result.optional_actions:
        lines.append("\nOptional Actions:")
        for a in result.optional_actions[:limit]:
            lines.append(f" - {a}")

    lines.append("\nNote: PASS indicates acceptable local operational performance. It does NOT constitute live trading approval.")
    return "\n".join(lines)

def performance_alert_to_text(alert: PerformanceAlert) -> str:
    return f"[{alert.severity.value}] {alert.title} - {alert.message}"

def performance_review_result_to_text(result: PerformanceReviewResult, limit: int = 50) -> str:
    lines = [
        "===========================================================",
        f"PERFORMANCE REVIEW RESULT: {result.status.value}",
        f"Type: {result.report_type.value}",
        f"Date: {result.created_at_utc}",
        "===========================================================",
        f"Overall Acceptance: {result.acceptance_status.value}"
    ]

    if result.samples:
        lines.append(f"\nSamples Evaluated: {len(result.samples)}")

    if result.comparisons:
        lines.append("\nKey Comparisons:")
        for c in result.comparisons[:limit]:
            lines.append(f" - Scope {c.scope.value}: {c.regression_status.value} ({c.drift_direction.value})")

    lines.append(performance_baseline_limitations_text())
    return "\n".join(lines)

def baseline_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return (
        f"Performance Store Summary:\n"
        f" - Baselines: {summary.get('baseline_count', 0)}\n"
        f" - Reviews: {summary.get('review_count', 0)}\n"
        f" - Latest Baseline: {summary.get('latest_baseline')}\n"
        f" - Latest Review: {summary.get('latest_review')}"
    )

def performance_baseline_limitations_text() -> str:
    return (
        "\n--- PERFORMANCE BASELINE LIMITATIONS ---\n"
        "1. This is a local operational performance review only.\n"
        "2. No external telemetry or cloud monitoring is used or supported.\n"
        "3. A 'PASS' outcome is purely for local pipeline runtime acceptance.\n"
        "4. This report does not contain, nor should it be construed as, investment advice.\n"
        "5. A passing performance gate is NOT a live trading approval.\n"
        "6. No broker integration, live, or demo orders will be triggered by these alerts."
    )

def write_performance_report_json(path: Path, result: PerformanceReviewResult, validation_report: Optional[PerformanceValidationReport] = None) -> Path:
    from usa_signal_bot.performance.baseline_models import performance_review_result_to_dict
    payload = performance_review_result_to_dict(result)

    if validation_report:
        payload["validation_valid"] = validation_report.valid
        payload["validation_issues"] = [i.message for i in validation_report.issues]

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(payload, f, indent=2)
    return path
