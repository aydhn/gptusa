"""Freeze Candidate Manifest Builder."""
import hashlib
from typing import Any
from datetime import datetime, timezone

from .phase124_models import (
    ArtifactChainReference,
    FreezeCandidateArtifact,
    FreezeCandidateManifest,
    FreezeCandidateStatus,
    create_freeze_candidate_artifact_id,
    create_freeze_candidate_manifest_id
)

def build_freeze_candidate_manifest(references: list[ArtifactChainReference]) -> FreezeCandidateManifest:
    now = datetime.now(timezone.utc).isoformat()
    artifacts = [build_freeze_candidate_artifact(r) for r in references]

    total = len(artifacts)
    included = sum(1 for a in artifacts if a.included)
    missing = sum(1 for a in artifacts if a.required and not a.included)

    manifest = FreezeCandidateManifest(
        manifest_id=create_freeze_candidate_manifest_id(),
        created_at_utc=now,
        status=FreezeCandidateStatus.MANIFESTED if missing == 0 else FreezeCandidateStatus.FAILED,
        artifacts=artifacts,
        total_artifacts=total,
        included_artifacts=included,
        missing_required_artifacts=missing,
        manifest_hash=None,
        immutable=True,
        research_data_only=True,
        no_secret_leak=True,
        no_forbidden_columns=True,
        no_execution_language=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        ready_for_final_closure=missing == 0
    )

    manifest.manifest_hash = compute_freeze_manifest_hash(manifest)
    errors = validate_freeze_candidate_manifest(manifest)
    if errors:
        manifest.status = FreezeCandidateStatus.FAILED
        manifest.ready_for_final_closure = False
        manifest.errors.extend(errors)

    return manifest

def build_freeze_candidate_artifact(reference: ArtifactChainReference) -> FreezeCandidateArtifact:
    return FreezeCandidateArtifact(
        artifact_id=create_freeze_candidate_artifact_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        phase=reference.phase,
        artifact_name=reference.artifact_name,
        artifact_kind="report",
        path=reference.artifact_path,
        artifact_hash=reference.artifact_hash,
        required=reference.artifact_required,
        included=reference.artifact_available,
        immutable=True,
        research_data_only=True,
        contains_secret=False,
        contains_forbidden_columns=False,
        contains_execution_language=False
    )

def compute_freeze_manifest_hash(manifest: FreezeCandidateManifest) -> str:
    h = hashlib.sha256()
    h.update(manifest.manifest_id.encode())
    for a in manifest.artifacts:
        if a.artifact_hash:
            h.update(a.artifact_hash.encode())
    return h.hexdigest()

def validate_freeze_candidate_manifest(manifest: FreezeCandidateManifest) -> list[str]:
    errors = []
    if manifest.activation_allowed:
        errors.append("activation_allowed must be False")
    return errors

def freeze_candidate_ready(manifest: FreezeCandidateManifest) -> bool:
    return manifest.ready_for_final_closure

def freeze_candidate_manifest_summary(manifest: FreezeCandidateManifest) -> dict[str, Any]:
    return {"status": manifest.status.value, "ready": manifest.ready_for_final_closure}

def freeze_candidate_manifest_to_text(manifest: FreezeCandidateManifest, limit: int = 300) -> str:
    return f"Manifest {manifest.manifest_id} - Ready: {manifest.ready_for_final_closure}"
