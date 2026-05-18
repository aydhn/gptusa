from usa_signal_bot.research_execution.execution_models import (
    ConfigSnapshot, ExperimentRunContext, ExperimentArtifact, ResearchRun,
    MetricComparison, AcceptanceGateEvaluation, ExperimentComparisonReport, ResearchExecutionReview
)

def config_snapshot_to_text(item: ConfigSnapshot) -> str:
    lines = [f"--- CONFIG SNAPSHOT: {item.snapshot_id} ---"]
    lines.append(f"Type: {item.snapshot_type.value}")
    lines.append(f"Source: {item.source_ref}")
    lines.append(f"Hash: {item.config_hash}")
    lines.append("NOTE: Secrets are completely redacted.")
    return "\n".join(lines)

def experiment_run_context_to_text(item: ExperimentRunContext) -> str:
    lines = [f"--- RUN CONTEXT: {item.context_id} ---"]
    lines.append(f"Run Type: {item.run_type.value}")
    lines.append(f"Mode: {item.execution_mode.value}")
    lines.append("NOTE: Context strictly forbids order routing and config modification.")
    return "\n".join(lines)

def experiment_artifact_to_text(item: ExperimentArtifact) -> str:
    lines = [f"--- ARTIFACT: {item.artifact_id} ---"]
    lines.append(f"Type: {item.artifact_type.value}")
    lines.append(f"Path: {item.path}")
    return "\n".join(lines)

def research_run_to_text(item: ResearchRun) -> str:
    lines = [f"--- RESEARCH RUN: {item.run_id} ---"]
    lines.append(f"Type: {item.run_type.value}")
    lines.append(f"Status: {item.status.value}")
    lines.append(f"Mode: {item.execution_mode.value}")
    lines.append("NOTE: Run is localized. No actual broker impact.")
    return "\n".join(lines)

def metric_comparison_to_text(item: MetricComparison) -> str:
    return f"{item.metric_name}: {item.baseline_value} -> {item.candidate_value} ({item.interpretation})"

def acceptance_gate_evaluation_to_text(item: AcceptanceGateEvaluation) -> str:
    return f"{item.gate_type}: {item.gate_status} (Threshold: {item.threshold})"

def experiment_comparison_report_to_text(item: ExperimentComparisonReport, limit: int = 100) -> str:
    lines = [f"--- COMPARISON REPORT: {item.report_id} ---"]
    lines.append(f"Outcome: {item.outcome.value}")
    lines.append("\nMetrics:")
    for mc in item.metric_comparisons[:limit]:
        lines.append(f"  {metric_comparison_to_text(mc)}")
    lines.append("\nGates:")
    for ge in item.gate_evaluations[:limit]:
        lines.append(f"  {acceptance_gate_evaluation_to_text(ge)}")
    lines.append("\nNOTE: This report is local analytics, NOT investment advice.")
    lines.append("PASS is NOT live trading approval.")
    return "\n".join(lines)

def research_execution_review_to_text(item: ResearchExecutionReview, limit: int = 100) -> str:
    lines = [f"--- EXECUTION REVIEW: {item.review_id} ---"]
    lines.append(f"Report Type: {item.report_type.value}")
    lines.append(f"Runs: {len(item.runs)}")
    lines.append(f"Reports: {len(item.comparison_reports)}")
    lines.append("\nNOTE: No auto-optimization. No production config patches.")
    return "\n".join(lines)

def execution_store_summary_to_text(summary: dict) -> str:
    lines = ["--- EXECUTION STORE SUMMARY ---"]
    for k, v in summary.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)

def research_execution_limitations_text() -> str:
    return """
--- RESEARCH EXECUTION LIMITATIONS ---
1. Research execution is strictly local analytics.
2. Mock/backtest/walk-forward results do NOT guarantee future performance.
3. No automatic production config patching is performed.
4. No automatic parameter optimization is executed.
5. No live or demo broker orders are generated.
6. A 'PASS' outcome is NOT a live trading approval.
7. This output is NOT investment advice.
"""
