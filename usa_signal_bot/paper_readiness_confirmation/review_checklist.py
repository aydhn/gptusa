from typing import Any
import datetime

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    HumanReviewChecklistItem,
    ReadinessConfirmationQueueItem,
    create_human_review_checklist_item_id
)
from usa_signal_bot.core.enums import ReviewChecklistItemStatus

def _build_base_item(title: str, desc: str) -> HumanReviewChecklistItem:
     return HumanReviewChecklistItem(
        checklist_item_id=create_human_review_checklist_item_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        category="SAFETY",
        title=title,
        status=ReviewChecklistItemStatus.NOT_REVIEWED,
        observed_value=None,
        expected_value=True,
        description=desc,
        required=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_human_review_checklist_items(queue_item: ReadinessConfirmationQueueItem, firewall_audit_payload: dict[str, Any] | None = None) -> list[HumanReviewChecklistItem]:
    return [
        checklist_item_activation_denied(queue_item),
        checklist_item_zero_mutation_confirmed(queue_item),
        checklist_item_firewall_replay_confirmed(queue_item),
        checklist_item_no_broker_execution(queue_item),
        checklist_item_no_paper_state_mutation(queue_item),
        checklist_item_no_config_patch(queue_item),
        checklist_item_no_telegram_real_send(queue_item)
    ]

def checklist_item_activation_denied(queue_item: ReadinessConfirmationQueueItem) -> HumanReviewChecklistItem:
    return _build_base_item("Activation Denied Confirmed", "Ensure that activation remains denied.")

def checklist_item_zero_mutation_confirmed(queue_item: ReadinessConfirmationQueueItem) -> HumanReviewChecklistItem:
    return _build_base_item("Zero Mutation Audit Passed", "Ensure that the zero mutation audit passed successfully.")

def checklist_item_firewall_replay_confirmed(queue_item: ReadinessConfirmationQueueItem) -> HumanReviewChecklistItem:
     return _build_base_item("Firewall Replay Passed", "Ensure that the firewall replay executed and passed.")

def checklist_item_no_broker_execution(queue_item: ReadinessConfirmationQueueItem) -> HumanReviewChecklistItem:
     return _build_base_item("No Broker Execution", "Confirm no live or demo broker orders will be generated.")

def checklist_item_no_paper_state_mutation(queue_item: ReadinessConfirmationQueueItem) -> HumanReviewChecklistItem:
     return _build_base_item("No Paper State Mutation", "Confirm no paper state mutation will occur.")

def checklist_item_no_config_patch(queue_item: ReadinessConfirmationQueueItem) -> HumanReviewChecklistItem:
     return _build_base_item("No Config Patch", "Confirm no production config patches will be applied.")

def checklist_item_no_telegram_real_send(queue_item: ReadinessConfirmationQueueItem) -> HumanReviewChecklistItem:
     return _build_base_item("No Telegram Real Send", "Confirm no real Telegram messages will be dispatched.")

def checklist_summary(items: list[HumanReviewChecklistItem]) -> dict[str, Any]:
    counts = {s.value: 0 for s in ReviewChecklistItemStatus}
    for item in items:
        counts[item.status.value] = counts.get(item.status.value, 0) + 1
    return counts

def checklist_to_text(items: list[HumanReviewChecklistItem], limit: int = 100) -> str:
    summary = checklist_summary(items)
    return f"Checklist Summary: {summary}"
