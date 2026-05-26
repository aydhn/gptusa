import datetime
from typing import Any
from usa_signal_bot.feature_engine.phase116_models import FeatureInputContract, create_feature_input_contract_id

def build_feature_input_contract() -> FeatureInputContract:
    return FeatureInputContract(
        contract_id=create_feature_input_contract_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        allowed_input_kinds=["OHLCV", "EVENT_METADATA", "QUALITY_METADATA"],
        required_ohlcv_columns=[
            "symbol", "timestamp", "open", "high", "low",
            "close", "adjusted_close", "volume", "source",
            "fetched_at_utc", "quality_flags"
        ],
        optional_metadata_inputs=[
            "provider_quality_score", "source_trust_profile",
            "provider_route_metadata", "source_blend_metadata",
            "event_context_metadata", "event_impact_metadata",
            "calendar_validation_metadata", "data_lineage_metadata",
            "audit_metadata"
        ],
        event_context_allowed=True,
        quality_metadata_allowed=True,
        calendar_metadata_allowed=True,
        lineage_metadata_required=True,
        metadata_only_required=True,
        research_data_only_required=True,
        network_allowed=False,
        paid_api_allowed=False,
        scraping_allowed=False,
        html_parsing_allowed=False,
        broker_allowed=False,
        order_allowed=False,
        paper_mutation_allowed=False,
        telegram_real_send_allowed=False,
        dashboard_allowed=False,
        contract_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_feature_input_contract_safety(contract: FeatureInputContract) -> list[str]:
    errors = []
    if contract.network_allowed:
        errors.append("network_allowed must be false")
    if contract.paid_api_allowed:
        errors.append("paid_api_allowed must be false")
    if contract.scraping_allowed:
        errors.append("scraping_allowed must be false")
    if contract.html_parsing_allowed:
        errors.append("html_parsing_allowed must be false")
    if contract.broker_allowed:
        errors.append("broker_allowed must be false")
    if contract.order_allowed:
        errors.append("order_allowed must be false")
    if contract.paper_mutation_allowed:
        errors.append("paper_mutation_allowed must be false")
    if contract.telegram_real_send_allowed:
        errors.append("telegram_real_send_allowed must be false")
    if contract.dashboard_allowed:
        errors.append("dashboard_allowed must be false")
    return errors

def validate_ohlcv_feature_input_records(records: list[dict[str, Any]]) -> list[str]:
    contract = build_feature_input_contract()
    errors = []
    for idx, rec in enumerate(records):
        for col in contract.required_ohlcv_columns:
            if col not in rec:
                errors.append(f"Record {idx} missing required column: {col}")
    return errors

def validate_feature_metadata_inputs(payload: dict[str, Any]) -> list[str]:
    return []

def feature_input_contract_summary(contract: FeatureInputContract) -> dict[str, Any]:
    return {"valid": contract.contract_valid, "required": len(contract.required_ohlcv_columns)}

def feature_input_contract_to_text(contract: FeatureInputContract) -> str:
    return f"Feature Input Contract: {contract.contract_id}\nValid: {contract.contract_valid}"
