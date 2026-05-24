from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.core.enums import SimulatorDossierRiskFlag
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    SimulatorDossierAuditEntry,
    create_simulator_dossier_audit_id,
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerEvent
)

def create_simulator_dossier_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: list[str] | None = None,
    risk_flags: list[SimulatorDossierRiskFlag] | None = None
) -> SimulatorDossierAuditEntry:
    return SimulatorDossierAuditEntry(
        audit_id=create_simulator_dossier_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[],
        metadata={"local_audit_only": True, "no_external_telemetry": True}
    )

def audit_entry_from_simulator_dossier(dossier: LocalPaperAdmissionSimulatorGateDossier) -> SimulatorDossierAuditEntry:
    return create_simulator_dossier_audit_entry(
        entity_type="LocalPaperAdmissionSimulatorGateDossier",
        entity_id=dossier.dossier_id,
        action="BUILD_DOSSIER",
        rationale="Built simulator dossier",
        decision=dossier.decision.value,
        evidence_refs=dossier.evidence_refs,
        risk_flags=dossier.safety_flags
    )

def audit_entry_from_simulator_acceptance_seal(seal: SimulatorAcceptanceSeal) -> SimulatorDossierAuditEntry:
    return create_simulator_dossier_audit_entry(
        entity_type="SimulatorAcceptanceSeal",
        entity_id=seal.seal_id,
        action="BUILD_SEAL",
        rationale="Built simulator acceptance seal",
        decision=seal.decision.value,
        evidence_refs=[],
        risk_flags=seal.risk_flags
    )

def audit_entry_from_sandbox_runtime_admission_blocker_events(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> SimulatorDossierAuditEntry:
    event_ids = [e.event_id for e in events]
    return create_simulator_dossier_audit_entry(
        entity_type="PaperSandboxRuntimeAdmissionBlockerEventList",
        entity_id=event_ids[0] if event_ids else "unknown",
        action="EVALUATE_ATTEMPTS",
        rationale=f"Evaluated {len(events)} admission attempts",
        decision="BLOCK_SANDBOX_RUNTIME_ADMISSION",
        evidence_refs=event_ids,
        risk_flags=[]
    )

def append_simulator_dossier_audit_entry(entries: list[SimulatorDossierAuditEntry], entry: SimulatorDossierAuditEntry) -> list[SimulatorDossierAuditEntry]:
    return entries + [entry]

def simulator_dossier_audit_summary(entries: list[SimulatorDossierAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "actions": list(set(e.action for e in entries))
    }

def simulator_dossier_audit_to_text(entries: list[SimulatorDossierAuditEntry], limit: int = 100) -> str:
    summary = simulator_dossier_audit_summary(entries)
    lines = [
        "--- Simulator Dossier Audit Trail ---",
        f"Total Entries: {summary['total_entries']}"
    ]
    for e in entries[:limit]:
        lines.append(f"  - {e.created_at_utc} [{e.action}] {e.entity_type} {e.entity_id}: {e.decision} ({e.rationale})")
    return "\n".join(lines)
