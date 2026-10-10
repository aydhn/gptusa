# mock adapters file
from dataclasses import dataclass
from typing import Any, List


@dataclass
class NotificationMessage:
    """Lightweight, local-only notification preview (never sent anywhere)."""
    type: str = ""
    title: str = ""
    body: str = ""


def format_paper_observer_report_message(review: Any) -> NotificationMessage:
    body = (
        f"Paper observer review: {getattr(review, 'review_id', 'unknown')}. "
        "Read-only observation, no execution. NOT investment advice."
    )
    return NotificationMessage(type="paper_observer_report", title="Paper Observer Report", body=body)


def notifications_from_paper_observer_review(review: Any) -> List[NotificationMessage]:
    return [format_paper_observer_report_message(review)]
