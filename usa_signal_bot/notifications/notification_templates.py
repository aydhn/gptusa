from typing import Any, Dict
from ..ml_research.foundation.phase136_models import MLFoundationFullReview

class NotificationMessage:
    def __init__(self, message: str):
        self.message = message

def format_ml_foundation_report_message(review: MLFoundationFullReview) -> NotificationMessage:
    return NotificationMessage(f"ML Foundation Review {review.review_id} generated. Ready for Phase 137: {review.readiness_gate.ready_for_phase137}.")

def notifications_from_ml_foundation_review(review: MLFoundationFullReview) -> list[NotificationMessage]:
    return [format_ml_foundation_report_message(review)]


def format_ml_dataset_assembly_report_message(review: 'Any') -> 'Any':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType
    import uuid
    from datetime import datetime, timezone
    now_str = datetime.now(timezone.utc).isoformat()
    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:12]}",
        created_at_utc=now_str,
        notification_type=NotificationType.ML_DATASET_ASSEMBLY_REPORT,
        subject="ML Dataset Assembly Report",
        body=f"ML Dataset Assembly Report ID: {review.review_id}",
        severity="INFO",
        metadata={"review_id": review.review_id}
    )

def format_ml_leakage_audit_warning_message(result: 'Any') -> 'Any':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType
    import uuid
    from datetime import datetime, timezone
    now_str = datetime.now(timezone.utc).isoformat()
    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:12]}",
        created_at_utc=now_str,
        notification_type=NotificationType.ML_LEAKAGE_AUDIT_WARNING,
        subject="ML Leakage Audit Warning",
        body=f"ML Leakage Audit Warnings/Failures detected in Audit ID: {result.audit_id}",
        severity="WARNING",
        metadata={"audit_id": result.audit_id}
    )

def format_ml_split_quality_warning_message(profile: 'Any') -> 'Any':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType
    import uuid
    from datetime import datetime, timezone
    now_str = datetime.now(timezone.utc).isoformat()
    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:12]}",
        created_at_utc=now_str,
        notification_type=NotificationType.ML_SPLIT_QUALITY_WARNING,
        subject="ML Split Quality Warning",
        body=f"ML Split Quality is Low/Warning in Profile ID: {profile.profile_id}. Score: {profile.score}",
        severity="WARNING",
        metadata={"profile_id": profile.profile_id}
    )

def notifications_from_ml_dataset_assembly_review(review: 'Any') -> list:
    msgs = [format_ml_dataset_assembly_report_message(review)]
    if review.leakage_audit and (review.leakage_audit.failed_rules > 0 or review.leakage_audit.warning_rules > 0):
        msgs.append(format_ml_leakage_audit_warning_message(review.leakage_audit))
    if review.split_quality_profile and review.split_quality_profile.score < 80.0:
        msgs.append(format_ml_split_quality_warning_message(review.split_quality_profile))
    return msgs
