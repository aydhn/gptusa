from pathlib import Path
from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import FeatureEnrichmentRiskFlag
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    AdvancedFeatureIngestionResult,
    create_advanced_feature_ingestion_id
)

def ingest_advanced_feature_review_payload(payload: dict[str, Any]) -> AdvancedFeatureIngestionResult:
    result = AdvancedFeatureIngestionResult(
        ingestion_id=create_advanced_feature_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        available=True,
        advanced_features_ready=payload.get("advanced_features_ready", False),
        cross_sectional_features_ready=payload.get("cross_sectional_features_ready", False),
        multi_symbol_feature_table_ready=payload.get("multi_symbol_feature_table_ready", False),
        ready_for_phase119=payload.get("ready_for_phase119", False),
        metadata_only=payload.get("metadata_only", True),
        research_data_only=payload.get("research_data_only", True),
        activation_allowed=payload.get("activation_allowed", True),
        active_paper_enabled=payload.get("active_paper_enabled", True),
        broker_execution_enabled=payload.get("broker_execution_enabled", True),
        order_creation_enabled=payload.get("order_creation_enabled", True),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", True),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", True),
        scraping_enabled=payload.get("scraping_enabled", True),
        html_parse_enabled=payload.get("html_parse_enabled", True),
        paid_api_enabled=payload.get("paid_api_enabled", True),
        dashboard_enabled=payload.get("dashboard_enabled", True),
        network_default_enabled=payload.get("network_default_enabled", True),
        produces_trade_signal=payload.get("produces_trade_signal", True),
        produces_order_decision=payload.get("produces_order_decision", True),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", True),
        network_used=payload.get("network_used", True),
        paid_api_used=payload.get("paid_api_used", True),
        scraping_used=payload.get("scraping_used", True),
        html_parsing_used=payload.get("html_parsing_used", True),
        broker_used=payload.get("broker_used", True),
        order_created=payload.get("order_created", True),
        paper_state_mutated=payload.get("paper_state_mutated", True),
        telegram_real_sent=payload.get("telegram_real_sent", True),
        dashboard_started=payload.get("dashboard_started", True),
        valid_for_phase119=True
    )

    # Check flags
    if not result.advanced_features_ready:
        result.valid_for_phase119 = False
        result.errors.append("advanced_features_ready is false")
    if not result.cross_sectional_features_ready:
        result.valid_for_phase119 = False
        result.errors.append("cross_sectional_features_ready is false")
    if not result.multi_symbol_feature_table_ready:
        result.valid_for_phase119 = False
        result.errors.append("multi_symbol_feature_table_ready is false")
    if not result.ready_for_phase119:
        result.valid_for_phase119 = False
        result.errors.append("ready_for_phase119 is false")
    if not result.research_data_only:
        result.valid_for_phase119 = False
        result.errors.append("research_data_only is false")

    unsafe_flags = [
        "activation_allowed", "active_paper_enabled", "broker_execution_enabled",
        "order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
        "scraping_enabled", "html_parse_enabled", "paid_api_enabled", "dashboard_enabled",
        "network_default_enabled", "produces_trade_signal", "produces_order_decision",
        "produces_portfolio_weights", "network_used", "paid_api_used", "scraping_used",
        "html_parsing_used", "broker_used", "order_created", "paper_state_mutated",
        "telegram_real_sent", "dashboard_started"
    ]
    for flag in unsafe_flags:
        if getattr(result, flag):
            result.valid_for_phase119 = False
            result.errors.append(f"{flag} must be false")

    if not result.valid_for_phase119:
        result.risk_flags.append(FeatureEnrichmentRiskFlag.ADVANCED_FEATURE_REVIEW_INVALID)

    return result

def ingest_latest_advanced_feature_review_from_store(data_root: Path) -> AdvancedFeatureIngestionResult:
    return ingest_advanced_feature_review_payload({})

def extract_advanced_feature_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_advanced_feature_table_paths(payload: dict[str, Any]) -> dict[str, str]:
    return payload.get("output_paths", {})

def advanced_feature_supports_phase119(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    result = ingest_advanced_feature_review_payload(payload)
    return result.valid_for_phase119, result.errors

def advanced_feature_ingestion_to_text(result: AdvancedFeatureIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - valid: {result.valid_for_phase119}"
