from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import FinalHumanApprovalQueueItem

def register_approval_queue_item(item: FinalHumanApprovalQueueItem, registry: Optional[List[FinalHumanApprovalQueueItem]] = None) -> List[FinalHumanApprovalQueueItem]:
    if registry is None:
        registry = []
    registry.append(item)
    return registry

def find_approval_item_by_id(registry: List[FinalHumanApprovalQueueItem], queue_item_id: str) -> Optional[FinalHumanApprovalQueueItem]:
    for item in registry:
        if item.queue_item_id == queue_item_id:
            return item
    return None

def find_approval_items_by_candidate_id(registry: List[FinalHumanApprovalQueueItem], candidate_id: str) -> List[FinalHumanApprovalQueueItem]:
    return [i for i in registry if i.candidate_id == candidate_id]

def latest_approval_item_for_candidate(registry: List[FinalHumanApprovalQueueItem], candidate_id: str) -> Optional[FinalHumanApprovalQueueItem]:
    items = find_approval_items_by_candidate_id(registry, candidate_id)
    if not items:
        return None
    # Sort by created_at descending
    return sorted(items, key=lambda x: x.created_at_utc, reverse=True)[0]

def approval_queue_registry_summary(registry: List[FinalHumanApprovalQueueItem]) -> dict[str, Any]:
    return {
        "total_items": len(registry),
        "queued": len([i for i in registry if i.status.value == "QUEUED"]),
        "approved": len([i for i in registry if i.status.value == "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE"]),
        "rejected": len([i for i in registry if i.status.value == "REJECTED"]),
        "blocked": len([i for i in registry if i.status.value == "BLOCKED"])
    }

def approval_queue_registry_to_text(registry: List[FinalHumanApprovalQueueItem], limit: int = 100) -> str:
    summary = approval_queue_registry_summary(registry)
    lines = [
        "📋 APPROVAL QUEUE REGISTRY",
        f"Total Items: {summary['total_items']}",
        f"Queued: {summary['queued']}",
        f"Approved: {summary['approved']}",
        f"Rejected: {summary['rejected']}",
        f"Blocked: {summary['blocked']}"
    ]
    return "\n".join(lines)
