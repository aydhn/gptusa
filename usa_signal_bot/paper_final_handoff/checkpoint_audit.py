from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    PrePaperGovernanceCheckpoint,
    FinalHandoffAuditEntry,
    create_final_handoff_audit_id,
    _ts,
)
from usa_signal_bot.core.enums import FinalHandoffRiskFlag

from dataclasses import dataclass


@dataclass
class FinalHandoffAuditParams:
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    decision: Optional[str] = None
    evidence_refs: Optional[List[str]] = None
    risk_flags: Optional[List[FinalHandoffRiskFlag]] = None


def create_final_handoff_audit_entry(
    params: FinalHandoffAuditParams,
) -> FinalHandoffAuditEntry:
    return FinalHandoffAuditEntry(
        audit_id=create_final_handoff_audit_id(),
        created_at_utc=_ts(),
        entity_type=params.entity_type,
        entity_id=params.entity_id,
        action=params.action,
        decision=params.decision,
        rationale=params.rationale,
        evidence_refs=params.evidence_refs or [],
        risk_flags=params.risk_flags or [],
        warnings=[],
        errors=[],
    )


def audit_entry_from_handoff_review(
    handoff_review: FinalHandoffReview,
) -> FinalHandoffAuditEntry:
    return create_final_handoff_audit_entry(
        FinalHandoffAuditParams(
            entity_type="FinalHandoffReview",
            entity_id=handoff_review.handoff_review_id,
            action="Created",
            rationale=f"Decision: {handoff_review.decision.value}",
            decision=handoff_review.decision.value,
            evidence_refs=[e.evidence_ref_id for e in handoff_review.evidence_refs],
            risk_flags=handoff_review.safety_flags,
        )
    )


def audit_entry_from_archive_manifest(
    manifest: SealedReadinessArchiveManifest,
) -> FinalHandoffAuditEntry:
    return create_final_handoff_audit_entry(
        FinalHandoffAuditParams(
            entity_type="SealedReadinessArchiveManifest",
            entity_id=manifest.archive_id,
            action="Sealed",
            rationale=f"Status: {manifest.status.value}",
            decision=manifest.status.value,
            evidence_refs=manifest.artifact_refs,
            risk_flags=[],
        )
    )


def audit_entry_from_pre_paper_checkpoint(
    checkpoint: PrePaperGovernanceCheckpoint,
) -> FinalHandoffAuditEntry:
    return create_final_handoff_audit_entry(
        FinalHandoffAuditParams(
            entity_type="PrePaperGovernanceCheckpoint",
            entity_id=checkpoint.checkpoint_id,
            action="Evaluated",
            rationale=checkpoint.rationale,
            decision=checkpoint.decision.value,
            evidence_refs=[checkpoint.archive_id] if checkpoint.archive_id else [],
            risk_flags=checkpoint.safety_flags,
        )
    )


def append_final_handoff_audit_entry(
    entries: List[FinalHandoffAuditEntry], entry: FinalHandoffAuditEntry
) -> List[FinalHandoffAuditEntry]:
    return entries + [entry]


def final_handoff_audit_summary(
    entries: List[FinalHandoffAuditEntry],
) -> Dict[str, Any]:
    return {"count": len(entries)}


def final_handoff_audit_to_text(
    entries: List[FinalHandoffAuditEntry], limit: int = 100
) -> str:
    return f"Audit Trails: {len(entries)} entries."
