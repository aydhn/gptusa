from typing import Any, Dict, List
from usa_signal_bot.release_packaging.packaging_models import BundleManifest, VersionedCandidateBundle, FrozenArtifact

def diff_bundle_manifests(a: BundleManifest, b: BundleManifest) -> Dict[str, Any]:
    a_types = {art.artifact_type for art in a.artifacts}
    b_types = {art.artifact_type for art in b.artifacts}

    return {
        "added_types": list(b_types - a_types),
        "removed_types": list(a_types - b_types),
        "hash_changed": a.manifest_hash != b.manifest_hash
    }

def diff_versioned_bundles(a: VersionedCandidateBundle, b: VersionedCandidateBundle) -> Dict[str, Any]:
    return {
        "version_change": f"{a.bundle_version} -> {b.bundle_version}",
        "status_change": f"{a.status.value} -> {b.status.value}"
    }

def diff_artifact_sets(a: List[FrozenArtifact], b: List[FrozenArtifact]) -> Dict[str, Any]:
    a_ids = {art.artifact_id for art in a}
    b_ids = {art.artifact_id for art in b}
    return {
        "added": len(b_ids - a_ids),
        "removed": len(a_ids - b_ids)
    }

def bundle_diff_summary(diff: Dict[str, Any]) -> Dict[str, Any]:
    return diff

def bundle_diff_to_text(diff: Dict[str, Any]) -> str:
    return f"Diff: {diff}"
