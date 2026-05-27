from typing import Any
from pathlib import Path
from datetime import datetime, timezone
import uuid

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorCompositionIngestionResult,
    FactorScoringRiskFlag,
    create_factor_composition_ingestion_id,
    validate_factor_composition_ingestion_result
)

def ingest_factor_composition_review_payload(payload: dict[str, Any]) -> FactorCompositionIngestionResult:
    ingestion_id = create_factor_composition_ingestion_id()
    created_at_utc = datetime.now(timezone.utc).isoformat()

    review_id = payload.get("review_id")
    context_id = payload.get("context", {}).get("context_id")

    feature_groups_ready = payload.get("feature_groups_ready", False)
    factor_candidates_ready = payload.get("factor_candidates_ready", False)
    selection_metadata_ready = payload.get("selection_metadata_ready", False)
    factor_readiness_gate_ready = payload.get("factor_readiness_gate_ready", False)
    ready_for_phase120 = payload.get("ready_for_phase120", False)

    activation_allowed = payload.get("activation_allowed", False)
    strategy_activation_allowed = payload.get("strategy_activation_allowed", False)
    active_paper_enabled = payload.get("active_paper_enabled", False)
    broker_execution_enabled = payload.get("broker_execution_enabled", False)
    order_creation_enabled = payload.get("order_creation_enabled", False)
    paper_state_mutation_enabled = payload.get("paper_state_mutation_enabled", False)
    telegram_real_send_enabled = payload.get("telegram_real_send_enabled", False)
    scraping_enabled = payload.get("scraping_enabled", False)
    html_parse_enabled = payload.get("html_parse_enabled", False)
    paid_api_enabled = payload.get("paid_api_enabled", False)
    dashboard_enabled = payload.get("dashboard_enabled", False)
    network_default_enabled = payload.get("network_default_enabled", False)

    produces_trade_signal = payload.get("produces_trade_signal", False)
    produces_order_decision = payload.get("produces_order_decision", False)
    produces_portfolio_weights = payload.get("produces_portfolio_weights", False)

    network_used = payload.get("network_used", False)
    paid_api_used = payload.get("paid_api_used", False)
    scraping_used = payload.get("scraping_used", False)
    html_parsing_used = payload.get("html_parsing_used", False)
    broker_used = payload.get("broker_used", False)
    order_created = payload.get("order_created", False)
    paper_state_mutated = payload.get("paper_state_mutated", False)
    telegram_real_sent = payload.get("telegram_real_sent", False)
    dashboard_started = payload.get("dashboard_started", False)

    risk_flags = []
    if not review_id:
        risk_flags.append(FactorScoringRiskFlag.FACTOR_COMPOSITION_REVIEW_MISSING)
    if not factor_readiness_gate_ready:
        risk_flags.append(FactorScoringRiskFlag.FACTOR_READINESS_GATE_FAILED)

    if activation_allowed or strategy_activation_allowed or active_paper_enabled:
        risk_flags.append(FactorScoringRiskFlag.PAPER_MUTATION_RISK)
    if broker_execution_enabled or order_creation_enabled or paper_state_mutation_enabled:
        risk_flags.append(FactorScoringRiskFlag.BROKER_RISK)
    if produces_trade_signal or produces_order_decision or produces_portfolio_weights:
        risk_flags.append(FactorScoringRiskFlag.TRADE_SIGNAL_COLUMN_RISK)

    ready_for_phase121 = (
        feature_groups_ready and
        factor_candidates_ready and
        selection_metadata_ready and
        factor_readiness_gate_ready and
        ready_for_phase120
    )

    result = FactorCompositionIngestionResult(
        ingestion_id=ingestion_id,
        created_at_utc=created_at_utc,
        source_path=None,
        source_review_id=review_id,
        source_context_id=context_id,
        available=bool(review_id),
        feature_groups_ready=feature_groups_ready,
        factor_candidates_ready=factor_candidates_ready,
        selection_metadata_ready=selection_metadata_ready,
        factor_readiness_gate_ready=factor_readiness_gate_ready,
        ready_for_phase121=ready_for_phase121,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=activation_allowed,
        strategy_activation_allowed=strategy_activation_allowed,
        active_paper_enabled=active_paper_enabled,
        broker_execution_enabled=broker_execution_enabled,
        order_creation_enabled=order_creation_enabled,
        paper_state_mutation_enabled=paper_state_mutation_enabled,
        telegram_real_send_enabled=telegram_real_send_enabled,
        scraping_enabled=scraping_enabled,
        html_parse_enabled=html_parse_enabled,
        paid_api_enabled=paid_api_enabled,
        dashboard_enabled=dashboard_enabled,
        network_default_enabled=network_default_enabled,
        produces_trade_signal=produces_trade_signal,
        produces_order_decision=produces_order_decision,
        produces_portfolio_weights=produces_portfolio_weights,
        network_used=network_used,
        paid_api_used=paid_api_used,
        scraping_used=scraping_used,
        html_parsing_used=html_parsing_used,
        broker_used=broker_used,
        order_created=order_created,
        paper_state_mutated=paper_state_mutated,
        telegram_real_sent=telegram_real_sent,
        dashboard_started=dashboard_started,
        valid_for_phase121=True,
        risk_flags=risk_flags,
        warnings=[],
        errors=[],
        metadata=payload
    )

    validate_factor_composition_ingestion_result(result)
    return result

def ingest_latest_factor_composition_review_from_store(data_root: Path) -> FactorCompositionIngestionResult:
    import json
    review_path = data_root / "feature_engine" / "factor_composition" / "reviews"
    if not review_path.exists():
        payload = {}
        result = ingest_factor_composition_review_payload(payload)
        result.source_path = None
        return result

    files = list(review_path.glob("*.json"))
    if not files:
        payload = {}
        result = ingest_factor_composition_review_payload(payload)
        result.source_path = None
        return result

    latest_file = max(files, key=lambda p: p.stat().st_mtime)
    with open(latest_file, "r") as f:
        payload = json.load(f)

    result = ingest_factor_composition_review_payload(payload)
    result.source_path = str(latest_file)
    return result

def extract_factor_composition_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_factor_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    context = payload.get("context", {})
    return context.get("factor_candidates", [])

def extract_factor_table_input_paths(payload: dict[str, Any]) -> dict[str, str]:
    context = payload.get("context", {})
    return context.get("feature_table_paths", {})

def factor_composition_supports_phase121(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    result = ingest_factor_composition_review_payload(payload)
    return result.valid_for_phase121, result.errors

def factor_composition_ingestion_to_text(result: FactorCompositionIngestionResult) -> str:
    lines = [
        "--- Factor Composition Ingestion ---",
        f"Ingestion ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Ready for Phase121: {result.ready_for_phase121}",
        f"Valid for Phase121: {result.valid_for_phase121}"
    ]
    return "\n".join(lines)
