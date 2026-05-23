from typing import Any, Optional
import datetime
from usa_signal_bot.core.enums import NoWriteTransitionRiskFlag
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionAuditEntry,
    NoWriteTransitionDossier,
    AdmissionEvidenceSealValidation,
    PaperSandboxBridgeEnvelope,
    create_transition_audit_id
)

def create_no_write_transition_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[list[str]] = None,
    risk_flags: Optional[list[NoWriteTransitionRiskFlag]] = None
) -> NoWriteTransitionAuditEntry:
    return NoWriteTransitionAuditEntry(
        audit_id=create_transition_audit_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[]
    )

def audit_entry_from_transition_dossier(dossier: NoWriteTransitionDossier) -> NoWriteTransitionAuditEntry:
    return create_no_write_transition_audit_entry(
        entity_type="NoWriteTransitionDossier",
        entity_id=dossier.dossier_id,
        action="CREATE_DOSSIER",
        rationale=f"Dossier created with status {dossier.status.value}",
        decision=dossier.decision.value,
        evidence_refs=dossier.evidence_refs,
        risk_flags=dossier.safety_flags
    )

def audit_entry_from_seal_validation(validation: AdmissionEvidenceSealValidation) -> NoWriteTransitionAuditEntry:
    return create_no_write_transition_audit_entry(
        entity_type="AdmissionEvidenceSealValidation",
        entity_id=validation.validation_id,
        action="VALIDATE_SEAL",
        rationale=f"Seal validated with status {validation.status.value}",
        decision=validation.decision.value,
        risk_flags=validation.risk_flags
    )

def audit_entry_from_bridge_envelope(envelope: PaperSandboxBridgeEnvelope) -> NoWriteTransitionAuditEntry:
    return create_no_write_transition_audit_entry(
        entity_type="PaperSandboxBridgeEnvelope",
        entity_id=envelope.bridge_id,
        action="CREATE_BRIDGE",
        rationale=f"Bridge created with status {envelope.status.value}",
        decision=envelope.decision.value,
        risk_flags=envelope.risk_flags
    )

def append_no_write_transition_audit_entry(entries: list[NoWriteTransitionAuditEntry], entry: NoWriteTransitionAuditEntry) -> list[NoWriteTransitionAuditEntry]:
    return entries + [entry]

def no_write_transition_audit_summary(entries: list[NoWriteTransitionAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "actions": [e.action for e in entries]
    }

def no_write_transition_audit_to_text(entries: list[NoWriteTransitionAuditEntry], limit: int = 100) -> str:
    lines = ["Audit Trails:"]
    for e in entries[:limit]:
        lines.append(f"  - [{e.created_at_utc}] {e.action} on {e.entity_type} ({e.entity_id}): {e.decision}")
    return "\n".join(lines)
