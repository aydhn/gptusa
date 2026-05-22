from typing import Any, Dict
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffEvidenceRef,
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    ArchiveIntegrityReport,
    PrePaperCheckpointGate,
    PrePaperGovernanceCheckpoint,
    FinalHandoffAuditEntry,
    FinalHandoffFullReview
)
from usa_signal_bot.paper_final_handoff.final_handoff_report import final_handoff_limitations_text

def final_handoff_evidence_ref_to_text(item: FinalHandoffEvidenceRef) -> str: return f"EvidenceRef: {item.evidence_ref_id}"
def final_handoff_review_to_text(item: FinalHandoffReview) -> str: return f"Review: {item.handoff_review_id} [{item.status.value}]"
def sealed_archive_manifest_to_text(item: SealedReadinessArchiveManifest) -> str: return f"Manifest: {item.archive_id} [{item.status.value}]"
def archive_integrity_report_to_text(item: ArchiveIntegrityReport) -> str: return f"Integrity: {item.status.value}"
def pre_paper_checkpoint_gate_to_text(item: PrePaperCheckpointGate) -> str: return f"Gate: {item.gate_name} [{item.status.value}]"
def pre_paper_governance_checkpoint_to_text(item: PrePaperGovernanceCheckpoint, limit: int = 100) -> str: return f"Checkpoint: {item.checkpoint_id} [{item.status.value}]"
def final_handoff_audit_entry_to_text(item: FinalHandoffAuditEntry) -> str: return f"Audit: {item.audit_id} [{item.action}]"

def final_handoff_full_review_to_text(item: FinalHandoffFullReview, limit: int = 100) -> str:
    return (
        f"FinalHandoffFullReview: {item.review_id}\n"
        f"Reviews: {len(item.handoff_reviews)}\n"
        f"Manifests: {len(item.archive_manifests)}\n"
        f"{final_handoff_limitations_text()}"
    )

def final_handoff_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
