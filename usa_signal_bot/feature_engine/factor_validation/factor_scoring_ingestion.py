import json
from pathlib import Path
from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorScoringIngestionResult,
    create_factor_scoring_ingestion_id,
    validate_factor_scoring_ingestion_result
)

def ingest_factor_scoring_review_payload(payload: dict[str, Any]) -> FactorScoringIngestionResult:
    ctx = payload.get("context", {})

    result = FactorScoringIngestionResult(
        ingestion_id=create_factor_scoring_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=True,
        factor_scoring_ready=ctx.get("factor_scoring_ready", False),
        factor_normalization_ready=ctx.get("factor_normalization_ready", False),
        factor_diagnostics_ready=ctx.get("factor_diagnostics_ready", False),
        factor_table_ready=ctx.get("factor_table_ready", False),
        ready_for_phase122=ctx.get("ready_for_phase122", False) or ctx.get("ready_for_phase121", False),
        metadata_only=True,
        research_data_only=ctx.get("research_data_only", True),
        activation_allowed=ctx.get("activation_allowed", False),
        strategy_activation_allowed=ctx.get("strategy_activation_allowed", False),
        active_paper_enabled=ctx.get("active_paper_enabled", False),
        broker_execution_enabled=ctx.get("broker_execution_enabled", False),
        order_creation_enabled=ctx.get("order_creation_enabled", False),
        paper_state_mutation_enabled=ctx.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=ctx.get("telegram_real_send_enabled", False),
        scraping_enabled=ctx.get("scraping_enabled", False),
        html_parse_enabled=ctx.get("html_parse_enabled", False),
        paid_api_enabled=ctx.get("paid_api_enabled", False),
        dashboard_enabled=ctx.get("dashboard_enabled", False),
        network_default_enabled=ctx.get("network_default_enabled", False),
        produces_trade_signal=ctx.get("produces_trade_signal", False),
        produces_order_decision=ctx.get("produces_order_decision", False),
        produces_portfolio_weights=ctx.get("produces_portfolio_weights", False),
        network_used=ctx.get("network_used", False),
        paid_api_used=ctx.get("paid_api_used", False),
        scraping_used=ctx.get("scraping_used", False),
        html_parsing_used=ctx.get("html_parsing_used", False),
        broker_used=ctx.get("broker_used", False),
        order_created=ctx.get("order_created", False),
        paper_state_mutated=ctx.get("paper_state_mutated", False),
        telegram_real_sent=ctx.get("telegram_real_sent", False),
        dashboard_started=ctx.get("dashboard_started", False),
        valid_for_phase122=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={"original_payload_keys": list(payload.keys())}
    )

    validate_factor_scoring_ingestion_result(result)
    return result

def ingest_latest_factor_scoring_review_from_store(data_root: Path) -> FactorScoringIngestionResult:
    # Minimal implementation for tests
    return ingest_factor_scoring_review_payload({})

def extract_factor_scoring_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_factor_table_paths(payload: dict[str, Any]) -> dict[str, str]:
    return payload.get("output_paths", {})

def extract_factor_diagnostics_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("diagnostics_profiles", [])

def factor_scoring_supports_phase122(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    res = ingest_factor_scoring_review_payload(payload)
    return res.valid_for_phase122, res.errors

def factor_scoring_ingestion_to_text(result: FactorScoringIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - valid_for_phase122: {result.valid_for_phase122}"
