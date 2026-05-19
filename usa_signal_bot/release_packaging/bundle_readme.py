from typing import Optional
from usa_signal_bot.release_packaging.packaging_models import VersionedCandidateBundle, BundleManifest, BundleValidationResult

def generate_bundle_readme(bundle: VersionedCandidateBundle) -> str:
    readme = f"# Release Candidate Bundle: {bundle.bundle_id}\n\n"
    readme += f"Version: {bundle.bundle_version}\n"
    readme += f"Title: {bundle.title}\n"
    readme += f"Description: {bundle.description}\n\n"

    readme += generate_bundle_limitations_section()
    readme += "\n"
    readme += generate_bundle_safety_section(bundle)
    readme += "\n"
    readme += generate_bundle_artifact_section(bundle.manifest)
    readme += "\n"
    readme += generate_bundle_validation_section(bundle.validation_result)

    return readme

def generate_bundle_limitations_section() -> str:
    return """## Limitations & Disclaimers
- No broker/live/demo order execution is supported by this bundle.
- No auto apply to production is permitted.
- No production config patching happens from this bundle.
- This bundle is solely a local research package.
- A PASS status does not constitute investment advice or live trading approval.
- Past performance guarantees no future results.
"""

def generate_bundle_safety_section(bundle: VersionedCandidateBundle) -> str:
    return f"## Safety\nAllowed for Auto Apply: {bundle.allowed_for_auto_apply}\nAllowed for Live/Demo: {bundle.allowed_for_live_or_demo_execution}\n"

def generate_bundle_artifact_section(manifest: Optional[BundleManifest]) -> str:
    if not manifest:
        return "## Artifacts\nNo manifest provided.\n"
    return f"## Artifacts\nIncluded artifacts: {len(manifest.artifacts)}\nMissing required: {manifest.missing_artifact_types}\n"

def generate_bundle_validation_section(validation: Optional[BundleValidationResult]) -> str:
    if not validation:
        return "## Validation\nNot validated yet.\n"
    return f"## Validation\nStatus: {validation.status.value}\nSafety Flags: {[f.value for f in validation.safety_flags]}\n"

def bundle_readme_to_text(bundle: VersionedCandidateBundle) -> str:
    return generate_bundle_readme(bundle)
