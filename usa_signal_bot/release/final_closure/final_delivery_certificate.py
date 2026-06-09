from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalDeliveryCertificate,
    FinalSystemAuditReport,
    FinalSafetyClosure,
    FinalLimitationRegister,
    ProjectClosureStatus,
    FinalClosureRiskFlag,
    create_final_delivery_certificate_id,
    generate_timestamp
)
import hashlib
import json

def compute_final_delivery_certificate_hash(certificate: FinalDeliveryCertificate) -> str:
    state = {
        "project_name": certificate.project_name,
        "total_phases": certificate.total_phases,
        "final_phase": certificate.final_phase,
        "source_audit_id": certificate.source_audit_id,
        "source_safety_closure_id": certificate.source_safety_closure_id,
        "source_limitation_register_id": certificate.source_limitation_register_id,
        "delivered": certificate.delivered,
        "delivery_status": certificate.delivery_status.value
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_delivery_certificate(
    audit: FinalSystemAuditReport,
    safety: FinalSafetyClosure,
    limitations: FinalLimitationRegister
) -> FinalDeliveryCertificate:

    delivered = audit.audit_passed and safety.safety_closure_passed and limitations.register_valid and limitations.blocking_limitation_count == 0
    status = ProjectClosureStatus.CLOSED if delivered else ProjectClosureStatus.FAILED

    errors = []
    risk_flags = []
    if not delivered:
        errors.append("Final delivery criteria not met (audit failed, safety failed, or blocking limitations exist).")
        risk_flags.append(FinalClosureRiskFlag.FINAL_DELIVERY_CERTIFICATE_INVALID)

    cert = FinalDeliveryCertificate(
        certificate_id=create_final_delivery_certificate_id(),
        created_at_utc=generate_timestamp(),
        project_name="USA Signal Bot",
        total_phases=160,
        final_phase=160,
        source_audit_id=audit.audit_id,
        source_safety_closure_id=safety.closure_id,
        source_limitation_register_id=limitations.register_id,
        delivered=delivered,
        delivery_status=status,
        certificate_hash=None,
        not_deployment_approval=True,
        not_trading_approval=True,
        not_broker_approval=True,
        not_investment_advice=True,
        limitations=[l.title for l in limitations.limitations],
        next_steps=["Canlı/paper aktivasyonun ayrı, kontrollü bir çalışma gerektirir."],
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

    cert.certificate_hash = compute_final_delivery_certificate_hash(cert)
    return cert

def validate_final_delivery_certificate(certificate: FinalDeliveryCertificate) -> List[str]:
    errors = []
    if not certificate.delivered:
        errors.extend(certificate.errors)
    if certificate.project_name != "USA Signal Bot":
        errors.append("Project name must be 'USA Signal Bot'.")
    if certificate.total_phases != 160 or certificate.final_phase != 160:
        errors.append("Total phases and final phase must be 160.")
    return errors

def final_delivery_certificate_to_text(certificate: FinalDeliveryCertificate, limit: int = 300) -> str:
    return f"Final Delivery Certificate: Delivered={certificate.delivered}, Status={certificate.delivery_status.value}"
