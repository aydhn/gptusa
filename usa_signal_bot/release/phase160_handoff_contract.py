from typing import Any, Dict, List
from usa_signal_bot.release.phase159_models import (
    Phase160HandoffContract,
    FinalFreezeCertificate,
    ReleaseCandidateAudit,
    create_phase160_handoff_contract_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_phase160_handoff_contract(certificate: FinalFreezeCertificate, audit: ReleaseCandidateAudit) -> Phase160HandoffContract:
    valid = certificate.frozen and audit.audit_passed

    contract = Phase160HandoffContract(
        contract_id=create_phase160_handoff_contract_id(),
        created_at_utc=generate_timestamp(),
        source_freeze_certificate_id=certificate.certificate_id,
        source_release_candidate_audit_id=audit.audit_id,
        read_only=True,
        research_data_only=True,
        final_delivery_handoff_only=True,
        allowed_items=[
            "freeze_certificate",
            "release_candidate_audit",
            "risk_register",
            "evidence_bundle",
            "scenario_matrix"
        ],
        forbidden_fields=[
            "broker_order", "paper_order", "live_order", "sent_to_broker",
            "strategy_active", "deployment_enabled", "production_patch",
            "live_signal", "buy_signal", "sell_signal", "target_weight",
            "portfolio_weight", "actual_target_weight", "allocation",
            "actual_allocation", "capital_allocation", "position_size",
            "order_size", "real_order", "telegram_sent"
        ],
        live_trading_allowed=False,
        paper_trading_allowed=False,
        broker_execution_allowed=False,
        real_order_creation_allowed=False,
        telegram_real_send_allowed=False,
        deployment_allowed=False,
        production_patch_allowed=False,
        strategy_activation_allowed=False,
        contract_valid=valid,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    if not valid:
        contract.risk_flags.append(AdvancedAcceptanceRiskFlag.PHASE160_HANDOFF_INVALID)

    return contract

def validate_phase160_handoff_contract(contract: Phase160HandoffContract) -> List[str]:
    errors = []
    if not contract.read_only:
        errors.append("Contract must be read_only")
    if not contract.final_delivery_handoff_only:
        errors.append("Contract must be final_delivery_handoff_only")
    if contract.live_trading_allowed:
        errors.append("live_trading_allowed must be False")
    if contract.deployment_allowed:
        errors.append("deployment_allowed must be False")
    return errors

def phase160_handoff_contract_to_text(contract: Phase160HandoffContract, limit: int = 300) -> str:
    lines = [
        f"Phase 160 Handoff Contract: {contract.contract_id}",
        f"Valid: {contract.contract_valid}"
    ]
    return "\n".join(lines)
