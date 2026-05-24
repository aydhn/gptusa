from typing import Any
import datetime
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionDossierAuditEntry,
    DryAdmissionGateDossier,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerEvent,
    create_dry_admission_dossier_audit_id
)

def create_dry_admission_dossier_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: list[str] | None = None,
    risk_flags: list[DryAdmissionDossierRiskFlag] | None = None
) -> DryAdmissionDossierAuditEntry:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return DryAdmissionDossierAuditEntry(
        audit_id=create_dry_admission_dossier_audit_id(),
        created_at_utc=now,
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

def audit_entry_from_dry_admission_dossier(dossier: DryAdmissionGateDossier) -> DryAdmissionDossierAuditEntry:
    return create_dry_admission_dossier_audit_entry(
        entity_type="DryAdmissionGateDossier",
        entity_id=dossier.dossier_id,
        action="CREATE_DOSSIER",
        rationale=f"Dossier status: {dossier.status.value}",
        decision=dossier.decision.value,
        evidence_refs=dossier.evidence_refs,
        risk_flags=dossier.safety_flags
    )

def audit_entry_from_dry_admission_acceptance_seal(seal: DryAdmissionAcceptanceSeal) -> DryAdmissionDossierAuditEntry:
    return create_dry_admission_dossier_audit_entry(
        entity_type="DryAdmissionAcceptanceSeal",
        entity_id=seal.seal_id,
        action="CREATE_SEAL",
        rationale=f"Seal status: {seal.status.value}",
        decision=seal.decision.value,
        evidence_refs=[],
        risk_flags=seal.risk_flags
    )

def audit_entry_from_rehearsal_blocker_events(events: list[PaperModeRehearsalBlockerEvent]) -> DryAdmissionDossierAuditEntry:
    return create_dry_admission_dossier_audit_entry(
        entity_type="RehearsalBlockerEventBatch",
        entity_id="batch",
        action="EVALUATE_EVENTS",
        rationale=f"Evaluated {len(events)} events",
        decision="BLOCK" if all(e.blocked for e in events) else "FAIL",
        evidence_refs=[e.event_id for e in events],
        risk_flags=[]
    )

def append_dry_admission_dossier_audit_entry(entries: list[DryAdmissionDossierAuditEntry], entry: DryAdmissionDossierAuditEntry) -> list[DryAdmissionDossierAuditEntry]:
    entries.append(entry)
    return entries

def dry_admission_dossier_audit_summary(entries: list[DryAdmissionDossierAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "actions": [e.action for e in entries]
    }

def dry_admission_dossier_audit_to_text(entries: list[DryAdmissionDossierAuditEntry], limit: int = 100) -> str:
    summary = dry_admission_dossier_audit_summary(entries)
    return f"Audit Trails: {summary['total_entries']} entries"
