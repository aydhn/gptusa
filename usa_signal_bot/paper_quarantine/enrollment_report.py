import datetime
from typing import Any

from usa_signal_bot.core.enums import QuarantineReportType
from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantineEnrollmentReview,
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
    create_quarantine_review_id,
    validate_quarantine_enrollment_review,
)
from usa_signal_bot.paper_quarantine.enrollment_safety import validate_quarantine_enrollment_safety

def build_quarantine_enrollment_review(
    candidate: QuarantinedPaperCandidate,
    ticket: ReadOnlyPromotionTicket | None = None,
    bridge_plan: SupervisedDryRunBridgePlan | None = None
) -> QuarantineEnrollmentReview:

    safety_errors = validate_quarantine_enrollment_safety(candidate, ticket, bridge_plan)

    review = QuarantineEnrollmentReview(
        review_id=create_quarantine_review_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_type=QuarantineReportType.ENROLLMENT_REVIEW,
        candidates=[candidate],
        tickets=[ticket] if ticket else [],
        bridge_plans=[bridge_plan] if bridge_plan else [],
        audit_entries=[],
        output_paths={"quarantine": bridge_plan.quarantine_output_path if bridge_plan else "unknown"},
        warnings=[],
        errors=safety_errors
    )
    validate_quarantine_enrollment_review(review)
    return review

def quarantine_review_summary(review: QuarantineEnrollmentReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "report_type": review.report_type.value,
        "candidate_count": len(review.candidates),
        "ticket_count": len(review.tickets),
        "bridge_plan_count": len(review.bridge_plans),
        "error_count": len(review.errors),
    }

def quarantine_limitations_text() -> str:
    lines = [
        "--- QUARANTINE LIMITATIONS ---",
        "1. No broker / live / demo order execution.",
        "2. No active paper enable or state mutation.",
        "3. No Telegram real send.",
        "4. No production config patch.",
        "5. Quarantine is strictly local governance metadata.",
        "6. This report is NOT investment advice.",
        "------------------------------"
    ]
    return "\n".join(lines)

def quarantine_enrollment_review_to_text(review: QuarantineEnrollmentReview, limit: int = 100) -> str:
    summary = quarantine_review_summary(review)
    lines = [
        f"Quarantine Enrollment Review: {summary['review_id']}",
        f"Type: {summary['report_type']}",
        f"Candidates: {summary['candidate_count']}, Tickets: {summary['ticket_count']}, Bridge Plans: {summary['bridge_plan_count']}",
        f"Errors: {summary['error_count']}",
        quarantine_limitations_text()
    ]
    return "\n".join(lines)
