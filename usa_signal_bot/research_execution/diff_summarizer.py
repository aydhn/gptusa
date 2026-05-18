from typing import Any
from usa_signal_bot.core.enums import MetricDeltaDirection
from usa_signal_bot.research_execution.execution_models import MetricComparison, AcceptanceGateEvaluation, ExperimentComparisonReport

def summarize_metric_deltas(comparisons: list[MetricComparison]) -> dict[str, Any]:
    improved = len([c for c in comparisons if c.direction == MetricDeltaDirection.IMPROVED])
    worsened = len([c for c in comparisons if c.direction == MetricDeltaDirection.WORSENED])
    unchanged = len([c for c in comparisons if c.direction == MetricDeltaDirection.UNCHANGED])
    missing = len([c for c in comparisons if c.direction == MetricDeltaDirection.INSUFFICIENT_DATA])

    return {
        "total": len(comparisons),
        "improved": improved,
        "worsened": worsened,
        "unchanged": unchanged,
        "insufficient_data": missing
    }

def summarize_gate_results(evaluations: list[AcceptanceGateEvaluation]) -> dict[str, Any]:
    passed = len([e for e in evaluations if e.passed])
    failed = len([e for e in evaluations if e.passed is False])
    skipped = len([e for e in evaluations if e.passed is None])

    return {
        "total": len(evaluations),
        "passed": passed,
        "failed": failed,
        "skipped": skipped
    }

def summarize_experiment_differences(report: ExperimentComparisonReport) -> dict[str, Any]:
    return {
        "metric_summary": summarize_metric_deltas(report.metric_comparisons),
        "gate_summary": summarize_gate_results(report.gate_evaluations),
        "top_improvements": [c.metric_name for c in top_improved_metrics(report.metric_comparisons)],
        "top_degradations": [c.metric_name for c in top_worsened_metrics(report.metric_comparisons)],
        "outcome": report.outcome.value
    }

def top_improved_metrics(comparisons: list[MetricComparison], top_n: int = 5) -> list[MetricComparison]:
    improved = [c for c in comparisons if c.direction == MetricDeltaDirection.IMPROVED and c.delta_pct is not None]
    improved.sort(key=lambda c: abs(c.delta_pct), reverse=True)
    return improved[:top_n]

def top_worsened_metrics(comparisons: list[MetricComparison], top_n: int = 5) -> list[MetricComparison]:
    worsened = [c for c in comparisons if c.direction == MetricDeltaDirection.WORSENED and c.delta_pct is not None]
    worsened.sort(key=lambda c: abs(c.delta_pct), reverse=True)
    return worsened[:top_n]

def diff_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["--- DIFFERENCE SUMMARY ---"]
    lines.append(f"Outcome: {summary.get('outcome')}")
    ms = summary.get('metric_summary', {})
    lines.append(f"Metrics: {ms.get('improved')} improved, {ms.get('worsened')} worsened, {ms.get('unchanged')} unchanged.")
    gs = summary.get('gate_summary', {})
    lines.append(f"Gates: {gs.get('passed')} passed, {gs.get('failed')} failed.")
    lines.append(f"Top Improvements: {', '.join(summary.get('top_improvements', []))}")
    lines.append(f"Top Degradations: {', '.join(summary.get('top_degradations', []))}")
    return "\n".join(lines)
