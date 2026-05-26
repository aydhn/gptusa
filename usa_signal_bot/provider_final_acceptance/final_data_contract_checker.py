from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    FeatureFactorDataContract,
    FeatureFactorKickoffGateStatus,
    create_feature_factor_data_contract_id,
    _utc_now
)

def build_feature_factor_data_contract() -> FeatureFactorDataContract:
    return FeatureFactorDataContract(
        contract_id=create_feature_factor_data_contract_id(),
        created_at_utc=_utc_now(),
        status=FeatureFactorKickoffGateStatus.PASSED_METADATA_ONLY,
        allowed_input_kinds=[
            "ohlcv_cache_metadata",
            "normalized_ohlcv_records",
            "provider_quality_score",
            "source_trust_profile",
            "provider_route_metadata",
            "source_blend_metadata",
            "event_context_metadata",
            "event_impact_metadata",
            "calendar_validation_metadata",
            "data_lineage_metadata",
            "audit_metadata"
        ],
        blocked_output_kinds=[
            "trade_signal",
            "order_decision",
            "broker_instruction",
            "paper_state_mutation",
            "live_order",
            "demo_order",
            "telegram_real_send",
            "dashboard_payload",
            "scraped_html",
            "paid_api_payload"
        ],
        ohlcv_input_allowed=True,
        event_context_input_allowed=True,
        quality_metadata_input_allowed=True,
        lineage_metadata_required=True,
        metadata_only_required=True,
        research_data_only_required=True,
        trade_signal_blocked=True,
        order_decision_blocked=True,
        broker_blocked=True,
        paper_mutation_blocked=True,
        telegram_real_send_blocked=True,
        scraping_blocked=True,
        html_parsing_blocked=True,
        paid_api_blocked=True,
        dashboard_blocked=True,
        network_default_enabled_blocked=True,
        contract_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_feature_factor_data_contract_safety(contract: FeatureFactorDataContract) -> list[str]:
    errors = []
    if not contract.trade_signal_blocked:
        errors.append("trade_signal is not blocked.")
    if not contract.order_decision_blocked:
        errors.append("order_decision is not blocked.")
    if not contract.broker_blocked:
        errors.append("broker is not blocked.")
    if not contract.paper_mutation_blocked:
        errors.append("paper_mutation is not blocked.")
    if not contract.telegram_real_send_blocked:
        errors.append("telegram_real_send is not blocked.")
    if not contract.scraping_blocked:
        errors.append("scraping is not blocked.")
    if not contract.html_parsing_blocked:
        errors.append("html_parsing is not blocked.")
    if not contract.paid_api_blocked:
        errors.append("paid_api is not blocked.")
    if not contract.dashboard_blocked:
        errors.append("dashboard is not blocked.")
    if not contract.network_default_enabled_blocked:
        errors.append("network_default_enabled is not blocked.")
    return errors

def feature_factor_data_contract_allows_trade_signal(contract: FeatureFactorDataContract) -> bool:
    return not contract.trade_signal_blocked

def feature_factor_data_contract_allows_order_decision(contract: FeatureFactorDataContract) -> bool:
    return not contract.order_decision_blocked

def feature_factor_data_contract_summary(contract: FeatureFactorDataContract) -> dict[str, Any]:
    return {"valid": contract.contract_valid}

def feature_factor_data_contract_to_text(contract: FeatureFactorDataContract) -> str:
    return f"Data Contract [{contract.status}] - Valid: {contract.contract_valid}"
