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


def format_full_system_integration_report_message(review: Any) -> Any:
    return "Full System Integration Report (preview_only=True)"

def format_full_system_integration_warning_message(context: Any) -> Any:
    return "Full System Integration Warning (preview_only=True)"

def format_e2e_rehearsal_warning_message(result: Any) -> Any:
    return "E2E Rehearsal Warning (preview_only=True)"

def notifications_from_full_system_integration_review(review: Any) -> list:
    return []


def format_backtest_run_report_message(review): return 'NotificationMessage()'
def format_backtest_run_warning_message(gate): return 'NotificationMessage()'
def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'
def notifications_from_backtest_run_review(review): return []

def format_advanced_acceptance_report_message(review: Any) -> NotificationMessage:
    lines = [
        "Advanced Acceptance Report (Phase 159)",
        "This is an offline dry-run output, NOT trading or deployment approval.",
        f"Review ID: {review.review_id}",
        f"Ready for Phase 160: {review.phase160_readiness_gate.ready_for_phase160 if review.phase160_readiness_gate else False}"
    ]
    return NotificationMessage(
        message_id="adv_acc_" + review.review_id,
        created_at_utc="mock_timestamp",
        notification_type=NotificationType.ADVANCED_ACCEPTANCE_REPORT,
        subject="Advanced Acceptance Report",
        body="\n".join(lines),
        dry_run_only=True,
        metadata={}
    )

def format_release_candidate_warning_message(audit: Any) -> NotificationMessage:
    lines = [
        "Release Candidate Warning (Phase 159)",
        f"Audit ID: {audit.audit_id}",
        f"Failed Areas: {audit.failed_area_count}",
        f"Blocking Risks: {audit.risk_register.blocking_risk_count if audit.risk_register else 0}"
    ]
    return NotificationMessage(
        message_id="rc_warn_" + audit.audit_id,
        created_at_utc="mock_timestamp",
        notification_type=NotificationType.RELEASE_CANDIDATE_WARNING,
        subject="Release Candidate Warning",
        body="\n".join(lines),
        dry_run_only=True,
        metadata={}
    )

def format_final_freeze_warning_message(certificate: Any) -> NotificationMessage:
    lines = [
        "Final Freeze Warning (Phase 159)",
        f"Certificate ID: {certificate.certificate_id}",
        f"Frozen: {certificate.frozen}"
    ]
    return NotificationMessage(
        message_id="freeze_warn_" + certificate.certificate_id,
        created_at_utc="mock_timestamp",
        notification_type=NotificationType.FINAL_FREEZE_WARNING,
        subject="Final Freeze Warning",
        body="\n".join(lines),
        dry_run_only=True,
        metadata={}
    )

def notifications_from_advanced_acceptance_review(review: Any) -> List[NotificationMessage]:
    msgs = [format_advanced_acceptance_report_message(review)]
    if review.release_candidate_audit and not review.release_candidate_audit.audit_passed:
        msgs.append(format_release_candidate_warning_message(review.release_candidate_audit))
    if review.final_freeze_certificate and not review.final_freeze_certificate.frozen:
        msgs.append(format_final_freeze_warning_message(review.final_freeze_certificate))
    return msgs

def format_final_system_audit_report_message(review: 'Any') -> 'Any':
    return f"[FINAL AUDIT] {review.review_id} completed. Safe and local only."

def format_final_delivery_certificate_message(certificate: 'Any') -> 'Any':
    return f"[FINAL CERTIFICATE] Delivered={certificate.delivered}"

def format_project_closure_report_message(report: 'Any') -> 'Any':
    return f"[PROJECT CLOSURE] Closed={report.project_closed}"

def notifications_from_final_closure_review(review: 'Any') -> list['Any']:
    return [
        format_final_system_audit_report_message(review),
        format_final_delivery_certificate_message(review.final_delivery_certificate),
        format_project_closure_report_message(review.project_closure_report)
    ]


def format_backtest_run_report_message(review): return 'NotificationMessage()'
def format_backtest_run_warning_message(gate): return 'NotificationMessage()'
def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'
def notifications_from_backtest_run_review(review): return []
