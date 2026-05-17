from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticReview, FailureModeAssessment, StrategyDiagnosticResult

class NotificationMessage:
    def __init__(self, title: str, body: str, severity: str):
        self.title = title
        self.body = body
        self.severity = severity

def format_diagnostics_report_message(review: DiagnosticReview) -> NotificationMessage:
    status = review.scorecard.diagnostic_status.value if review.scorecard else "UNKNOWN"
    body = (
        f"Diagnostic Review ID: {review.review_id}\n"
        f"Status: {status}\n"
        f"Failures Identified: {len(review.failure_assessments)}\n"
        f"Degraded Strategies: {len([s for s in review.strategy_diagnostics if s.status.value in ['DEGRADED', 'FAILING']])}\n"
        f"Remediation Hints: {len(review.remediation_hints)}\n"
        f"\nNote: This is a diagnostic review report. It is NOT investment advice and does NOT indicate live trading approval."
    )
    return NotificationMessage(title="Diagnostics Review Report", body=body, severity="INFO" if status == "HEALTHY" else "WARNING")

def format_failure_mode_warning_message(assessments: List[FailureModeAssessment]) -> NotificationMessage:
    high_sev = [a for a in assessments if a.severity.value in ["HIGH", "CRITICAL"]]
    body = f"Detected {len(high_sev)} high/critical severity failure modes in recent diagnostic analysis. Manual review recommended."
    return NotificationMessage(title="Failure Mode Warning", body=body, severity="WARNING")

def format_strategy_diagnostic_warning_message(results: List[StrategyDiagnosticResult]) -> NotificationMessage:
    degraded = [s.strategy_name for s in results if s.status.value in ["DEGRADED", "FAILING"]]
    body = f"The following strategies are showing degraded or failing diagnostic status: {', '.join(degraded)}. Please review their logic locally."
    return NotificationMessage(title="Strategy Diagnostic Warning", body=body, severity="WARNING")

def notifications_from_diagnostic_review(review: DiagnosticReview) -> List[NotificationMessage]:
    msgs = [format_diagnostics_report_message(review)]
    high_sev_assessments = [a for a in review.failure_assessments if a.severity.value in ["HIGH", "CRITICAL"]]
    if high_sev_assessments:
        msgs.append(format_failure_mode_warning_message(high_sev_assessments))

    degraded_strats = [s for s in review.strategy_diagnostics if s.status.value in ["DEGRADED", "FAILING"]]
    if degraded_strats:
        msgs.append(format_strategy_diagnostic_warning_message(degraded_strats))

    return msgs
