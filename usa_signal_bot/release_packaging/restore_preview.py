from typing import Any, Dict, List
from usa_signal_bot.release_packaging.packaging_models import VersionedCandidateBundle

def build_restore_preview(bundle: VersionedCandidateBundle) -> Dict[str, Any]:
    return {
        "bundle_id": bundle.bundle_id,
        "bundle_version": bundle.bundle_version,
        "restore_allowed": restore_preview_allowed(bundle),
        "artifacts_to_restore": restore_preview_artifact_list(bundle),
        "warnings": restore_preview_safety_warnings(bundle)
    }

def restore_preview_artifact_list(bundle: VersionedCandidateBundle) -> List[Dict[str, Any]]:
    if not bundle.manifest:
        return []
    return [{"type": a.artifact_type, "id": a.artifact_id} for a in bundle.manifest.artifacts]

def restore_preview_safety_warnings(bundle: VersionedCandidateBundle) -> List[str]:
    warns = ["This is a local preview. No real restore will be performed.", "No production config will be patched."]
    if bundle.manifest and bundle.manifest.missing_artifact_types:
        warns.append("Manifest is missing some required artifacts.")
    return warns

def restore_preview_allowed(bundle: VersionedCandidateBundle) -> bool:
    if bundle.allowed_for_auto_apply or bundle.allowed_for_live_or_demo_execution:
        return False
    return True

def restore_preview_to_text(preview: Dict[str, Any]) -> str:
    return f"Preview for {preview.get('bundle_id')}: allowed={preview.get('restore_allowed')}."
