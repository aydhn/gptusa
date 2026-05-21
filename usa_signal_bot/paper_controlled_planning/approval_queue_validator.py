from typing import Any, List
from usa_signal_bot.paper_controlled_planning.planning_models import FinalHumanApprovalQueueItem
from usa_signal_bot.core.enums import ApprovalQueueItemStatus

def validate_approval_queue_item_safety(item: FinalHumanApprovalQueueItem) -> List[str]:
    errors = []
    if item.allows_active_paper:
        errors.append("Item allows_active_paper is True")
    if item.allows_broker_execution:
        errors.append("Item allows_broker_execution is True")
    if item.allows_paper_state_mutation:
        errors.append("Item allows_paper_state_mutation is True")
    if item.allows_config_patch:
        errors.append("Item allows_config_patch is True")
    return errors

def approval_item_requires_followup(item: FinalHumanApprovalQueueItem) -> bool:
    return item.status in [ApprovalQueueItemStatus.REQUEST_CHANGES, ApprovalQueueItemStatus.REJECTED, ApprovalQueueItemStatus.BLOCKED]

def approval_item_has_required_notes(item: FinalHumanApprovalQueueItem) -> bool:
    return bool(item.reviewer_notes and len(item.reviewer_notes.strip()) > 0)

def approval_item_blocks_next_stage(item: FinalHumanApprovalQueueItem) -> bool:
    return item.status in [ApprovalQueueItemStatus.BLOCKED, ApprovalQueueItemStatus.REJECTED]

def approval_queue_validator_summary(item: FinalHumanApprovalQueueItem) -> dict[str, Any]:
    safety_errors = validate_approval_queue_item_safety(item)
    return {
        "queue_item_id": item.queue_item_id,
        "is_safe": len(safety_errors) == 0,
        "has_notes": approval_item_has_required_notes(item),
        "blocks_next_stage": approval_item_blocks_next_stage(item)
    }

def approval_queue_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [
        "🔍 APPROVAL QUEUE VALIDATOR",
        f"Item ID: {payload.get('queue_item_id', 'Unknown')}",
        f"Is Safe: {payload.get('is_safe', False)}",
        f"Has Notes: {payload.get('has_notes', False)}",
        f"Blocks Next Stage: {payload.get('blocks_next_stage', False)}"
    ]
    return "\n".join(lines)
