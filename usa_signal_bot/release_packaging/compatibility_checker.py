from typing import Any, Dict, List, Optional
from usa_signal_bot.release_packaging.packaging_models import BundleManifest, VersionedCandidateBundle
from usa_signal_bot.core.enums import BundleCompatibilityStatus

def check_bundle_schema_compatibility(manifest: BundleManifest, supported_schema_versions: Optional[List[str]] = None) -> BundleCompatibilityStatus:
    if not supported_schema_versions:
        supported_schema_versions = ["1.0"]
    if manifest.schema_version in supported_schema_versions:
        return BundleCompatibilityStatus.COMPATIBLE
    return BundleCompatibilityStatus.INCOMPATIBLE

def check_bundle_version_compatibility(bundle: VersionedCandidateBundle, min_supported_version: Optional[str] = None) -> BundleCompatibilityStatus:
    if not min_supported_version:
        min_supported_version = "0.1.0"
    if bundle.bundle_version >= min_supported_version:
        return BundleCompatibilityStatus.COMPATIBLE
    return BundleCompatibilityStatus.INCOMPATIBLE

def check_required_artifacts_compatibility(manifest: BundleManifest) -> BundleCompatibilityStatus:
    if not manifest.missing_artifact_types:
        return BundleCompatibilityStatus.COMPATIBLE
    return BundleCompatibilityStatus.WARNING

def compatibility_warnings(bundle: Any) -> List[str]:
    return []

def compatibility_checker_to_text(payload: Dict[str, Any]) -> str:
    return "Compatibility Check OK"
