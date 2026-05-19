from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    ReleaseBundleStatus, ReleaseBundleType, FrozenArtifactStatus,
    FrozenArtifactSource, BundleValidationStatus, BundleSafetyFlag,
    BundleCompatibilityStatus, BundleReportType
)
from usa_signal_bot.core.exceptions import ReleasePackagingValidationError

@dataclass
class FrozenArtifact:
    artifact_id: str
    created_at_utc: str
    source: FrozenArtifactSource
    artifact_type: str
    source_ref: Optional[str]
    status: FrozenArtifactStatus
    path: Optional[str]
    payload_hash: Optional[str]
    payload_size_bytes: Optional[int]
    summary: Dict[str, Any]
    safety_flags: List[BundleSafetyFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BundleManifest:
    manifest_id: str
    created_at_utc: str
    bundle_id: str
    bundle_version: str
    bundle_type: ReleaseBundleType
    bundle_status: ReleaseBundleStatus
    source_candidate_id: Optional[str]
    source_experiment_id: Optional[str]
    source_governance_review_id: Optional[str]
    artifacts: List[FrozenArtifact]
    required_artifact_types: List[str]
    missing_artifact_types: List[str]
    manifest_hash: Optional[str]
    schema_version: str
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BundleValidationResult:
    validation_id: str
    created_at_utc: str
    bundle_id: str
    status: BundleValidationStatus
    compatibility_status: BundleCompatibilityStatus
    safety_flags: List[BundleSafetyFlag]
    checksum_verified: bool
    required_artifacts_present: bool
    secret_scan_passed: bool
    broker_field_scan_passed: bool
    auto_apply_scan_passed: bool
    validation_messages: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VersionedCandidateBundle:
    bundle_id: str
    created_at_utc: str
    bundle_version: str
    bundle_type: ReleaseBundleType
    status: ReleaseBundleStatus
    title: str
    description: str
    source_candidate_id: Optional[str]
    source_experiment_id: Optional[str]
    source_hypothesis_id: Optional[str]
    source_governance_review_id: Optional[str]
    manifest: Optional[BundleManifest]
    validation_result: Optional[BundleValidationResult]
    bundle_path: Optional[str]
    readme_path: Optional[str]
    allowed_for_auto_apply: bool
    allowed_for_live_or_demo_execution: bool
    allowed_for_order_routing: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleasePackagingReview:
    review_id: str
    created_at_utc: str
    report_type: BundleReportType
    bundles: List[VersionedCandidateBundle]
    manifests: List[BundleManifest]
    frozen_artifacts: List[FrozenArtifact]
    validation_results: List[BundleValidationResult]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def frozen_artifact_to_dict(item: FrozenArtifact) -> dict:
    return {
        "artifact_id": item.artifact_id,
        "created_at_utc": item.created_at_utc,
        "source": item.source.value,
        "artifact_type": item.artifact_type,
        "source_ref": item.source_ref,
        "status": item.status.value,
        "path": item.path,
        "payload_hash": item.payload_hash,
        "payload_size_bytes": item.payload_size_bytes,
        "summary": item.summary,
        "safety_flags": [f.value for f in item.safety_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def bundle_manifest_to_dict(item: BundleManifest) -> dict:
    return {
        "manifest_id": item.manifest_id,
        "created_at_utc": item.created_at_utc,
        "bundle_id": item.bundle_id,
        "bundle_version": item.bundle_version,
        "bundle_type": item.bundle_type.value,
        "bundle_status": item.bundle_status.value,
        "source_candidate_id": item.source_candidate_id,
        "source_experiment_id": item.source_experiment_id,
        "source_governance_review_id": item.source_governance_review_id,
        "artifacts": [frozen_artifact_to_dict(a) for a in item.artifacts],
        "required_artifact_types": item.required_artifact_types,
        "missing_artifact_types": item.missing_artifact_types,
        "manifest_hash": item.manifest_hash,
        "schema_version": item.schema_version,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def bundle_validation_result_to_dict(item: BundleValidationResult) -> dict:
    return {
        "validation_id": item.validation_id,
        "created_at_utc": item.created_at_utc,
        "bundle_id": item.bundle_id,
        "status": item.status.value,
        "compatibility_status": item.compatibility_status.value,
        "safety_flags": [f.value for f in item.safety_flags],
        "checksum_verified": item.checksum_verified,
        "required_artifacts_present": item.required_artifacts_present,
        "secret_scan_passed": item.secret_scan_passed,
        "broker_field_scan_passed": item.broker_field_scan_passed,
        "auto_apply_scan_passed": item.auto_apply_scan_passed,
        "validation_messages": item.validation_messages,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def versioned_candidate_bundle_to_dict(item: VersionedCandidateBundle) -> dict:
    return {
        "bundle_id": item.bundle_id,
        "created_at_utc": item.created_at_utc,
        "bundle_version": item.bundle_version,
        "bundle_type": item.bundle_type.value,
        "status": item.status.value,
        "title": item.title,
        "description": item.description,
        "source_candidate_id": item.source_candidate_id,
        "source_experiment_id": item.source_experiment_id,
        "source_hypothesis_id": item.source_hypothesis_id,
        "source_governance_review_id": item.source_governance_review_id,
        "manifest": bundle_manifest_to_dict(item.manifest) if item.manifest else None,
        "validation_result": bundle_validation_result_to_dict(item.validation_result) if item.validation_result else None,
        "bundle_path": item.bundle_path,
        "readme_path": item.readme_path,
        "allowed_for_auto_apply": item.allowed_for_auto_apply,
        "allowed_for_live_or_demo_execution": item.allowed_for_live_or_demo_execution,
        "allowed_for_order_routing": item.allowed_for_order_routing,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def release_packaging_review_to_dict(item: ReleasePackagingReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "bundles": [versioned_candidate_bundle_to_dict(b) for b in item.bundles],
        "manifests": [bundle_manifest_to_dict(m) for m in item.manifests],
        "frozen_artifacts": [frozen_artifact_to_dict(a) for a in item.frozen_artifacts],
        "validation_results": [bundle_validation_result_to_dict(v) for v in item.validation_results],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors
    }

def validate_frozen_artifact(item: FrozenArtifact) -> None:
    if item.payload_size_bytes is not None and item.payload_size_bytes < 0:
        raise ReleasePackagingValidationError("payload_size_bytes negatif olamaz.")

def validate_bundle_manifest(item: BundleManifest) -> None:
    if not item.bundle_version:
        raise ReleasePackagingValidationError("bundle_version boş olamaz.")
    if not item.schema_version:
        raise ReleasePackagingValidationError("schema_version boş olamaz.")

def validate_bundle_validation_result(item: BundleValidationResult) -> None:
    pass

def validate_versioned_candidate_bundle(item: VersionedCandidateBundle) -> None:
    if not item.bundle_version:
        raise ReleasePackagingValidationError("bundle_version boş olamaz.")
    if item.allowed_for_auto_apply:
        raise ReleasePackagingValidationError("allowed_for_auto_apply false olmalı.")
    if item.allowed_for_live_or_demo_execution:
        raise ReleasePackagingValidationError("allowed_for_live_or_demo_execution false olmalı.")
    if item.allowed_for_order_routing:
        raise ReleasePackagingValidationError("allowed_for_order_routing false olmalı.")

def validate_release_packaging_review(item: ReleasePackagingReview) -> None:
    pass

def create_frozen_artifact_id(prefix: str = "frozen_artifact") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_bundle_manifest_id(prefix: str = "bundle_manifest") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_bundle_validation_result_id(prefix: str = "bundle_validation") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_versioned_candidate_bundle_id(prefix: str = "candidate_bundle") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_release_packaging_review_id(prefix: str = "release_packaging_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
