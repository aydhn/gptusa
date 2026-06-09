from typing import Any, Dict, List
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    AcceptanceAreaReport,
    AcceptanceEvidenceBundle,
    AdvancedDryRunStep,
    AcceptanceAreaKind,
    ReleaseCandidateStatus,
    create_acceptance_area_report_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_storage_acceptance_report(bundle: AcceptanceEvidenceBundle, steps: List[AdvancedDryRunStep]) -> AcceptanceAreaReport:
    evidence_ids = []
    passed = True
    findings = []

    target_area = AcceptanceAreaKind.STORAGE

    for item in bundle.evidence_items:
        if item.area_kind == target_area:
            evidence_ids.append(item.evidence_id)
            if not item.valid:
                passed = False
                findings.append(f"Invalid storage evidence: {item.evidence_name}")

    for step in steps:
        if step.area_kind == target_area:
            if step.status != ReleaseCandidateStatus.PASSED:
                passed = False
                findings.append(f"Failed storage step: {step.step_name}")

    status = ReleaseCandidateStatus.PASSED if passed else ReleaseCandidateStatus.FAILED

    report = AcceptanceAreaReport(
        report_id=create_acceptance_area_report_id(),
        created_at_utc=generate_timestamp(),
        area_kind=target_area,
        title="Storage Acceptance",
        status=status,
        passed=passed,
        checked_items=len(evidence_ids) + len(steps),
        warning_count=0,
        error_count=len(findings) if not passed else 0,
        blocked_count=0,
        findings=findings,
        evidence_ids=evidence_ids,
        report_hash=None,
        report_valid=True,
        dry_run_only=True,
        no_real_side_effects=True,
        not_deployment_approval=True,
        not_trading_approval=True,
        not_investment_advice=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    data = {"title": report.title, "passed": report.passed, "findings": report.findings}
    report.report_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    if not passed:
        report.risk_flags.append(AdvancedAcceptanceRiskFlag.SYSTEM_AREA_ACCEPTANCE_FAILED)

    return report

def validate_storage_acceptance_report(report: AcceptanceAreaReport) -> List[str]:
    errors = []
    if not report.report_valid:
        errors.append("Report is invalid")
    if not report.dry_run_only:
        errors.append("Report must be dry_run_only")
    if not report.no_real_side_effects:
        errors.append("Report must have no real side effects")
    return errors

def storage_acceptance_report_to_text(report: AcceptanceAreaReport, limit: int = 300) -> str:
    lines = [f"Storage Report: {report.title} [{report.status.value}]"]
    for f in report.findings[:limit]:
        lines.append(f" - {f}")
    return "\n".join(lines)
