from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import BoundaryAuditEntry, PaperSandboxBoundaryCertificate, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeBundle, create_boundary_audit_id
from usa_signal_bot.core.enums import PaperSandboxBoundaryRiskFlag

def create_boundary_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, decision: str | None = None, evidence_refs: list[str] | None = None, risk_flags: list[PaperSandboxBoundaryRiskFlag] | None = None) -> BoundaryAuditEntry:
    return BoundaryAuditEntry(
        audit_id=create_boundary_audit_id(),
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

def audit_entry_from_boundary_certificate(certificate: PaperSandboxBoundaryCertificate) -> BoundaryAuditEntry:
    return create_boundary_audit_entry("certificate", certificate.certificate_id, "build", "Boundary certificate created")

def audit_entry_from_blocker_replay_result(result: AdmissionBlockerReplayResult) -> BoundaryAuditEntry:
    return create_boundary_audit_entry("replay_result", result.replay_result_id, "replay", "Blocker replay executed")

def audit_entry_from_evidence_freeze(bundle: NoOrderEvidenceFreezeBundle) -> BoundaryAuditEntry:
    return create_boundary_audit_entry("evidence_freeze", bundle.freeze_id, "freeze", "Evidence frozen")

def append_boundary_audit_entry(entries: list[BoundaryAuditEntry], entry: BoundaryAuditEntry) -> list[BoundaryAuditEntry]:
    res = list(entries)
    res.append(entry)
    return res

def boundary_audit_summary(entries: list[BoundaryAuditEntry]) -> dict[str, Any]:
    return {"count": len(entries)}

def boundary_audit_to_text(entries: list[BoundaryAuditEntry], limit: int = 100) -> str:
    return str(boundary_audit_summary(entries))
