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
