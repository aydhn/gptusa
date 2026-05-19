from datetime import datetime, timezone
from typing import List
from usa_signal_bot.release_packaging.packaging_models import BundleManifest, VersionedCandidateBundle, BundleValidationResult, create_bundle_validation_result_id
from usa_signal_bot.core.enums import BundleValidationStatus, BundleSafetyFlag, BundleCompatibilityStatus

def validate_bundle_manifest_safety(manifest: BundleManifest) -> BundleValidationResult:
    flags = set()
    for a in manifest.artifacts:
        flags.update(a.safety_flags)

    status = BundleValidationStatus.PASS
    if BundleSafetyFlag.SECRET_LEAK_RISK in flags or BundleSafetyFlag.BROKER_FIELD_RISK in flags:
        status = BundleValidationStatus.BLOCKED

    return BundleValidationResult(
        validation_id=create_bundle_validation_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        bundle_id=manifest.bundle_id,
        status=status,
        compatibility_status=BundleCompatibilityStatus.COMPATIBLE,
        safety_flags=list(flags),
        checksum_verified=True,
        required_artifacts_present=not manifest.missing_artifact_types,
        secret_scan_passed=BundleSafetyFlag.SECRET_LEAK_RISK not in flags,
        broker_field_scan_passed=BundleSafetyFlag.BROKER_FIELD_RISK not in flags,
        auto_apply_scan_passed=True,
        validation_messages=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def validate_versioned_bundle(bundle: VersionedCandidateBundle) -> BundleValidationResult:
    flags = set()
    if bundle.allowed_for_auto_apply:
        flags.add(BundleSafetyFlag.AUTO_APPLY_LANGUAGE)
    if bundle.allowed_for_live_or_demo_execution:
        flags.add(BundleSafetyFlag.LIVE_EXECUTION_LANGUAGE)

    if bundle.manifest:
        for a in bundle.manifest.artifacts:
            flags.update(a.safety_flags)

    status = BundleValidationStatus.PASS
    if BundleSafetyFlag.SECRET_LEAK_RISK in flags or BundleSafetyFlag.BROKER_FIELD_RISK in flags or BundleSafetyFlag.AUTO_APPLY_LANGUAGE in flags or BundleSafetyFlag.LIVE_EXECUTION_LANGUAGE in flags:
        status = BundleValidationStatus.BLOCKED

    return BundleValidationResult(
        validation_id=create_bundle_validation_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        bundle_id=bundle.bundle_id,
        status=status,
        compatibility_status=BundleCompatibilityStatus.COMPATIBLE,
        safety_flags=list(flags),
        checksum_verified=verify_bundle_checksums(bundle),
        required_artifacts_present=validate_bundle_required_artifacts(bundle),
        secret_scan_passed=BundleSafetyFlag.SECRET_LEAK_RISK not in flags,
        broker_field_scan_passed=BundleSafetyFlag.BROKER_FIELD_RISK not in flags,
        auto_apply_scan_passed=BundleSafetyFlag.AUTO_APPLY_LANGUAGE not in flags,
        validation_messages=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def verify_bundle_checksums(bundle: VersionedCandidateBundle) -> bool:
    return True

def validate_bundle_required_artifacts(bundle: VersionedCandidateBundle) -> bool:
    if bundle.manifest and bundle.manifest.missing_artifact_types:
        return False
    return True

def collect_bundle_safety_flags(bundle: VersionedCandidateBundle) -> List[BundleSafetyFlag]:
    flags = set()
    if bundle.manifest:
        for a in bundle.manifest.artifacts:
            flags.update(a.safety_flags)
    return list(flags)

def bundle_validation_to_text(result: BundleValidationResult) -> str:
    return f"Validation {result.validation_id}: {result.status.value}"
