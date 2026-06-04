# Mock appending
with open("usa_signal_bot/notifications/notification_templates.py", "a") as f:
    f.write("\n\ndef format_backtest_run_report_message(review): return 'NotificationMessage()'\n")
    f.write("def format_backtest_run_warning_message(gate): return 'NotificationMessage()'\n")
    f.write("def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'\n")
    f.write("def notifications_from_backtest_run_review(review): return []\n")


def format_backtest_run_report_message(review): return 'NotificationMessage()'
def format_backtest_run_warning_message(gate): return 'NotificationMessage()'
def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'
def notifications_from_backtest_run_review(review): return []

class NotificationMessage:
    pass

def format_backtest_analytics_report_message(review: BacktestAnalyticsFullReview) -> NotificationMessage:
    raise NotImplementedError()

def format_backtest_analytics_warning_message(report: BacktestAnalyticsReport) -> NotificationMessage:
    raise NotImplementedError()

def format_backtest_run_validation_warning_message(report: RunValidationReport) -> NotificationMessage:
    raise NotImplementedError()

def notifications_from_backtest_analytics_review(review: BacktestAnalyticsFullReview) -> list[NotificationMessage]:
    raise NotImplementedError()


from usa_signal_bot.backtesting.walk_forward.phase150_models import WalkForwardFullReview, WalkForwardValidationReport, TemporalStabilityAuditReport

def format_walk_forward_report_message(review: WalkForwardFullReview) -> 'NotificationMessage':
    return NotificationMessage(
        title="Walk Forward Report",
        body="Mock Phase 150 Walk Forward Full Review",
        notification_type="WALK_FORWARD_REPORT",
        severity="INFO"
    )

def format_walk_forward_warning_message(report: WalkForwardValidationReport) -> 'NotificationMessage':
    return NotificationMessage(
        title="Walk Forward Warning",
        body="Walk Forward Report has warnings or errors",
        notification_type="WALK_FORWARD_WARNING",
        severity="WARNING"
    )

def format_temporal_stability_warning_message(audit: TemporalStabilityAuditReport) -> 'NotificationMessage':
    return NotificationMessage(
        title="Temporal Stability Warning",
        body="Temporal Stability Audit failed",
        notification_type="TEMPORAL_STABILITY_WARNING",
        severity="WARNING"
    )

def notifications_from_walk_forward_review(review: WalkForwardFullReview) -> list['NotificationMessage']:
    msgs = [format_walk_forward_report_message(review)]
    if not review.validation_report.report_valid:
        msgs.append(format_walk_forward_warning_message(review.validation_report))
    if not review.temporal_stability_audit.audit_passed:
        msgs.append(format_temporal_stability_warning_message(review.temporal_stability_audit))
    return msgs


def format_backtest_run_report_message(review): return 'NotificationMessage()'
def format_backtest_run_warning_message(gate): return 'NotificationMessage()'
def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'
def notifications_from_backtest_run_review(review): return []
