from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from usa_signal_bot.release_packaging.packaging_models import BundleManifest, FrozenArtifact, create_bundle_manifest_id
from usa_signal_bot.release_packaging.checksum import text_sha256
from usa_signal_bot.core.enums import ReleaseBundleType, ReleaseBundleStatus

def build_bundle_manifest(bundle_id: str, bundle_version: str, bundle_type: ReleaseBundleType, artifacts: List[FrozenArtifact], source_candidate_id: Optional[str] = None, source_experiment_id: Optional[str] = None, source_governance_review_id: Optional[str] = None) -> BundleManifest:
    required_types = ["release_candidate", "governance_review", "evidence_pack", "comparison_report", "acceptance_gate_evaluation", "config_snapshot", "validation_report", "safety_report"]
    missing_types = determine_missing_artifact_types(artifacts, required_types)

    manifest = BundleManifest(
        manifest_id=create_bundle_manifest_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        bundle_id=bundle_id,
        bundle_version=bundle_version,
        bundle_type=bundle_type,
        bundle_status=ReleaseBundleStatus.FROZEN,
        source_candidate_id=source_candidate_id,
        source_experiment_id=source_experiment_id,
        source_governance_review_id=source_governance_review_id,
        artifacts=artifacts,
        required_artifact_types=required_types,
        missing_artifact_types=missing_types,
        manifest_hash=None,
        schema_version="1.0",
        warnings=[],
        errors=[]
    )
    manifest.manifest_hash = calculate_manifest_hash(manifest)
    if missing_types:
        manifest.warnings.append(f"Missing required artifact types: {missing_types}")
    return manifest

def calculate_manifest_hash(manifest: BundleManifest) -> str:
    hashes = sorted([a.payload_hash for a in manifest.artifacts if a.payload_hash])
    return text_sha256("".join(hashes))

def determine_missing_artifact_types(artifacts: List[FrozenArtifact], required_types: List[str]) -> List[str]:
    present = {a.artifact_type for a in artifacts}
    return [rt for rt in required_types if rt not in present]

def manifest_is_complete(manifest: BundleManifest) -> bool:
    return len(manifest.missing_artifact_types) == 0

def manifest_summary(manifest: BundleManifest) -> Dict[str, Any]:
    return {"artifacts": len(manifest.artifacts), "complete": manifest_is_complete(manifest)}

def manifest_to_text(manifest: BundleManifest) -> str:
    return f"Manifest {manifest.manifest_id}: {len(manifest.artifacts)} artifacts."
