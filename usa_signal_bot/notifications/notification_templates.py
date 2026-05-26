
from typing import List, Dict, Any
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeFullReview,
    MultiProviderFinalReviewReport,
    DataLayerRehearsalReport
)

class NotificationMessage:
    def __init__(self, title: str, body: str, type: str):
        self.title = title
        self.body = body
        self.type = type

def format_provider_freeze_report_message(review: ProviderFreezeFullReview) -> NotificationMessage:
    return NotificationMessage(
        title=f"Provider Freeze Report: {review.review_id}",
        body=f"Ready for Phase 115: {review.context.ready_for_phase115}. Validation status: {review.freeze_bundle.freeze_valid}",
        type="PROVIDER_FREEZE_REPORT"
    )

def format_multi_provider_review_warning_message(report: MultiProviderFinalReviewReport) -> NotificationMessage:
    return NotificationMessage(
        title="Multi-Provider Review Warning",
        body=f"Warning items found: {report.warning_items}, Failed: {report.failed_items}",
        type="MULTI_PROVIDER_REVIEW_WARNING"
    )

def format_data_layer_rehearsal_warning_message(report: DataLayerRehearsalReport) -> NotificationMessage:
    return NotificationMessage(
        title="Data Layer Rehearsal Warning",
        body=f"Failed scenarios: {report.failed_scenarios}, Warning scenarios: {report.warning_scenarios}",
        type="DATA_LAYER_REHEARSAL_WARNING"
    )

def notifications_from_provider_freeze_review(review: ProviderFreezeFullReview) -> List[NotificationMessage]:
    msgs = [format_provider_freeze_report_message(review)]
    if not review.multi_provider_review.multi_provider_review_passed or review.multi_provider_review.warning_items > 0:
        msgs.append(format_multi_provider_review_warning_message(review.multi_provider_review))
    if not review.rehearsal_report.rehearsal_passed or review.rehearsal_report.warning_scenarios > 0:
        msgs.append(format_data_layer_rehearsal_warning_message(review.rehearsal_report))
    return msgs
