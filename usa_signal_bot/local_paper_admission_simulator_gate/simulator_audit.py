from typing import Any
from .simulator_gate_models import SimulatorGateAuditEntry, FinalLocalPaperAdmissionSimulatorGate, RehearsalReplayResult, DryAdmissionEvidenceFreezeBundle, create_simulator_audit_id
from usa_signal_bot.core.enums import SimulatorGateRiskFlag
from datetime import datetime, timezone

def create_simulator_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, decision: str | None = None, evidence_refs: list[str] | None = None, risk_flags: list[SimulatorGateRiskFlag] | None = None) -> SimulatorGateAuditEntry:
    return SimulatorGateAuditEntry(
        audit_id=create_simulator_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or []
    )

def audit_entry_from_final_simulator_gate(gate: FinalLocalPaperAdmissionSimulatorGate) -> SimulatorGateAuditEntry:
    return create_simulator_audit_entry("FinalSimulatorGate", gate.gate_id, "EVALUATE", "Simulator gate evaluated")

def audit_entry_from_rehearsal_replay_result(result: RehearsalReplayResult) -> SimulatorGateAuditEntry:
    return create_simulator_audit_entry("RehearsalReplayResult", result.replay_result_id, "REPLAY", "Rehearsal replayed")

def audit_entry_from_dry_admission_evidence_freeze(bundle: DryAdmissionEvidenceFreezeBundle) -> SimulatorGateAuditEntry:
    return create_simulator_audit_entry("EvidenceFreezeBundle", bundle.freeze_id, "FREEZE", "Evidence frozen")

def append_simulator_audit_entry(entries: list[SimulatorGateAuditEntry], entry: SimulatorGateAuditEntry) -> list[SimulatorGateAuditEntry]:
    entries.append(entry)
    return entries

def simulator_audit_summary(entries: list[SimulatorGateAuditEntry]) -> dict[str, Any]:
    return {}

def simulator_audit_to_text(entries: list[SimulatorGateAuditEntry], limit: int = 100) -> str:
    return ""
