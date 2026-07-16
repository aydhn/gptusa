
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    PaperSafeGateAuditEntry, PaperSafeGateRiskFlag, FinalPaperSafeGate,
    BoundaryCertificateReplayResult, FrozenEvidenceIntegrityAudit,
    create_paper_safe_audit_id, utcnow_iso
)

@dataclass
class CreatePaperSafeAuditEntryParams:
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    decision: Optional[str] = None
    evidence_refs: Optional[List[str]] = None
    risk_flags: Optional[List[PaperSafeGateRiskFlag]] = None

def create_paper_safe_audit_entry(params: CreatePaperSafeAuditEntryParams) -> PaperSafeGateAuditEntry:
    return PaperSafeGateAuditEntry(
        audit_id=create_paper_safe_audit_id(),
        created_at_utc=utcnow_iso(),
        entity_type=params.entity_type,
        entity_id=params.entity_id,
        action=params.action,
        decision=params.decision,
        rationale=params.rationale,
        evidence_refs=params.evidence_refs or [],
        risk_flags=params.risk_flags or [],
        warnings=[],
        errors=[]
    )

def audit_entry_from_final_paper_safe_gate(gate: FinalPaperSafeGate) -> PaperSafeGateAuditEntry:
    return create_paper_safe_audit_entry(CreatePaperSafeAuditEntryParams("FinalPaperSafeGate", gate.gate_id, "VALIDATE", "Paper safe validation"))

def audit_entry_from_boundary_replay_result(result: BoundaryCertificateReplayResult) -> PaperSafeGateAuditEntry:
    return create_paper_safe_audit_entry(CreatePaperSafeAuditEntryParams("BoundaryCertificateReplayResult", result.replay_result_id, "REPLAY", "Boundary replay"))

def audit_entry_from_integrity_audit(audit: FrozenEvidenceIntegrityAudit) -> PaperSafeGateAuditEntry:
    return create_paper_safe_audit_entry(CreatePaperSafeAuditEntryParams("FrozenEvidenceIntegrityAudit", audit.audit_id, "AUDIT", "Integrity check"))

def append_paper_safe_audit_entry(entries: List[PaperSafeGateAuditEntry], entry: PaperSafeGateAuditEntry) -> List[PaperSafeGateAuditEntry]:
    entries.append(entry)
    return entries

def paper_safe_audit_summary(entries: List[PaperSafeGateAuditEntry]) -> Dict[str, Any]:
    return {"total": len(entries)}

def paper_safe_audit_to_text(entries: List[PaperSafeGateAuditEntry], limit: int = 100) -> str:
    return f"Audit Entries: {len(entries)}"
