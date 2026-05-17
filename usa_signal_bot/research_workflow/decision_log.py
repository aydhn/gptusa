from typing import Any, List, Optional
import datetime
from .workflow_models import ResearchDecisionLogEntry, create_research_decision_log_entry_id

def create_decision_log_entry(entity_type: str, entity_id: str, decision: str, rationale: str, evidence_refs: Optional[List[str]] = None, made_by: str = "local_research_workflow") -> ResearchDecisionLogEntry:
    return ResearchDecisionLogEntry(
        entry_id=create_research_decision_log_entry_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        entity_type=entity_type,
        entity_id=entity_id,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        made_by=made_by,
        warnings=[],
        errors=[],
        metadata={}
    )

def decision_log_for_status_change(entity_type: str, entity_id: str, old_status: str, new_status: str, rationale: Optional[str] = None) -> ResearchDecisionLogEntry:
    return create_decision_log_entry(
        entity_type=entity_type,
        entity_id=entity_id,
        decision=f"Status changed from {old_status} to {new_status}",
        rationale=rationale or "Workflow progression"
    )

def append_decision_log(entries: List[ResearchDecisionLogEntry], entry: ResearchDecisionLogEntry) -> List[ResearchDecisionLogEntry]:
    return entries + [entry]

def decision_log_summary(entries: List[ResearchDecisionLogEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "by_entity_type": {et: len([e for e in entries if e.entity_type == et]) for et in set(e.entity_type for e in entries)}
    }

def decision_log_to_text(entries: List[ResearchDecisionLogEntry], limit: int = 100) -> str:
    lines = [f"Decision Log: {len(entries)} entries", "-"*40]
    for e in entries[:limit]:
        lines.append(f"[{e.created_at_utc}] {e.entity_type} {e.entity_id} -> {e.decision}")
        lines.append(f"  Rationale: {e.rationale}")
        lines.append("")
    if len(entries) > limit:
        lines.append(f"... and {len(entries) - limit} more.")
    return "\n".join(lines)
