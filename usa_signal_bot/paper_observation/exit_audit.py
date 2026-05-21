from typing import Any, List, Optional
from usa_signal_bot.paper_observation.observation_models import ObservationAuditEntry, QuarantineExitReview, ObservationRiskFlag, create_observation_audit_id
import datetime

def create_observation_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: List[str] | None = None,
    risk_flags: List[ObservationRiskFlag] | None = None
) -> ObservationAuditEntry:
    return ObservationAuditEntry(
        audit_id=create_observation_audit_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[],
        metadata={}
    )

def audit_entry_from_exit_review(exit_review: QuarantineExitReview) -> ObservationAuditEntry:
    return create_observation_audit_entry(
        entity_type="QuarantineExitReview",
        entity_id=exit_review.exit_review_id,
        action="QUARANTINE_EXIT_DECISION",
        rationale=exit_review.rationale,
        decision=exit_review.decision,
        evidence_refs=[exit_review.scorecard.scorecard_id] if exit_review.scorecard else [],
        risk_flags=exit_review.risk_flags
    )

def append_observation_audit_entry(entries: List[ObservationAuditEntry], entry: ObservationAuditEntry) -> List[ObservationAuditEntry]:
    # Append-only
    return entries + [entry]

def observation_audit_summary(entries: List[ObservationAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "latest_audit_id": entries[-1].audit_id if entries else None
    }

def observation_audit_to_text(entries: List[ObservationAuditEntry], limit: int = 100) -> str:
    return f"Observation Audit\nTotal Entries: {len(entries)}\nLatest: {entries[-1].audit_id if entries else 'None'}"
