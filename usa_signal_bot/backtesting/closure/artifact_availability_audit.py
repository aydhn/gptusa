from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    ArtifactAvailabilityAudit, ClosureAuditCheck, ClosureAuditKind,
    ClosureComplianceStatus, ArtifactLineageManifest, BacktestClosureRiskFlag
)
from usa_signal_bot.core.exceptions import ArtifactAvailabilityAuditError

def build_availability_checks(manifest: ArtifactLineageManifest) -> list[ClosureAuditCheck]:
    checks = []
    for ref in manifest.artifacts:
        chk = ClosureAuditCheck(
            audit_kind=ClosureAuditKind.ARTIFACT_AVAILABILITY,
            name=f"Availability of {ref.artifact_name}",
            required=ref.required,
            passed=ref.available,
            expected_value=True,
            observed_value=ref.available,
            rationale=f"Check if {ref.artifact_name} is available"
        )
        if ref.available:
            chk.status = ClosureComplianceStatus.PASSED
        else:
            if ref.required:
                chk.status = ClosureComplianceStatus.FAILED
                chk.errors.append("Required artifact missing")
            else:
                chk.status = ClosureComplianceStatus.WARNING
                chk.warnings.append("Optional artifact missing")
        checks.append(chk)
    return checks

def build_artifact_availability_audit(manifest: ArtifactLineageManifest) -> ArtifactAvailabilityAudit:
    audit = ArtifactAvailabilityAudit()
    audit.checks = build_availability_checks(manifest)

    audit.required_artifact_count = sum(1 for c in audit.checks if c.required)
    audit.available_artifact_count = sum(1 for c in audit.checks if c.passed)
    audit.missing_artifact_count = sum(1 for c in audit.checks if c.required and not c.passed)

    audit.audit_passed = (audit.missing_artifact_count == 0)

    if not audit.audit_passed:
        audit.risk_flags.append(BacktestClosureRiskFlag.ARTIFACT_AVAILABILITY_INVALID)
        audit.errors.append("Artifact availability audit failed")

    return audit

def validate_artifact_availability_audit(audit: ArtifactAvailabilityAudit) -> list[str]:
    errors = []
    if not audit.audit_passed:
        errors.append("Availability audit failed")
    return errors

def artifact_availability_audit_summary(audit: ArtifactAvailabilityAudit) -> dict[str, Any]:
    return {
        "passed": audit.audit_passed,
        "available": audit.available_artifact_count,
        "missing": audit.missing_artifact_count
    }

def artifact_availability_audit_to_text(audit: ArtifactAvailabilityAudit, limit: int = 300) -> str:
    return f"ArtifactAvailabilityAudit(passed={audit.audit_passed}, available={audit.available_artifact_count}, missing={audit.missing_artifact_count})"
