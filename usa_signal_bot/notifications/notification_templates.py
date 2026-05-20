from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalReview, ShadowRehearsalSession

class NotificationMessage:
    def __init__(self, message: str, is_real_send: bool):
        self.message = message
        self.is_real_send = is_real_send

def format_paper_shadow_report_message(review: ShadowRehearsalReview) -> NotificationMessage:
    return NotificationMessage(f"Paper-shadow review required: {review.review_id}", False)

def format_shadow_safety_warning_message(sessions: List[ShadowRehearsalSession]) -> NotificationMessage:
    return NotificationMessage("Shadow safety warning detected.", False)

def format_shadow_rehearsal_warning_message(sessions: List[ShadowRehearsalSession]) -> NotificationMessage:
    return NotificationMessage("Shadow rehearsal warning detected.", False)

def notifications_from_shadow_rehearsal_review(review: ShadowRehearsalReview) -> List[NotificationMessage]:
    return [format_paper_shadow_report_message(review)]

from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowGovernanceReview, ShadowAcceptanceScorecard, ShadowDecisionBoardResult

def format_shadow_governance_report_message(review: ShadowGovernanceReview) -> str:
    return f"[SHADOW GOVERNANCE] Review ID: {review.review_id}"

def format_shadow_acceptance_warning_message(scorecards: list[ShadowAcceptanceScorecard]) -> str:
    return f"[SHADOW WARNING] High risk scorecard detected."

def format_shadow_decision_warning_message(decisions: list[ShadowDecisionBoardResult]) -> str:
    return f"[SHADOW WARNING] Decision board issued a warning."

def notifications_from_shadow_governance_review(review: ShadowGovernanceReview) -> list[str]:
    return [format_shadow_governance_report_message(review)]


def format_quarantine_report_message(review: 'QuarantineEnrollmentReview') -> NotificationMessage:
    from usa_signal_bot.paper_quarantine.enrollment_report import quarantine_review_summary, quarantine_limitations_text
    summary = quarantine_review_summary(review)

    lines = [
        "🛡️ Quarantine Enrollment Review 🛡️",
        f"Review ID: {review.review_id}",
        f"Candidates Enrolled: {summary['candidate_count']}",
        f"Errors: {summary['error_count']}",
        "",
        "Note: Quarantine review required.",
        "Local governance metadata only.",
        quarantine_limitations_text()
    ]
    return NotificationMessage(
        title="Quarantine Review",
        body="\n".join(lines),
        notification_type=NotificationType.QUARANTINE_REPORT,
        level="INFO" if summary['error_count'] == 0 else "WARNING",
        metadata={"review_id": review.review_id}
    )

def format_promotion_ticket_warning_message(tickets: list['ReadOnlyPromotionTicket']) -> NotificationMessage:
    from usa_signal_bot.paper_quarantine.enrollment_report import quarantine_limitations_text
    count = len(tickets)

    lines = [
        f"⚠️ Promotion Ticket Warning ⚠️",
        f"{count} tickets require attention.",
        "",
        quarantine_limitations_text()
    ]
    return NotificationMessage(
        title="Promotion Ticket Warning",
        body="\n".join(lines),
        notification_type=NotificationType.PROMOTION_TICKET_WARNING,
        level="WARNING",
        metadata={"count": count}
    )

def format_dry_run_bridge_warning_message(plans: list['SupervisedDryRunBridgePlan']) -> NotificationMessage:
    from usa_signal_bot.paper_quarantine.enrollment_report import quarantine_limitations_text
    count = len(plans)

    lines = [
        f"⚠️ Dry Run Bridge Warning ⚠️",
        f"{count} bridge plans require attention.",
        "",
        quarantine_limitations_text()
    ]
    return NotificationMessage(
        title="Dry Run Bridge Warning",
        body="\n".join(lines),
        notification_type=NotificationType.DRY_RUN_BRIDGE_WARNING,
        level="WARNING",
        metadata={"count": count}
    )

def notifications_from_quarantine_review(review: 'QuarantineEnrollmentReview') -> list[NotificationMessage]:
    messages = []
    messages.append(format_quarantine_report_message(review))

    problem_tickets = [t for t in review.tickets if t.status.value == "blocked" or not t.read_only]
    if problem_tickets:
         messages.append(format_promotion_ticket_warning_message(problem_tickets))

    problem_plans = [p for p in review.bridge_plans if p.status.value == "blocked" or p.paper_state_mutation_enabled]
    if problem_plans:
         messages.append(format_dry_run_bridge_warning_message(problem_plans))

    return messages
