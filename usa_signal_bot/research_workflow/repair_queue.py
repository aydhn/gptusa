from typing import Any, List, Optional
import datetime
from .workflow_models import RepairQueueItem, create_repair_queue_item_id
from ..core.enums import RepairItemType, RepairPriority, RepairStatus

def create_repair_item_from_failure_assessment(assessment_payload: dict[str, Any]) -> RepairQueueItem:
    item_id = create_repair_queue_item_id()
    now_utc = datetime.datetime.utcnow().isoformat() + "Z"

    target_name = assessment_payload.get("target_name", "unknown")
    failure_mode = assessment_payload.get("failure_mode", "unknown")
    severity = assessment_payload.get("severity")

    return RepairQueueItem(
        item_id=item_id,
        created_at_utc=now_utc,
        item_type=RepairItemType.UNKNOWN,
        priority=repair_item_priority_from_severity(severity),
        status=RepairStatus.NEW,
        target_scope=assessment_payload.get("target_scope"),
        target_name=target_name,
        title=f"Repair {target_name} for {failure_mode}",
        description=assessment_payload.get("description", "Auto-generated repair item from failure assessment."),
        source_failure_modes=[failure_mode],
        evidence_refs=[assessment_payload.get("assessment_id", "unknown")],
        diagnostic_severity=severity,
        evidence_quality=assessment_payload.get("evidence_quality"),
        suggested_safe_action=assessment_payload.get("suggested_remediation", "Review and investigate"),
        linked_hypothesis_ids=[],
        warnings=[],
        errors=[],
        metadata={"assessment_payload": assessment_payload}
    )

def create_repair_items_from_diagnostics(diagnostic_payload: dict[str, Any]) -> List[RepairQueueItem]:
    items = []
    assessments = diagnostic_payload.get("failure_assessments", [])
    for assessment in assessments:
        items.append(create_repair_item_from_failure_assessment(assessment))
    return deduplicate_repair_items(items)

def triage_repair_item(item: RepairQueueItem) -> RepairQueueItem:
    if item.status == RepairStatus.NEW:
        item.status = RepairStatus.TRIAGED
    return item

def update_repair_item_status(item: RepairQueueItem, status: RepairStatus, rationale: Optional[str] = None) -> RepairQueueItem:
    item.status = status
    if rationale:
        item.metadata["status_change_rationale"] = rationale
    return item

def repair_item_priority_from_severity(severity: Optional[str], evidence_quality: Optional[str] = None) -> RepairPriority:
    if not severity:
        return RepairPriority.UNKNOWN

    sev_upper = severity.upper()
    if sev_upper in ["CRITICAL", "FATAL"]:
        return RepairPriority.CRITICAL if evidence_quality != "LOW" else RepairPriority.HIGH
    elif sev_upper == "HIGH":
        return RepairPriority.HIGH
    elif sev_upper in ["MEDIUM", "MODERATE"]:
        return RepairPriority.MEDIUM
    elif sev_upper == "LOW":
        return RepairPriority.LOW
    return RepairPriority.UNKNOWN

def deduplicate_repair_items(items: List[RepairQueueItem]) -> List[RepairQueueItem]:
    deduped = {}
    for item in items:
        key = (item.target_name, tuple(sorted(item.source_failure_modes)))
        if key not in deduped:
            deduped[key] = item
        else:
            existing = deduped[key]
            existing.evidence_refs = list(set(existing.evidence_refs + item.evidence_refs))
            if item.priority == RepairPriority.CRITICAL and existing.priority != RepairPriority.CRITICAL:
                existing.priority = RepairPriority.CRITICAL
    return list(deduped.values())

def repair_queue_summary(items: List[RepairQueueItem]) -> dict[str, Any]:
    return {
        "total_items": len(items),
        "by_priority": {p.value: len([i for i in items if i.priority == p]) for p in RepairPriority},
        "by_status": {s.value: len([i for i in items if i.status == s]) for s in RepairStatus}
    }

def repair_queue_to_text(items: List[RepairQueueItem], limit: int = 100) -> str:
    summary = repair_queue_summary(items)
    lines = [f"Repair Queue Summary: {summary['total_items']} total items", "-"*40]

    for item in items[:limit]:
        lines.append(f"[{item.priority.value}] {item.title} ({item.status.value})")
        lines.append(f"  Target: {item.target_name} | Scope: {item.target_scope}")
        lines.append(f"  Suggested: {item.suggested_safe_action}")
        lines.append("")

    if len(items) > limit:
        lines.append(f"... and {len(items) - limit} more items.")

    return "\n".join(lines)
