from typing import Any, Dict, List
from dataclasses import dataclass
from usa_signal_bot.core.enums import NotificationType
from usa_signal_bot.paper_observer.observer_models import PaperObserverReview, ObserverRuntimeSession, ObserverDriftEvent

@dataclass
class NotificationMessage:
    type: str
    message: str
    payload: Dict[str, Any]

def format_paper_observer_report_message(review: PaperObserverReview) -> NotificationMessage:
    msg = f"Paper Observer Review {review.review_id} generated. Sessions: {len(review.sessions)}. NOT INVESTMENT ADVICE."
    return NotificationMessage(type=NotificationType.PAPER_OBSERVER_REPORT.value, message=msg, payload={"review_id": review.review_id})

def format_observer_runtime_warning_message(sessions: List[ObserverRuntimeSession]) -> NotificationMessage:
    msg = f"Observer Runtime Warning on {len(sessions)} sessions."
    return NotificationMessage(type=NotificationType.OBSERVER_RUNTIME_WARNING.value, message=msg, payload={"count": len(sessions)})

def format_observer_drift_warning_message(events: List[ObserverDriftEvent]) -> NotificationMessage:
    msg = f"Observer Drift Warning: {len(events)} events detected."
    return NotificationMessage(type=NotificationType.OBSERVER_DRIFT_WARNING.value, message=msg, payload={"count": len(events)})

def notifications_from_paper_observer_review(review: PaperObserverReview) -> List[NotificationMessage]:
    messages = [format_paper_observer_report_message(review)]

    warn_sessions = [s for s in review.sessions if s.warnings]
    if warn_sessions:
        messages.append(format_observer_runtime_warning_message(warn_sessions))

    if review.drift_events:
        messages.append(format_observer_drift_warning_message(review.drift_events))

    return messages


def format_readiness_rehearsal_report_message(review: Any) -> NotificationMessage:
    msg = f"Readiness Rehearsal Review {getattr(review, 'review_id', 'UNKNOWN')} generated. No broker execution."
    return NotificationMessage(type=NotificationType.READINESS_REHEARSAL_REPORT.value, message=msg, payload={"review_id": getattr(review, 'review_id', 'UNKNOWN')})

def format_final_review_lock_warning_message(locks: List[Any]) -> NotificationMessage:
    msg = f"Final Review Lock Warning: {len(locks)} locks blocked."
    return NotificationMessage(type=NotificationType.FINAL_REVIEW_LOCK_WARNING.value, message=msg, payload={"count": len(locks)})

def format_guarded_handoff_warning_message(entries: List[Any]) -> NotificationMessage:
    msg = f"Guarded Handoff Warning: {len(entries)} handoffs blocked."
    return NotificationMessage(type=NotificationType.GUARDED_HANDOFF_WARNING.value, message=msg, payload={"count": len(entries)})

def notifications_from_readiness_rehearsal_review(review: Any) -> List[NotificationMessage]:
    messages = [format_readiness_rehearsal_report_message(review)]
    return messages
