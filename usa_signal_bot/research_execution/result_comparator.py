from typing import Any
from usa_signal_bot.core.enums import MetricDeltaDirection, ComparisonOutcome
from usa_signal_bot.research_execution.execution_models import MetricComparison, ResearchRun, ExperimentComparisonReport, create_metric_comparison_id, create_experiment_comparison_report_id
from usa_signal_bot.research_execution.metrics_extractor import extract_metrics_from_research_run
from datetime import datetime, timezone

def compare_metric(metric_name: str, baseline_value: float | None, candidate_value: float | None, higher_is_better: bool = True) -> MetricComparison:
    if baseline_value is None or candidate_value is None:
        return MetricComparison(
            comparison_id=create_metric_comparison_id(metric_name),
            metric_name=metric_name,
            baseline_value=baseline_value,
            candidate_value=candidate_value,
            delta_value=None,
            delta_pct=None,
            direction=MetricDeltaDirection.INSUFFICIENT_DATA,
            interpretation="Insufficient data for comparison.",
            warnings=["Missing value(s)."],
            errors=[]
        )

    delta = candidate_value - baseline_value
    delta_pct = (delta / abs(baseline_value)) * 100 if baseline_value != 0 else 0.0

    if abs(delta) < 1e-6:
        direction = MetricDeltaDirection.UNCHANGED
        interp = "Unchanged"
    else:
        if higher_is_better:
            direction = MetricDeltaDirection.IMPROVED if delta > 0 else MetricDeltaDirection.WORSENED
        else:
            direction = MetricDeltaDirection.IMPROVED if delta < 0 else MetricDeltaDirection.WORSENED

        interp = "Improved" if direction == MetricDeltaDirection.IMPROVED else "Worsened"

    return MetricComparison(
        comparison_id=create_metric_comparison_id(metric_name),
        metric_name=metric_name,
        baseline_value=baseline_value,
        candidate_value=candidate_value,
        delta_value=delta,
        delta_pct=delta_pct,
        direction=direction,
        interpretation=interp,
        warnings=[],
        errors=[]
    )

def compare_research_runs(baseline: ResearchRun, candidate: ResearchRun) -> ExperimentComparisonReport:
    b_metrics = extract_metrics_from_research_run(baseline)
    c_metrics = extract_metrics_from_research_run(candidate)

    comparisons = []
    all_keys = set(list(b_metrics.keys()) + list(c_metrics.keys()))

    for k in all_keys:
        higher_better = infer_metric_higher_is_better(k)
        mc = compare_metric(k, b_metrics.get(k), c_metrics.get(k), higher_better)
        comparisons.append(mc)

    outcome = determine_comparison_outcome(comparisons)

    return ExperimentComparisonReport(
        report_id=create_experiment_comparison_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        experiment_id=candidate.experiment_id,
        baseline_run_id=baseline.run_id,
        candidate_run_id=candidate.run_id,
        outcome=outcome,
        metric_comparisons=comparisons,
        gate_evaluations=[],
        attribution_delta={},
        diagnostics_delta={},
        summary={"comparisons_count": len(comparisons)},
        warnings=[],
        errors=[]
    )

def infer_metric_higher_is_better(metric_name: str) -> bool:
    lower_better_keywords = ["drawdown", "cost", "drag", "turnover", "latency", "error", "risk"]
    for k in lower_better_keywords:
        if k in metric_name.lower():
            return False
    return True

def determine_comparison_outcome(metric_comparisons: list[MetricComparison], gate_evaluations: list[Any] | None = None) -> ComparisonOutcome:
    improved = 0
    worsened = 0
    missing = 0

    for mc in metric_comparisons:
        if mc.direction == MetricDeltaDirection.IMPROVED:
            improved += 1
        elif mc.direction == MetricDeltaDirection.WORSENED:
            worsened += 1
        elif mc.direction == MetricDeltaDirection.INSUFFICIENT_DATA:
            missing += 1

    if missing > len(metric_comparisons) / 2:
        return ComparisonOutcome.INSUFFICIENT_DATA

    if improved > worsened:
        return ComparisonOutcome.CANDIDATE_BETTER
    elif worsened > improved:
        return ComparisonOutcome.BASELINE_BETTER
    elif improved > 0 or worsened > 0:
        return ComparisonOutcome.MIXED

    return ComparisonOutcome.INCONCLUSIVE

def comparison_report_summary(report: ExperimentComparisonReport) -> dict[str, Any]:
    return {
        "report_id": report.report_id,
        "outcome": report.outcome.value,
        "metrics_compared": len(report.metric_comparisons)
    }

def comparison_report_to_text(report: ExperimentComparisonReport) -> str:
    lines = [f"--- COMPARISON REPORT: {report.report_id} ---"]
    lines.append(f"Outcome: {report.outcome.value}")
    lines.append("\nMetric Deltas:")
    for mc in report.metric_comparisons:
        b_val = f"{mc.baseline_value:.2f}" if mc.baseline_value is not None else "N/A"
        c_val = f"{mc.candidate_value:.2f}" if mc.candidate_value is not None else "N/A"
        d_val = f"{mc.delta_value:.2f}" if mc.delta_value is not None else "N/A"
        lines.append(f"  {mc.metric_name}: Baseline={b_val} -> Candidate={c_val} (Delta: {d_val}) [{mc.interpretation}]")

    lines.append("\nNOTE: Comparison outcome does NOT guarantee future performance.")
    return "\n".join(lines)
