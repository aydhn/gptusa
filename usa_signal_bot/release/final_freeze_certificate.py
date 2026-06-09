from typing import Any, Dict, List
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    FinalFreezeCertificate,
    ReleaseCandidateAudit,
    FinalFreezeChecklist,
    FinalFreezeBoundaryResult,
    FinalFreezeStatus,
    create_final_freeze_certificate_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_final_freeze_certificate(audit: ReleaseCandidateAudit, checklist: FinalFreezeChecklist, boundary: FinalFreezeBoundaryResult) -> FinalFreezeCertificate:
    frozen = audit.audit_passed and checklist.checklist_valid and boundary.boundary_passed
    status = FinalFreezeStatus.PASSED if frozen else FinalFreezeStatus.FAILED

    cert = FinalFreezeCertificate(
        certificate_id=create_final_freeze_certificate_id(),
        created_at_utc=generate_timestamp(),
        source_audit_id=audit.audit_id,
        source_checklist_id=checklist.checklist_id,
        frozen=frozen,
        freeze_status=status,
        freeze_hash=None,
        next_phase=160,
        ready_for_phase160=frozen,
        not_deployment_approval=True,
        not_trading_approval=True,
        not_investment_advice=True,
        limitations=[
            "This certificate is NOT a deployment approval.",
            "This certificate is NOT a trading approval.",
            "This certificate is NOT investment advice.",
            "Phase 160 is strictly for final system audit and delivery preparation."
        ],
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    cert.freeze_hash = compute_final_freeze_certificate_hash(cert)

    if not frozen:
        cert.risk_flags.append(AdvancedAcceptanceRiskFlag.FINAL_FREEZE_CERTIFICATE_INVALID)

    return cert

def compute_final_freeze_certificate_hash(certificate: FinalFreezeCertificate) -> str:
    data = {
        "source_audit_id": certificate.source_audit_id,
        "source_checklist_id": certificate.source_checklist_id,
        "frozen": certificate.frozen
    }
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def validate_final_freeze_certificate(certificate: FinalFreezeCertificate) -> List[str]:
    errors = []
    if certificate.ready_for_phase160 and not certificate.frozen:
        errors.append("Cannot be ready for Phase160 if not frozen")
    if not certificate.not_deployment_approval:
        errors.append("Must not be deployment approval")
    if not certificate.not_trading_approval:
        errors.append("Must not be trading approval")
    if certificate.next_phase != 160:
        errors.append("Next phase must be 160")
    return errors

def final_freeze_certificate_to_text(certificate: FinalFreezeCertificate, limit: int = 300) -> str:
    lines = [
        f"Final Freeze Certificate: {certificate.certificate_id}",
        f"Frozen: {certificate.frozen}",
        f"Ready for Phase 160: {certificate.ready_for_phase160}"
    ]
    for lim in certificate.limitations[:limit]:
        lines.append(f" - LIMITATION: {lim}")
    return "\n".join(lines)
