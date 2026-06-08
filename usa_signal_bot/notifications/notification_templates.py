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


def format_backtest_run_report_message(review): return 'NotificationMessage()'
def format_backtest_run_warning_message(gate): return 'NotificationMessage()'
def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'
def notifications_from_backtest_run_review(review): return []

def format_portfolio_foundation_report_message(review: Any) -> NotificationMessage:
    msg = NotificationMessage()
    return msg

def format_portfolio_foundation_warning_message(context: Any) -> NotificationMessage:
    msg = NotificationMessage()
    return msg

def format_position_sizing_boundary_warning_message(report: Any) -> NotificationMessage:
    msg = NotificationMessage()
    return msg

def notifications_from_portfolio_foundation_review(review: Any) -> list[NotificationMessage]:
    return [format_portfolio_foundation_report_message(review)]

def format_sizing_prototype_report_message(review: 'SizingPrototypeFullReview') -> 'NotificationMessage':
    from usa_signal_bot.notifications.notification_adapters import NotificationMessage
    return NotificationMessage(title="Sizing Prototype Report", body="Phase 154 prototype completed.")

def format_sizing_prototype_warning_message(context: 'SizingPrototypeContext') -> 'NotificationMessage':
    from usa_signal_bot.notifications.notification_adapters import NotificationMessage
    return NotificationMessage(title="Sizing Prototype Warning", body="Phase 154 warning.")

def format_sizing_safety_warning_message(boundary: 'SizingSafetyBoundaryResult') -> 'NotificationMessage':
    from usa_signal_bot.notifications.notification_adapters import NotificationMessage
    return NotificationMessage(title="Sizing Safety Warning", body="Phase 154 safety boundary alert.")

def notifications_from_sizing_prototype_review(review: 'SizingPrototypeFullReview') -> list['NotificationMessage']:
    return [format_sizing_prototype_report_message(review)]

def format_portfolio_construction_sandbox_report_message(review: PortfolioConstructionFullReview) -> NotificationMessage:
    from usa_signal_bot.portfolio.construction.portfolio_construction_report import portfolio_construction_full_review_to_text
    text = portfolio_construction_full_review_to_text(review)
    return NotificationMessage(
        type=NotificationType.PORTFOLIO_CONSTRUCTION_SANDBOX_REPORT,
        subject="Portfolio Construction Sandbox Report",
        body=text,
        level=NotificationLevel.INFO,
        metadata={"review_id": review.review_id}
    )

def format_portfolio_construction_sandbox_warning_message(context: PortfolioConstructionContext) -> NotificationMessage:
    return NotificationMessage(
        type=NotificationType.PORTFOLIO_CONSTRUCTION_SANDBOX_WARNING,
        subject="Portfolio Construction Sandbox Warning",
        body=f"Phase 155 readiness failed for context {context.context_id}.",
        level=NotificationLevel.WARNING,
        metadata={"context_id": context.context_id}
    )

def format_allocation_sandbox_safety_warning_message(boundary: AllocationSandboxSafetyBoundaryResult) -> NotificationMessage:
    failed = [r.name for r in boundary.rules if not r.passed]
    return NotificationMessage(
        type=NotificationType.ALLOCATION_SANDBOX_SAFETY_WARNING,
        subject="Allocation Sandbox Safety Boundary Alert",
        body=f"Safety boundary {boundary.boundary_id} failed. Rules: {failed}",
        level=NotificationLevel.ERROR,
        metadata={"boundary_id": boundary.boundary_id}
    )

def notifications_from_portfolio_construction_review(review: PortfolioConstructionFullReview) -> List[NotificationMessage]:
    msgs = [format_portfolio_construction_sandbox_report_message(review)]
    if not review.phase156_readiness_gate.ready_for_phase156:
        msgs.append(format_portfolio_construction_sandbox_warning_message(review.context))
    if not review.safety_boundary.boundary_passed:
        msgs.append(format_allocation_sandbox_safety_warning_message(review.safety_boundary))
    return msgs


def format_backtest_run_report_message(review): return 'NotificationMessage()'
def format_backtest_run_warning_message(gate): return 'NotificationMessage()'
def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'
def notifications_from_backtest_run_review(review): return []

from typing import Any, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerPrototypeFullReview, OptimizerPrototypeContext, OptimizerSafetyBoundaryResult

def format_optimizer_prototype_report_message(review: OptimizerPrototypeFullReview) -> Any:
    return {"message": "Phase 156 Optimizer Prototype Report", "valid": len(review.errors) == 0}

def format_optimizer_prototype_warning_message(context: OptimizerPrototypeContext) -> Any:
    return {"message": "Phase 156 Optimizer Prototype Warning", "errors": context.errors}

def format_optimizer_safety_warning_message(boundary: OptimizerSafetyBoundaryResult) -> Any:
    return {"message": "Phase 156 Optimizer Safety Warning", "passed": boundary.boundary_passed}

def notifications_from_optimizer_prototype_review(review: OptimizerPrototypeFullReview) -> List[Any]:
    return [format_optimizer_prototype_report_message(review)]
