from typing import Any, Dict, List, Optional
from usa_signal_bot.provider_freeze.phase114_models import (
    DataLayerOutputContract,
    DataLayerRehearsalStep,
    create_output_contract_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import DataLayerOutputContractStatus, ProviderFreezeRiskFlag

def build_data_layer_output_contract() -> DataLayerOutputContract:
    return DataLayerOutputContract(
        contract_id=create_output_contract_id(),
        created_at_utc=_utcnow_str(),
        allowed_output_kinds=[
            "provider_metadata", "cache_metadata", "quality_score", "source_trust",
            "provider_route_metadata", "source_blend_metadata", "event_context_metadata",
            "calendar_validation_metadata", "lineage_metadata", "audit_metadata",
            "rehearsal_report"
        ],
        blocked_output_kinds=[
            "trade_signal", "order_decision", "broker_instruction", "paper_state_mutation",
            "telegram_live_send", "dashboard_payload", "scraped_html", "paid_api_payload"
        ],
        metadata_only_required=True,
        research_data_only_required=True,
        trade_signal_blocked=True,
        order_decision_blocked=True,
        execution_blocked=True,
        broker_blocked=True,
        paper_mutation_blocked=True,
        telegram_real_send_blocked=True,
        scraping_blocked=True,
        html_parsing_blocked=True,
        paid_api_blocked=True,
        network_default_enabled_blocked=True,
        contract_valid=True,
        status=DataLayerOutputContractStatus.PASS
    )

def validate_data_layer_output_contract(contract: DataLayerOutputContract) -> List[str]:
    errors = []
    if not contract.trade_signal_blocked:
        errors.append("trade_signal must be blocked.")
    if not contract.order_decision_blocked:
        errors.append("order_decision must be blocked.")
    if not contract.execution_blocked:
        errors.append("execution must be blocked.")
    if not contract.broker_blocked:
        errors.append("broker must be blocked.")
    if not contract.paper_mutation_blocked:
        errors.append("paper mutation must be blocked.")
    if not contract.telegram_real_send_blocked:
        errors.append("telegram_real_send must be blocked.")
    if not contract.scraping_blocked:
        errors.append("scraping must be blocked.")
    if not contract.html_parsing_blocked:
        errors.append("html parsing must be blocked.")
    if not contract.paid_api_blocked:
        errors.append("paid api must be blocked.")
    if not contract.network_default_enabled_blocked:
        errors.append("network_default_enabled must be blocked.")
    return errors

def check_rehearsal_step_output_contract(step: DataLayerRehearsalStep, contract: Optional[DataLayerOutputContract] = None) -> DataLayerOutputContractStatus:
    if not contract:
        contract = build_data_layer_output_contract()

    for blocked in contract.blocked_output_kinds:
        if blocked in step.outputs:
            step.risk_flags.append(ProviderFreezeRiskFlag.OUTPUT_CONTRACT_FAILED)
            return DataLayerOutputContractStatus.FAIL

    if step.produces_trade_signal or step.produces_order_decision:
        step.risk_flags.append(ProviderFreezeRiskFlag.OUTPUT_CONTRACT_FAILED)
        return DataLayerOutputContractStatus.FAIL

    if (step.network_used or step.paid_api_used or step.scraping_used or
        step.html_parsing_used or step.broker_used or step.order_created or
        step.paper_state_mutated or step.telegram_real_sent or step.dashboard_started):
        step.risk_flags.append(ProviderFreezeRiskFlag.OUTPUT_CONTRACT_FAILED)
        return DataLayerOutputContractStatus.FAIL

    return DataLayerOutputContractStatus.PASS

def output_contract_summary(contract: DataLayerOutputContract) -> Dict[str, Any]:
    return {
        "status": contract.status.value,
        "valid": contract.contract_valid,
        "allowed_count": len(contract.allowed_output_kinds),
        "blocked_count": len(contract.blocked_output_kinds)
    }

def output_contract_to_text(contract: DataLayerOutputContract) -> str:
    lines = [
        f"Data Layer Output Contract: {contract.contract_id}",
        f"Status: {contract.status.value}",
        f"Valid: {contract.contract_valid}",
        "Allowed Kinds: " + ", ".join(contract.allowed_output_kinds),
        "Blocked Kinds: " + ", ".join(contract.blocked_output_kinds)
    ]
    return "\n".join(lines)
