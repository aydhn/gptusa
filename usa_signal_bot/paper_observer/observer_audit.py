from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ObserverSafetyFlag
from usa_signal_bot.paper_observer.observer_models import (
    ObserverAuditEntry,
    PaperObserverEnrollment,
    ObserverRuntimeSession,
    create_observer_audit_id,
)

from dataclasses import dataclass


@dataclass
class ObserverAuditEntryParams:
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: Optional[List[str]] = None
    safety_flags: Optional[List[ObserverSafetyFlag]] = None


def create_observer_audit_entry(params: ObserverAuditEntryParams) -> ObserverAuditEntry:
    return ObserverAuditEntry(
        audit_id=create_observer_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        entity_type=params.entity_type,
        entity_id=params.entity_id,
        action=params.action,
        rationale=params.rationale,
        evidence_refs=params.evidence_refs or [],
        safety_flags=params.safety_flags or [],
        warnings=[],
        errors=[],
        metadata={},
    )


def audit_entry_from_observer_enrollment(
    enrollment: PaperObserverEnrollment,
) -> ObserverAuditEntry:
    return create_observer_audit_entry(
        ObserverAuditEntryParams(
            entity_type="PaperObserverEnrollment",
            entity_id=enrollment.enrollment_id,
            action="ENROLLMENT_CREATED",
            rationale=f"Candidate {enrollment.candidate_id} enrolled with status {enrollment.status.value}",
            evidence_refs=(
                [enrollment.planning_ticket_id] if enrollment.planning_ticket_id else []
            ),
            safety_flags=enrollment.safety_flags,
        )
    )


def audit_entry_from_observer_session(
    session: ObserverRuntimeSession,
) -> ObserverAuditEntry:
    return create_observer_audit_entry(
        ObserverAuditEntryParams(
            entity_type="ObserverRuntimeSession",
            entity_id=session.session_id,
            action="SESSION_COMPLETED",
            rationale=f"Session completed with {len(session.outputs)} outputs and {len(session.drift_events)} drift events",
            evidence_refs=[session.context.context_id] if session.context else [],
            safety_flags=session.safety_flags,
        )
    )


def append_observer_audit_entry(
    entries: List[ObserverAuditEntry], entry: ObserverAuditEntry
) -> List[ObserverAuditEntry]:
    entries.append(entry)
    return entries


def observer_audit_summary(entries: List[ObserverAuditEntry]) -> Dict[str, Any]:
    return {"audit_count": len(entries)}


def observer_audit_to_text(entries: List[ObserverAuditEntry], limit: int = 100) -> str:
    return f"Audit log contains {len(entries)} entries."
