from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    HumanReviewChecklistItem,
    ReviewerNote,
    ActivationStillDeniedRegistryEntry,
    ReadinessConfirmationAuditEntry,
    ReadinessConfirmationReview
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import confirmation_queue_item_to_text
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import human_review_bundle_to_text
from usa_signal_bot.paper_readiness_confirmation.review_checklist import checklist_to_text
from usa_signal_bot.paper_readiness_confirmation.reviewer_notes import reviewer_note_to_text
from usa_signal_bot.paper_readiness_confirmation.activation_denied_registry import activation_denied_registry_to_text
from usa_signal_bot.paper_readiness_confirmation.confirmation_audit import readiness_confirmation_audit_to_text
from usa_signal_bot.paper_readiness_confirmation.confirmation_report import readiness_confirmation_review_to_text, readiness_confirmation_limitations_text

def readiness_confirmation_queue_item_to_text(item: ReadinessConfirmationQueueItem) -> str:
    return confirmation_queue_item_to_text(item)

def human_review_bundle_to_text_report(item: HumanReviewBundle, limit: int = 100) -> str:
    return human_review_bundle_to_text(item, limit)

def human_review_checklist_item_to_text(item: HumanReviewChecklistItem) -> str:
    return f"Checklist Item: {item.title}, Status: {item.status.value}"

def reviewer_note_to_text_report(item: ReviewerNote) -> str:
    return reviewer_note_to_text(item)

def activation_still_denied_registry_entry_to_text(item: ActivationStillDeniedRegistryEntry) -> str:
    return f"Registry Entry: {item.registry_entry_id}, Status: {item.status.value}"

def readiness_confirmation_audit_entry_to_text(item: ReadinessConfirmationAuditEntry) -> str:
    return f"Audit Entry: {item.audit_id}, Action: {item.action}"

def readiness_confirmation_review_to_text_report(item: ReadinessConfirmationReview, limit: int = 100) -> str:
    return readiness_confirmation_review_to_text(item, limit)

def readiness_confirmation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Confirmation Store Summary: {summary}"
