from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, FailureCluster, StrategyDiagnosticResult,
    RemediationHint, DiagnosticScorecard, DiagnosticReview
)

def diagnostic_event_to_text(item: DiagnosticEvent) -> str:
    return f"[{item.event_id}] {item.symbol} {item.side} - Net PnL: {item.net_pnl_usd}"

def failure_mode_assessment_to_text(item: FailureModeAssessment) -> str:
    return f"[{item.failure_mode.value}] {item.affected_name} - Events: {item.event_count}, Loss: {item.total_net_loss_usd}, Sev: {item.severity.value}"

def failure_cluster_to_text(item: FailureCluster) -> str:
    return f"[{item.cluster_type.value}] {item.name} - Events: {item.event_count}, Loss: {item.total_net_pnl_usd}, Sev: {item.severity.value}"

def strategy_diagnostic_result_to_text(item: StrategyDiagnosticResult) -> str:
    return f"[{item.strategy_name}] Status: {item.status.value}, Win Rate: {item.win_rate}%, Sev: {item.severity.value}"

def remediation_hint_to_text(item: RemediationHint) -> str:
    return f"[{item.target_name}] {item.title} -> {item.safe_action}"

def diagnostic_scorecard_to_text(item: DiagnosticScorecard) -> str:
    return f"Scorecard Status: {item.diagnostic_status.value}, Failures: {item.total_failure_count}, Score: {item.score_components.get('quality_score')}"

def diagnostic_review_to_text(item: DiagnosticReview, limit: int = 100) -> str:
    lines = [
        "================ DIAGNOSTIC REVIEW ================",
        f"Review ID: {item.review_id}",
        f"Report Type: {item.report_type.value}",
        f"Generated At: {item.created_at_utc}",
        "---------------------------------------------------"
    ]
    if item.scorecard:
        lines.append(diagnostic_scorecard_to_text(item.scorecard))

    lines.append("\n-- Top Failure Modes --")
    for a in item.failure_assessments[:10]:
        lines.append(failure_mode_assessment_to_text(a))

    lines.append("\n-- Top Failure Clusters --")
    for c in item.failure_clusters[:10]:
        lines.append(failure_cluster_to_text(c))

    lines.append("\n-- Strategy Diagnostics --")
    for s in item.strategy_diagnostics[:10]:
        lines.append(strategy_diagnostic_result_to_text(s))

    lines.append("\n-- Remediation Hints --")
    for h in item.remediation_hints[:10]:
        lines.append(remediation_hint_to_text(h))

    lines.append("\n---------------------------------------------------")
    lines.append(diagnostics_limitations_text())
    return "\n".join(lines)

def diagnostics_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return (f"Diagnostics Store Summary:\n"
            f"  Events Files: {summary.get('events_files', 0)}\n"
            f"  Assessments Files: {summary.get('assessments_files', 0)}\n"
            f"  Reviews Files: {summary.get('reviews_files', 0)}")

def diagnostics_limitations_text() -> str:
    return """DISCLAIMER: Diagnostics and failure modes are strictly local heuristic analytics based on historical or simulated data.
They do not constitute financial advice, investment recommendations, or live trading approvals.
Failure mode classifications do not imply definitive causality.
Remediation hints are research suggestions and should not be used for automatic code/strategy modifications.
This system does not execute live broker orders and does not use automated portfolio optimizers."""
