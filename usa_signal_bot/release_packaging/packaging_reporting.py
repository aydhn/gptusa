from typing import Any, Dict
from usa_signal_bot.release_packaging.packaging_models import (
    FrozenArtifact, BundleManifest, BundleValidationResult,
    VersionedCandidateBundle, ReleasePackagingReview
)

def frozen_artifact_to_text(item: FrozenArtifact) -> str:
    return f"Artifact {item.artifact_id} ({item.artifact_type}): {item.status.value}"

def bundle_manifest_to_text(item: BundleManifest) -> str:
    return f"Manifest {item.manifest_id} (Bundle: {item.bundle_id}): {len(item.artifacts)} artifacts"

def bundle_validation_result_to_text(item: BundleValidationResult) -> str:
    return f"Validation {item.validation_id}: {item.status.value}"

def versioned_candidate_bundle_to_text(item: VersionedCandidateBundle) -> str:
    return f"Bundle {item.bundle_id} (v{item.bundle_version}): {item.status.value}"

def release_packaging_review_to_text(item: ReleasePackagingReview, limit: int = 100) -> str:
    return f"Review {item.review_id}: {len(item.bundles)} bundles"

def packaging_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"

def release_packaging_limitations_text() -> str:
    return "NOTE: This bundle is a local research package only. No live trading, broker routing, or auto-apply to production is performed."
