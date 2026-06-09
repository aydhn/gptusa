from typing import Any, Dict, List
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    ReleaseCandidateAudit,
    AcceptanceAreaReport,
    ReleaseCandidateRiskRegister,
    ReleaseCandidateStatus,
    create_release_candidate_audit_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_release_candidate_audit(area_reports: List[AcceptanceAreaReport], risk_register: ReleaseCandidateRiskRegister) -> ReleaseCandidateAudit:
    passed_count = sum(1 for r in area_reports if r.passed)
    failed_count = sum(1 for r in area_reports if not r.passed)

    passed = passed_count == len(area_reports) and risk_register.blocking_risk_count == 0
    status = ReleaseCandidateStatus.PASSED if passed else ReleaseCandidateStatus.FAILED

    if risk_register.release_candidate_blocked:
        status = ReleaseCandidateStatus.BLOCKED
        passed = False

    audit = ReleaseCandidateAudit(
        audit_id=create_release_candidate_audit_id(),
        created_at_utc=generate_timestamp(),
        area_reports=area_reports,
        risk_register=risk_register,
        audit_status=status,
        audit_passed=passed,
        passed_area_count=passed_count,
        warning_area_count=0,
        failed_area_count=failed_count,
        blocked_area_count=1 if status == ReleaseCandidateStatus.BLOCKED else 0,
        audit_hash=None,
        not_deployment_approval=True,
        not_trading_approval=True,
        not_investment_advice=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    audit.audit_hash = compute_release_candidate_audit_hash(audit)

    if not passed:
        audit.risk_flags.append(AdvancedAcceptanceRiskFlag.RELEASE_CANDIDATE_AUDIT_FAILED)

    return audit

def compute_release_candidate_audit_hash(audit: ReleaseCandidateAudit) -> str:
    data = {
        "status": audit.audit_status.value,
        "passed_areas": audit.passed_area_count,
        "failed_areas": audit.failed_area_count,
        "blocking_risks": audit.risk_register.blocking_risk_count
    }
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def validate_release_candidate_audit(audit: ReleaseCandidateAudit) -> List[str]:
    errors = []
    if audit.risk_register.blocking_risk_count > 0 and audit.audit_passed:
        errors.append("Audit cannot pass with blocking risks")
    if audit.failed_area_count > 0 and audit.audit_passed:
        errors.append("Audit cannot pass with failed area reports")
    return errors

def release_candidate_audit_to_text(audit: ReleaseCandidateAudit, limit: int = 300) -> str:
    lines = [
        f"Release Candidate Audit: {audit.audit_id}",
        f"Status: {audit.audit_status.value}",
        f"Passed Areas: {audit.passed_area_count}",
        f"Failed Areas: {audit.failed_area_count}",
        f"Blocking Risks: {audit.risk_register.blocking_risk_count}"
    ]
    return "\n".join(lines)
