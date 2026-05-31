from typing import Any, Dict
from ..ml_research.foundation.phase136_models import MLFoundationFullReview

class NotificationMessage:
    def __init__(self, message: str):
        self.message = message

def format_ml_foundation_report_message(review: MLFoundationFullReview) -> NotificationMessage:
    return NotificationMessage(f"ML Foundation Review {review.review_id} generated. Ready for Phase 137: {review.readiness_gate.ready_for_phase137}.")

def notifications_from_ml_foundation_review(review: MLFoundationFullReview) -> list[NotificationMessage]:
    return [format_ml_foundation_report_message(review)]
