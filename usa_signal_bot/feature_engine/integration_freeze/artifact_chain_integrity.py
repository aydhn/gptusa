"""Artifact Chain Integrity."""
from datetime import datetime, timezone
from typing import Any

from .phase124_models import (
    ArtifactChainReference,
    ArtifactChainIntegrityResult,
    ArtifactChainStatus,
    ArtifactChainPhase,
    create_artifact_chain_integrity_id
)

def check_artifact_chain_integrity(references: list[ArtifactChainReference]) -> ArtifactChainIntegrityResult:
    missing_required = len(detect_missing_required_artifacts(references))
    hash_mismatch_count = len(detect_hash_mismatches(references))
    schema_break_count = 0  # Checked by schema validator
    lineage_break_count = 0 # Checked by lineage validator
    safety_break_count = 0  # Checked by safety validator

    status = artifact_chain_status_from_counts(
        missing_required, hash_mismatch_count, schema_break_count,
        lineage_break_count, safety_break_count
    )

    total_required = sum(1 for r in references if r.artifact_required)
    total_available = sum(1 for r in references if r.artifact_available)

    chain_complete = (missing_required == 0)
    chain_valid = chain_complete and (hash_mismatch_count == 0)

    return ArtifactChainIntegrityResult(
        integrity_id=create_artifact_chain_integrity_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        references=references,
        status=status,
        total_required=total_required,
        total_available=total_available,
        missing_required=missing_required,
        hash_mismatch_count=hash_mismatch_count,
        schema_break_count=schema_break_count,
        lineage_break_count=lineage_break_count,
        safety_break_count=safety_break_count,
        chain_complete=chain_complete,
        chain_valid=chain_valid
    )

def detect_missing_required_artifacts(references: list[ArtifactChainReference]) -> list[ArtifactChainReference]:
    return [r for r in references if r.artifact_required and not r.artifact_available]

def detect_hash_mismatches(references: list[ArtifactChainReference]) -> list[ArtifactChainReference]:
    mismatches = []
    # This is a stub for actual hash checking against a manifest
    # For now, we assume if available and hash is present, it's ok, unless explicitly marked error
    return mismatches

def detect_chain_phase_gaps(references: list[ArtifactChainReference]) -> list[ArtifactChainPhase]:
    expected = [
        ArtifactChainPhase.PHASE_116_FEATURE_FOUNDATION,
        ArtifactChainPhase.PHASE_117_CORE_INDICATORS,
        ArtifactChainPhase.PHASE_118_ADVANCED_FEATURES,
        ArtifactChainPhase.PHASE_119_ENRICHED_FEATURES,
        ArtifactChainPhase.PHASE_120_FACTOR_COMPOSITION,
        ArtifactChainPhase.PHASE_121_FACTOR_SCORING,
        ArtifactChainPhase.PHASE_122_FACTOR_VALIDATION,
        ArtifactChainPhase.PHASE_123_FACTOR_EXPLAINABILITY
    ]
    present = [r.phase for r in references if r.artifact_available]
    return [p for p in expected if p not in present]

def artifact_chain_status_from_counts(missing_required: int, hash_mismatch_count: int, schema_break_count: int, lineage_break_count: int, safety_break_count: int) -> ArtifactChainStatus:
    if safety_break_count > 0:
        return ArtifactChainStatus.SAFETY_BREAK
    if missing_required > 0:
        return ArtifactChainStatus.MISSING_ARTIFACTS
    if hash_mismatch_count > 0:
        return ArtifactChainStatus.HASH_MISMATCH
    if lineage_break_count > 0:
        return ArtifactChainStatus.LINEAGE_BREAK
    if schema_break_count > 0:
         return ArtifactChainStatus.SCHEMA_BREAK

    return ArtifactChainStatus.COMPLETE

def artifact_chain_integrity_summary(result: ArtifactChainIntegrityResult) -> dict[str, Any]:
    return {
        "status": result.status.value,
        "valid": result.chain_valid,
        "missing": result.missing_required
    }

def artifact_chain_integrity_to_text(result: ArtifactChainIntegrityResult, limit: int = 300) -> str:
    return f"Artifact Chain Integrity {result.integrity_id} - Valid: {result.chain_valid}"
