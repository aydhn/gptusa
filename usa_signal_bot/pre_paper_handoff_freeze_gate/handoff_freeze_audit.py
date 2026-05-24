from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PrePaperHandoffFreezeRiskFlag
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    PrePaperHandoffFreezeAuditEntry,
    FinalPrePaperHandoffFreezeGate,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle,
    create_handoff_freeze_audit_id
)

def create_handoff_freeze_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[PrePaperHandoffFreezeRiskFlag]] = None
) -> PrePaperHandoffFreezeAuditEntry:
    return PrePaperHandoffFreezeAuditEntry(
        audit_id=create_handoff_freeze_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
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

def audit_entry_from_final_handoff_freeze_gate(gate: FinalPrePaperHandoffFreezeGate) -> PrePaperHandoffFreezeAuditEntry:
    return create_handoff_freeze_audit_entry(
        entity_type="FinalPrePaperHandoffFreezeGate",
        entity_id=gate.gate_id,
        action="EVALUATE_GATE",
        rationale=f"Evaluated gate status {gate.status.value}",
        decision=gate.decision.value,
        evidence_refs=[gate.source_simulator_dossier_id] if gate.source_simulator_dossier_id else [],
        risk_flags=gate.safety_flags
    )

def audit_entry_from_sandbox_runtime_admission_replay_result(result: SandboxRuntimeAdmissionReplayResult) -> PrePaperHandoffFreezeAuditEntry:
    return create_handoff_freeze_audit_entry(
        entity_type="SandboxRuntimeAdmissionReplayResult",
        entity_id=result.replay_result_id,
        action="REPLAY_EVALUATION",
        rationale=f"Replay evaluated {result.replayed_attempt_count} attempts",
        decision=result.outcome.value,
        risk_flags=result.risk_flags
    )

def audit_entry_from_simulator_evidence_freeze(bundle: SimulatorEvidenceFreezeBundle) -> PrePaperHandoffFreezeAuditEntry:
    return create_handoff_freeze_audit_entry(
        entity_type="SimulatorEvidenceFreezeBundle",
        entity_id=bundle.freeze_id,
        action="EVIDENCE_FREEZE",
        rationale=f"Frozen with {bundle.missing_evidence_count} missing evidence",
        decision=bundle.decision.value,
        evidence_refs=bundle.evidence_refs,
        risk_flags=bundle.risk_flags
    )

def append_handoff_freeze_audit_entry(entries: List[PrePaperHandoffFreezeAuditEntry], entry: PrePaperHandoffFreezeAuditEntry) -> List[PrePaperHandoffFreezeAuditEntry]:
    return entries + [entry]

def handoff_freeze_audit_summary(entries: List[PrePaperHandoffFreezeAuditEntry]) -> dict[str, Any]:
    return {"total_entries": len(entries)}

def handoff_freeze_audit_to_text(entries: List[PrePaperHandoffFreezeAuditEntry], limit: int = 100) -> str:
    res = "Handoff Freeze Audit Trail:\n"
    for e in entries[:limit]:
        res += f"- {e.created_at_utc}: {e.action} on {e.entity_type} ({e.decision})\n"
    return res
