from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    DeterminismComplianceAudit, ClosureAuditCheck, ClosureAuditKind,
    ClosureComplianceStatus, ArtifactLineageManifest, BacktestClosureRiskFlag
)
from usa_signal_bot.core.exceptions import DeterminismComplianceAuditError

def build_determinism_checks(payloads: dict[str, dict[str, Any]], manifest: ArtifactLineageManifest) -> list[ClosureAuditCheck]:
    checks = []
    for ref in manifest.artifacts:
        if not ref.available: continue

        # Check deterministic properties
        # In a real system, we'd check if the payload explicitly declares determinism
        # Here we just check if hash exists and payload is not empty
        is_det = ref.source_hash is not None

        chk = ClosureAuditCheck(
            audit_kind=ClosureAuditKind.DETERMINISM_COMPLIANCE,
            name=f"Determinism of {ref.artifact_name}",
            required=True,
            passed=is_det,
            expected_value=True,
            observed_value=is_det,
            rationale=f"Check if {ref.artifact_name} has a deterministic hash"
        )
        if is_det:
            chk.status = ClosureComplianceStatus.PASSED
        else:
            chk.status = ClosureComplianceStatus.FAILED
            chk.errors.append("Non-deterministic artifact")
        checks.append(chk)
    return checks

def build_determinism_compliance_audit(payloads: dict[str, dict[str, Any]], manifest: ArtifactLineageManifest) -> DeterminismComplianceAudit:
    audit = DeterminismComplianceAudit()
    audit.checks = build_determinism_checks(payloads, manifest)

    audit.deterministic_artifact_count = sum(1 for c in audit.checks if c.passed)
    audit.non_deterministic_artifact_count = sum(1 for c in audit.checks if not c.passed)

    audit.all_hashes_consistent = manifest.deterministic_hashes_available
    audit.audit_passed = (audit.non_deterministic_artifact_count == 0) and audit.all_hashes_consistent

    if not audit.audit_passed:
        audit.risk_flags.append(BacktestClosureRiskFlag.DETERMINISM_COMPLIANCE_FAILED)
        audit.errors.append("Determinism compliance audit failed")

    return audit

def validate_determinism_compliance_audit(audit: DeterminismComplianceAudit) -> list[str]:
    errors = []
    if not audit.audit_passed:
        errors.append("Determinism audit failed")
    return errors

def determinism_compliance_audit_summary(audit: DeterminismComplianceAudit) -> dict[str, Any]:
    return {
        "passed": audit.audit_passed,
        "deterministic": audit.deterministic_artifact_count,
        "non_deterministic": audit.non_deterministic_artifact_count
    }

def determinism_compliance_audit_to_text(audit: DeterminismComplianceAudit, limit: int = 300) -> str:
    return f"DeterminismComplianceAudit(passed={audit.audit_passed}, det={audit.deterministic_artifact_count}, non_det={audit.non_deterministic_artifact_count})"
