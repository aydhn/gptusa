from typing import Any, List
from usa_signal_bot.paper_controlled_planning.planning_models import FinalHumanApprovalQueueItem
from usa_signal_bot.core.enums import ApprovalQueueDecision

def build_approval_history(items: List[FinalHumanApprovalQueueItem]) -> List[dict[str, Any]]:
    # Sort chronologically
    sorted_items = sorted(items, key=lambda x: x.created_at_utc)
    return [
        {
            "queue_item_id": i.queue_item_id,
            "created_at_utc": i.created_at_utc,
            "status": i.status.value,
            "decision": i.decision.value,
            "has_notes": bool(i.reviewer_notes)
        }
        for i in sorted_items
    ]

def latest_approval_decision(items: List[FinalHumanApprovalQueueItem]) -> ApprovalQueueDecision:
    if not items:
        return ApprovalQueueDecision.UNKNOWN
    sorted_items = sorted(items, key=lambda x: x.created_at_utc, reverse=True)
    return sorted_items[0].decision

def approval_history_warnings(items: List[FinalHumanApprovalQueueItem]) -> List[str]:
    warnings = []
    if not items:
        warnings.append("No approval history items found.")
    else:
        latest = sorted(items, key=lambda x: x.created_at_utc, reverse=True)[0]
        if not latest.reviewer_notes:
            warnings.append(f"Latest approval item {latest.queue_item_id} is missing reviewer notes.")
        if latest.decision in [ApprovalQueueDecision.BLOCK, ApprovalQueueDecision.REJECT]:
            warnings.append(f"Latest approval item {latest.queue_item_id} decision is {latest.decision.value}.")
    return warnings

def approval_history_summary(items: List[FinalHumanApprovalQueueItem]) -> dict[str, Any]:
    return {
        "history_count": len(items),
        "latest_decision": latest_approval_decision(items).value,
        "warnings": approval_history_warnings(items)
    }

def approval_history_to_text(items: List[FinalHumanApprovalQueueItem], limit: int = 100) -> str:
    summary = approval_history_summary(items)
    lines = [
        "📜 APPROVAL HISTORY",
        f"Items: {summary['history_count']}",
        f"Latest Decision: {summary['latest_decision']}"
    ]
    if summary["warnings"]:
        lines.append("WARNINGS:")
        for w in summary["warnings"]:
            lines.append(f" - {w}")
    return "\n".join(lines)
