from typing import Any, Dict, List
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    Phase160HandoffPackage,
    Phase160HandoffContract,
    FinalFreezeCertificate,
    ReleaseCandidateAudit,
    ReleaseCandidateRiskRegister,
    AcceptanceEvidenceBundle,
    create_phase160_handoff_package_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_phase160_handoff_package(
    contract: Phase160HandoffContract,
    certificate: FinalFreezeCertificate,
    audit: ReleaseCandidateAudit,
    risk_register: ReleaseCandidateRiskRegister,
    evidence_bundle: AcceptanceEvidenceBundle
) -> Phase160HandoffPackage:

    valid = contract.contract_valid and certificate.frozen and audit.audit_passed and evidence_bundle.bundle_valid

    pkg = Phase160HandoffPackage(
        package_id=create_phase160_handoff_package_id(),
        created_at_utc=generate_timestamp(),
        contract=contract,
        freeze_certificate=certificate,
        release_candidate_audit=audit,
        risk_register=risk_register,
        evidence_bundle=evidence_bundle,
        package_hash=None,
        package_valid=valid,
        read_only=True,
        research_data_only=True,
        final_delivery_handoff_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        telegram_real_send_enabled=False,
        deployment_allowed=False,
        production_patch_allowed=False,
        strategy_activation_allowed=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    pkg.package_hash = compute_phase160_handoff_package_hash(pkg)

    if not valid:
        pkg.risk_flags.append(AdvancedAcceptanceRiskFlag.PHASE160_HANDOFF_INVALID)

    return pkg

def compute_phase160_handoff_package_hash(package: Phase160HandoffPackage) -> str:
    data = {
        "contract_id": package.contract.contract_id,
        "certificate_id": package.freeze_certificate.certificate_id,
        "audit_id": package.release_candidate_audit.audit_id,
        "valid": package.package_valid
    }
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def validate_phase160_handoff_package(package: Phase160HandoffPackage) -> List[str]:
    errors = []
    if not package.package_valid:
        errors.append("Package is marked invalid")
    if not package.read_only:
        errors.append("Package must be read_only")
    if not package.final_delivery_handoff_only:
        errors.append("Package must be final_delivery_handoff_only")
    if package.live_trading_enabled:
        errors.append("live_trading_enabled must be False")
    return errors

def phase160_handoff_package_to_text(package: Phase160HandoffPackage, limit: int = 300) -> str:
    lines = [
        f"Phase 160 Handoff Package: {package.package_id}",
        f"Valid: {package.package_valid}"
    ]
    return "\n".join(lines)
