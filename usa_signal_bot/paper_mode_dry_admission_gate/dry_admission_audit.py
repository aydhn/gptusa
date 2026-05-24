from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.core.enums import DryAdmissionGateRiskFlag
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    DryAdmissionGateAuditEntry,
    FinalPaperModeDryAdmissionGate,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle,
    create_dry_admission_audit_id
)

def create_dry_admission_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: List[str] | None = None,
    risk_flags: List[DryAdmissionGateRiskFlag] | None = None
) -> DryAdmissionGateAuditEntry:
    return DryAdmissionGateAuditEntry(
        audit_id=create_dry_admission_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        rationale=rationale,
        decision=decision,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[]
    )

def audit_entry_from_final_dry_admission_gate(gate: FinalPaperModeDryAdmissionGate) -> DryAdmissionGateAuditEntry:
    return create_dry_admission_audit_entry(
        entity_type="FinalPaperModeDryAdmissionGate",
        entity_id=gate.gate_id,
        action="Created",
        rationale="Final Gate Evaluated",
        decision=gate.decision.value,
        risk_flags=gate.safety_flags
    )

def audit_entry_from_shadow_replay_result(result: ShadowLaunchReplayResult) -> DryAdmissionGateAuditEntry:
    return create_dry_admission_audit_entry(
        entity_type="ShadowLaunchReplayResult",
        entity_id=result.replay_result_id,
        action="Created",
        rationale="Shadow Replay Executed",
        decision=result.outcome.value,
        risk_flags=result.risk_flags
    )

def audit_entry_from_board_evidence_freeze(bundle: BoardEvidenceFreezeBundle) -> DryAdmissionGateAuditEntry:
    return create_dry_admission_audit_entry(
        entity_type="BoardEvidenceFreezeBundle",
        entity_id=bundle.freeze_id,
        action="Created",
        rationale="Evidence Freeze Evaluated",
        decision=bundle.decision.value,
        risk_flags=bundle.risk_flags
    )

def append_dry_admission_audit_entry(entries: List[DryAdmissionGateAuditEntry], entry: DryAdmissionGateAuditEntry) -> List[DryAdmissionGateAuditEntry]:
    # Local only, no external
    return entries + [entry]

def dry_admission_audit_summary(entries: List[DryAdmissionGateAuditEntry]) -> dict[str, Any]:
    return {
        "count": len(entries)
    }

def dry_admission_audit_to_text(entries: List[DryAdmissionGateAuditEntry], limit: int = 100) -> str:
    return f"Dry Admission Audit - Total entries: {len(entries)}"
