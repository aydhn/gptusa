from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningAuditEntry,
    ControlledPlanningTicket,
    FinalHumanApprovalQueueItem,
    create_controlled_planning_audit_id,
    _now_str
)
from usa_signal_bot.core.enums import ControlledPlanningSafetyFlag

def create_controlled_planning_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    safety_flags: Optional[List[ControlledPlanningSafetyFlag]] = None
) -> ControlledPlanningAuditEntry:
    return ControlledPlanningAuditEntry(
        audit_id=create_controlled_planning_audit_id(),
        created_at_utc=_now_str(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        safety_flags=safety_flags or [],
        warnings=[],
        errors=[],
        metadata={}
    )

def audit_entry_from_planning_ticket(ticket: ControlledPlanningTicket) -> ControlledPlanningAuditEntry:
    return create_controlled_planning_audit_entry(
        entity_type="CONTROLLED_PLANNING_TICKET",
        entity_id=ticket.ticket_id,
        action="CREATE_TICKET",
        rationale="Generated from observation exit review",
        decision=ticket.status.value,
        evidence_refs=ticket.evidence_refs,
        safety_flags=ticket.safety_flags
    )

def audit_entry_from_approval_queue_item(item: FinalHumanApprovalQueueItem) -> ControlledPlanningAuditEntry:
    return create_controlled_planning_audit_entry(
        entity_type="FINAL_HUMAN_APPROVAL_QUEUE_ITEM",
        entity_id=item.queue_item_id,
        action="HUMAN_APPROVAL_REVIEW",
        rationale=item.reviewer_notes or "No notes provided",
        decision=item.decision.value,
        evidence_refs=item.required_evidence_refs,
        safety_flags=item.safety_flags
    )

def append_controlled_planning_audit_entry(entries: List[ControlledPlanningAuditEntry], entry: ControlledPlanningAuditEntry) -> List[ControlledPlanningAuditEntry]:
    entries.append(entry)
    return entries

def controlled_planning_audit_summary(entries: List[ControlledPlanningAuditEntry]) -> dict[str, Any]:
    return {
        "audit_count": len(entries),
        "actions": list(set(e.action for e in entries))
    }

def controlled_planning_audit_to_text(entries: List[ControlledPlanningAuditEntry], limit: int = 100) -> str:
    lines = [
        "📑 CONTROLLED PLANNING AUDIT",
        f"Entries: {len(entries)}"
    ]
    for e in sorted(entries, key=lambda x: x.created_at_utc, reverse=True)[:limit]:
        lines.append(f" - [{e.created_at_utc}] {e.entity_type} {e.entity_id}: {e.action} -> {e.decision or 'N/A'}")
    lines.append("LIMITATION: Audit trails are strictly local and redact sensitive data. They DO NOT trigger telemetry.")
    return "\n".join(lines)
