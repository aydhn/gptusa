from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    PrePaperGovernanceCheckpoint,
    FinalHandoffAuditEntry,
    create_final_handoff_audit_id,
    _ts
)
from usa_signal_bot.core.enums import FinalHandoffRiskFlag

def create_final_handoff_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, decision: Optional[str] = None, evidence_refs: Optional[List[str]] = None, risk_flags: Optional[List[FinalHandoffRiskFlag]] = None) -> FinalHandoffAuditEntry:
    return FinalHandoffAuditEntry(
        audit_id=create_final_handoff_audit_id(),
        created_at_utc=_ts(),
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

def audit_entry_from_handoff_review(handoff_review: FinalHandoffReview) -> FinalHandoffAuditEntry:
    return create_final_handoff_audit_entry(
        "FinalHandoffReview",
        handoff_review.handoff_review_id,
        "Created",
        f"Decision: {handoff_review.decision.value}",
        handoff_review.decision.value,
        [e.evidence_ref_id for e in handoff_review.evidence_refs],
        handoff_review.safety_flags
    )

def audit_entry_from_archive_manifest(manifest: SealedReadinessArchiveManifest) -> FinalHandoffAuditEntry:
    return create_final_handoff_audit_entry(
        "SealedReadinessArchiveManifest",
        manifest.archive_id,
        "Sealed",
        f"Status: {manifest.status.value}",
        manifest.status.value,
        manifest.artifact_refs,
        []
    )

def audit_entry_from_pre_paper_checkpoint(checkpoint: PrePaperGovernanceCheckpoint) -> FinalHandoffAuditEntry:
    return create_final_handoff_audit_entry(
        "PrePaperGovernanceCheckpoint",
        checkpoint.checkpoint_id,
        "Evaluated",
        checkpoint.rationale,
        checkpoint.decision.value,
        [checkpoint.archive_id] if checkpoint.archive_id else [],
        checkpoint.safety_flags
    )

def append_final_handoff_audit_entry(entries: List[FinalHandoffAuditEntry], entry: FinalHandoffAuditEntry) -> List[FinalHandoffAuditEntry]:
    return entries + [entry]

def final_handoff_audit_summary(entries: List[FinalHandoffAuditEntry]) -> Dict[str, Any]:
    return {"count": len(entries)}

def final_handoff_audit_to_text(entries: List[FinalHandoffAuditEntry], limit: int = 100) -> str:
    return f"Audit Trails: {len(entries)} entries."
