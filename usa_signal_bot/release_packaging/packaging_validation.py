from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.release_packaging.packaging_models import (
    FrozenArtifact, BundleManifest, BundleValidationResult,
    VersionedCandidateBundle, ReleasePackagingReview
)
from usa_signal_bot.release_packaging.safety_scanner import (
    scan_text_for_secret_like_patterns, scan_payload_for_broker_order_fields,
    scan_text_for_live_execution_language, scan_text_for_auto_apply_language
)
from usa_signal_bot.core.exceptions import ReleasePackagingValidationError

@dataclass
class ReleasePackagingValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleasePackagingValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ReleasePackagingValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[ReleasePackagingValidationIssue]) -> ReleasePackagingValidationReport:
    warnings = [i for i in issues if i.severity == "WARNING"]
    errors = [i for i in issues if i.severity == "ERROR"]
    blocked = [i for i in issues if i.severity == "BLOCKED"]

    return ReleasePackagingValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=[w.message for w in warnings],
        errors=[e.message for e in errors] + [b.message for b in blocked]
    )

def validate_frozen_artifacts_report(items: List[FrozenArtifact]) -> ReleasePackagingValidationReport:
    issues = []
    for item in items:
        if item.status.value in ["BLOCKED", "INVALID"]:
            issues.append(ReleasePackagingValidationIssue("BLOCKED", "status", f"Artifact {item.artifact_id} is blocked or invalid."))
    return _create_report(issues)

def validate_bundle_manifest_report(item: BundleManifest) -> ReleasePackagingValidationReport:
    issues = []
    if not item.bundle_version:
        issues.append(ReleasePackagingValidationIssue("ERROR", "bundle_version", "Missing bundle version"))
    if item.missing_artifact_types:
        issues.append(ReleasePackagingValidationIssue("ERROR", "artifacts", f"Missing required artifacts: {item.missing_artifact_types}"))
    return _create_report(issues)

def validate_bundle_validation_result_report(item: BundleValidationResult) -> ReleasePackagingValidationReport:
    issues = []
    if item.status.value in ["FAIL", "BLOCKED"]:
        issues.append(ReleasePackagingValidationIssue(item.status.value, "status", f"Validation status is {item.status.value}"))
    if not item.checksum_verified:
        issues.append(ReleasePackagingValidationIssue("ERROR", "checksum_verified", "Checksum mismatch"))
    return _create_report(issues)

def validate_versioned_bundle_report(item: VersionedCandidateBundle) -> ReleasePackagingValidationReport:
    issues = []
    if item.allowed_for_auto_apply:
        issues.append(ReleasePackagingValidationIssue("ERROR", "allowed_for_auto_apply", "Must be false"))
    if item.allowed_for_live_or_demo_execution:
        issues.append(ReleasePackagingValidationIssue("ERROR", "allowed_for_live_or_demo_execution", "Must be false"))
    if item.allowed_for_order_routing:
        issues.append(ReleasePackagingValidationIssue("ERROR", "allowed_for_order_routing", "Must be false"))
    if not item.manifest:
        issues.append(ReleasePackagingValidationIssue("ERROR", "manifest", "Missing manifest"))
    return _create_report(issues)

def validate_release_packaging_review_report(item: ReleasePackagingReview) -> ReleasePackagingValidationReport:
    issues = []
    for b in item.bundles:
        rep = validate_versioned_bundle_report(b)
        issues.extend(rep.issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_bundle_payload(payload: Dict[str, Any]) -> ReleasePackagingValidationReport:
    text = json.dumps(payload)
    flags = scan_text_for_secret_like_patterns(text)
    issues = []
    if flags:
        issues.append(ReleasePackagingValidationIssue("BLOCKED", "secrets", "Secret like patterns found"))
    return _create_report(issues)

def validate_no_live_execution_language_in_bundle(text: str) -> ReleasePackagingValidationReport:
    flags = scan_text_for_live_execution_language(text)
    issues = []
    if flags:
        issues.append(ReleasePackagingValidationIssue("BLOCKED", "live_language", "Live execution language found"))
    return _create_report(issues)

def validate_no_auto_apply_or_production_language(text: str) -> ReleasePackagingValidationReport:
    flags = scan_text_for_auto_apply_language(text)
    issues = []
    if flags:
        issues.append(ReleasePackagingValidationIssue("BLOCKED", "auto_apply_language", "Auto apply language found"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_bundle(payload: Dict[str, Any]) -> ReleasePackagingValidationReport:
    flags = scan_payload_for_broker_order_fields(payload)
    issues = []
    if flags:
        issues.append(ReleasePackagingValidationIssue("BLOCKED", "broker_fields", "Broker order fields found"))
    return _create_report(issues)

def release_packaging_validation_report_to_text(report: ReleasePackagingValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}, Blocked: {report.blocked_count}"

def assert_release_packaging_valid(report: ReleasePackagingValidationReport) -> None:
    if not report.valid:
        raise ReleasePackagingValidationError(f"Packaging validation failed: {report.errors}")
