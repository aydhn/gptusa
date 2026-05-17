from typing import Any, Dict
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticReview, DiagnosticReportType, create_diagnostic_review_id
from usa_signal_bot.diagnostics.event_normalizer import diagnostic_events_from_backtest_result
from usa_signal_bot.diagnostics.strategy_diagnostics import diagnose_strategies
from usa_signal_bot.diagnostics.loss_event_analysis import loss_assessments_by_dimension, detect_repeated_loss_patterns
from usa_signal_bot.diagnostics.remediation_hints import remediation_hints_from_strategy_diagnostics
from usa_signal_bot.diagnostics.diagnostic_scorecard import build_diagnostic_scorecard
from datetime import datetime, timezone

def build_diagnostic_review_from_backtest_result(result: Dict[str, Any]) -> DiagnosticReview:
    events = diagnostic_events_from_backtest_result(result)

    assessments = loss_assessments_by_dimension(events, "symbol")
    clusters = detect_repeated_loss_patterns(events)
    strat_diags = diagnose_strategies(events)
    hints = remediation_hints_from_strategy_diagnostics(strat_diags)
    scorecard = build_diagnostic_scorecard(events, assessments, clusters, strat_diags)

    return DiagnosticReview(
        review_id=create_diagnostic_review_id("bt_review"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=DiagnosticReportType.FULL_DIAGNOSTICS_REVIEW,
        events=events,
        failure_assessments=assessments,
        failure_clusters=clusters,
        strategy_diagnostics=strat_diags,
        remediation_hints=hints,
        scorecard=scorecard
    )

def attach_diagnostics_to_backtest_result(result: Dict[str, Any], review: DiagnosticReview = None) -> Dict[str, Any]:
    if review is None:
        review = build_diagnostic_review_from_backtest_result(result)

    if "metadata" not in result:
        result["metadata"] = {}

    result["metadata"]["diagnostics"] = {
        "review_id": review.review_id,
        "diagnostic_status": review.scorecard.diagnostic_status.value if review.scorecard else "UNKNOWN",
        "failure_mode_count": len(review.failure_assessments),
        "high_severity_failure_count": len([a for a in review.failure_assessments if a.severity.value in ["HIGH", "CRITICAL"]]),
        "degraded_strategy_count": len([s for s in review.strategy_diagnostics if s.status.value in ["DEGRADED", "FAILING"]]),
        "remediation_hint_count": len(review.remediation_hints),
        "top_failure_clusters": [c.name for c in review.failure_clusters[:3]]
    }
    return result

def backtest_diagnostics_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("metadata", {}).get("diagnostics", {})

def backtest_diagnostics_warnings(result: Dict[str, Any]) -> list[str]:
    diags = backtest_diagnostics_summary(result)
    warnings = []
    if diags.get("diagnostic_status") in ["DEGRADED", "FAILING"]:
        warnings.append(f"Backtest diagnostics indicated {diags.get('diagnostic_status')} status.")
    if diags.get("high_severity_failure_count", 0) > 0:
        warnings.append(f"Found {diags.get('high_severity_failure_count')} high severity failures.")
    return warnings
