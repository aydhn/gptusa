from typing import Any, Dict, List
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    FinalHandoffEvidenceRef,
    create_sealed_archive_id,
    _ts
)
from usa_signal_bot.core.enums import SealedArchiveStatus

def required_archive_artifact_types() -> List[str]:
    return [
        "promotion_dossier_review",
        "final_safety_board_review",
        "staged_readiness_package",
        "readiness_rehearsal_review",
        "readiness_rehearsal_run",
        "final_review_lock",
        "guarded_handoff_registry_entry",
        "observer_governance_review",
        "paper_observer_review",
        "validation_reports",
        "audit_trails"
    ]

def build_final_handoff_evidence_refs(readiness_payload: Dict[str, Any]) -> List[FinalHandoffEvidenceRef]:
    refs = []
    # Mocking extraction for now based on typical payload structure
    for typ in required_archive_artifact_types():
        refs.append(FinalHandoffEvidenceRef(
            evidence_ref_id=f"ev_{typ}",
            created_at_utc=_ts(),
            source_type=typ,
            source_id=readiness_payload.get(f"{typ}_id"),
            source_path=None,
            required=True,
            available=True,
            stale=False,
            summary={"info": "Mocked evidence extraction"},
            warnings=[],
            errors=[]
        ))
    return refs

def build_sealed_readiness_archive_manifest(handoff_review: FinalHandoffReview) -> SealedReadinessArchiveManifest:
    artifact_refs = collect_archive_artifact_refs(handoff_review)
    evidence_ref_ids = [e.evidence_ref_id for e in handoff_review.evidence_refs]
    return SealedReadinessArchiveManifest(
        archive_id=create_sealed_archive_id(),
        created_at_utc=_ts(),
        status=SealedArchiveStatus.CREATED,
        candidate_id=handoff_review.candidate_id,
        handoff_review_id=handoff_review.handoff_review_id,
        artifact_refs=artifact_refs,
        evidence_refs=evidence_ref_ids,
        archive_hash=None,
        sealed=False,
        immutable=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )

def collect_archive_artifact_refs(handoff_review: FinalHandoffReview) -> List[str]:
    # In real implementation this would collect paths or URIs
    return [e.source_id for e in handoff_review.evidence_refs if e.source_id]

def validate_archive_manifest_safety(manifest: SealedReadinessArchiveManifest) -> List[str]:
    errors = []
    if manifest.allows_active_paper: errors.append("Archive allows_active_paper")
    if manifest.allows_broker_execution: errors.append("Archive allows_broker_execution")
    if manifest.allows_paper_state_mutation: errors.append("Archive allows_paper_state_mutation")
    if manifest.allows_config_patch: errors.append("Archive allows_config_patch")
    return errors

def archive_manifest_summary(manifest: SealedReadinessArchiveManifest) -> Dict[str, Any]:
    return {"id": manifest.archive_id, "status": manifest.status.value, "sealed": manifest.sealed}

def archive_manifest_to_text(manifest: SealedReadinessArchiveManifest) -> str:
    return f"ArchiveManifest: {manifest.archive_id} [{manifest.status.value}] sealed={manifest.sealed}"
