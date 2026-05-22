from typing import Any
import datetime

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationReview,
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    ActivationStillDeniedRegistryEntry,
    create_readiness_confirmation_review_id
)
from usa_signal_bot.core.enums import ReadinessConfirmationReportType

def build_readiness_confirmation_review(
    queue_item: ReadinessConfirmationQueueItem,
    bundle: HumanReviewBundle | None = None,
    registry_entry: ActivationStillDeniedRegistryEntry | None = None
) -> ReadinessConfirmationReview:

    return ReadinessConfirmationReview(
        review_id=create_readiness_confirmation_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=ReadinessConfirmationReportType.FULL_READINESS_CONFIRMATION_REVIEW,
        queue_items=[queue_item] if queue_item else [],
        bundles=[bundle] if bundle else [],
        checklist_items=[],
        reviewer_notes=[],
        registry_entries=[registry_entry] if registry_entry else [],
        audit_entries=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def readiness_confirmation_review_summary(review: ReadinessConfirmationReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "type": review.report_type.value,
        "queues": len(review.queue_items),
        "bundles": len(review.bundles),
        "registry_entries": len(review.registry_entries),
        "limitations": readiness_confirmation_limitations_text()
    }

def readiness_confirmation_limitations_text() -> str:
    return (
        "Readiness confirmation is local metadata only.\n"
        "No broker/live/demo order.\n"
        "No active paper enable.\n"
        "No real paper mutation.\n"
        "No Telegram real send.\n"
        "No production config patch.\n"
        "Human review bundle is not activation.\n"
        "Activation-still-denied registry is not activation.\n"
        "Not investment advice."
    )

def readiness_confirmation_review_to_text(review: ReadinessConfirmationReview, limit: int = 100) -> str:
    summary = readiness_confirmation_review_summary(review)
    return f"Review: {summary['review_id']}\nLimitations: {summary['limitations']}"
