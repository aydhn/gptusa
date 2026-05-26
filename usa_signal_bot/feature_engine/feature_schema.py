import datetime
from typing import Any
from usa_signal_bot.core.enums import FeatureOutputKind, FeatureBlockedOutputKind
from usa_signal_bot.feature_engine.phase116_models import (
    FeatureOutputSchema, FeatureDefinition, FactorDefinition, create_feature_output_schema_id
)

def build_feature_output_schema(features: list[FeatureDefinition], factors: list[FactorDefinition]) -> FeatureOutputSchema:
    return FeatureOutputSchema(
        schema_id=create_feature_output_schema_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        feature_definitions=features,
        factor_definitions=factors,
        allowed_output_kinds=[
            FeatureOutputKind.FEATURE_METADATA,
            FeatureOutputKind.FEATURE_SCHEMA,
            FeatureOutputKind.FEATURE_PLAN,
            FeatureOutputKind.FEATURE_VALUE_PLACEHOLDER,
            FeatureOutputKind.FACTOR_METADATA,
            FeatureOutputKind.LINEAGE_METADATA,
            FeatureOutputKind.VALIDATION_REPORT
        ],
        blocked_output_kinds=[
            FeatureBlockedOutputKind.TRADE_SIGNAL,
            FeatureBlockedOutputKind.ORDER_DECISION,
            FeatureBlockedOutputKind.BROKER_INSTRUCTION,
            FeatureBlockedOutputKind.PAPER_STATE_MUTATION,
            FeatureBlockedOutputKind.LIVE_ORDER,
            FeatureBlockedOutputKind.DEMO_ORDER,
            FeatureBlockedOutputKind.TELEGRAM_REAL_SEND,
            FeatureBlockedOutputKind.DASHBOARD_PAYLOAD,
            FeatureBlockedOutputKind.SCRAPED_HTML,
            FeatureBlockedOutputKind.PAID_API_PAYLOAD
        ],
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
        schema_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_feature_output_schema_safety(schema: FeatureOutputSchema) -> list[str]:
    errors = []
    if not schema.trade_signal_blocked:
        errors.append("trade_signal_blocked must be true")
    if not schema.order_decision_blocked:
        errors.append("order_decision_blocked must be true")
    if not schema.broker_blocked:
        errors.append("broker_blocked must be true")
    if not schema.paper_mutation_blocked:
        errors.append("paper_mutation_blocked must be true")
    if not schema.telegram_real_send_blocked:
        errors.append("telegram_real_send_blocked must be true")
    if not schema.scraping_blocked:
        errors.append("scraping_blocked must be true")
    if not schema.html_parsing_blocked:
        errors.append("html_parsing_blocked must be true")
    if not schema.paid_api_blocked:
        errors.append("paid_api_blocked must be true")
    if not schema.dashboard_blocked:
        errors.append("dashboard_blocked must be true")
    if not schema.network_default_enabled_blocked:
        errors.append("network_default_enabled_blocked must be true")
    return errors

def _has_unsafe_language(name: str) -> bool:
    s = name.lower()
    unsafe = ["buy", "sell", "signal", "order", "broker", "live", "paper_order", "trade"]
    return any(u in s for u in unsafe)

def validate_feature_column_names(features: list[FeatureDefinition]) -> list[str]:
    errors = []
    for f in features:
        if _has_unsafe_language(f.name) or _has_unsafe_language(f.output_column):
            errors.append(f"Unsafe feature column name: {f.name} / {f.output_column}")
    return errors

def validate_factor_column_names(factors: list[FactorDefinition]) -> list[str]:
    errors = []
    for f in factors:
        if _has_unsafe_language(f.name) or _has_unsafe_language(f.output_column):
            errors.append(f"Unsafe factor column name: {f.name} / {f.output_column}")
    return errors

def feature_output_schema_summary(schema: FeatureOutputSchema) -> dict[str, Any]:
    return {"valid": schema.schema_valid, "features": len(schema.feature_definitions), "factors": len(schema.factor_definitions)}

def feature_output_schema_to_text(schema: FeatureOutputSchema, limit: int = 200) -> str:
    return f"Schema ID: {schema.schema_id}\nFeatures: {len(schema.feature_definitions)}\nFactors: {len(schema.factor_definitions)}"
