from typing import Any
from pathlib import Path
import json

from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureEnrichmentIngestionResult,
    create_feature_enrichment_ingestion_id,
    validate_feature_enrichment_ingestion_result,
    _now_str
)

def extract_feature_enrichment_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_enriched_feature_table_paths(payload: dict[str, Any]) -> dict[str, str]:
    output_paths = payload.get("output_paths", {})
    tables = {}
    for k, v in output_paths.items():
        if k.startswith("enriched_feature_table_"):
            symbol = k.replace("enriched_feature_table_", "")
            tables[symbol] = v
    return tables

def feature_enrichment_supports_phase120(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []

    context = extract_feature_enrichment_context(payload)
    if not context:
        return False, ["Missing context in feature enrichment payload"]

    if not context.get("event_enrichment_ready", False): return False, ["event_enrichment_ready is false"]
    if not context.get("quality_enrichment_ready", False): return False, ["quality_enrichment_ready is false"]
    if not context.get("calendar_enrichment_ready", False): return False, ["calendar_enrichment_ready is false"]
    if not context.get("interactions_ready", False): return False, ["interactions_ready is false"]
    if not context.get("enriched_feature_table_ready", False): return False, ["enriched_feature_table_ready is false"]
    if not context.get("ready_for_phase119", False): return False, ["ready_for_phase119 is false"]
    if not context.get("research_data_only", False): return False, ["research_data_only is false"]

    for field in [
        "activation_allowed", "active_paper_enabled", "broker_execution_enabled",
        "order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
        "scraping_enabled", "html_parse_enabled", "paid_api_enabled", "dashboard_enabled",
        "network_default_enabled", "produces_trade_signal", "produces_order_decision",
        "produces_portfolio_weights"
    ]:
        if context.get(field, False):
            return False, [f"{field} is true"]

    return True, warnings

def ingest_feature_enrichment_review_payload(payload: dict[str, Any]) -> FeatureEnrichmentIngestionResult:
    result = FeatureEnrichmentIngestionResult(
        ingestion_id=create_feature_enrichment_ingestion_id(),
        created_at_utc=_now_str(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context", {}).get("context_id"),
        available=True,
        event_enrichment_ready=payload.get("context", {}).get("event_enrichment_ready", False),
        quality_enrichment_ready=payload.get("context", {}).get("quality_enrichment_ready", False),
        calendar_enrichment_ready=payload.get("context", {}).get("calendar_enrichment_ready", False),
        interactions_ready=payload.get("context", {}).get("interactions_ready", False),
        enriched_feature_table_ready=payload.get("context", {}).get("enriched_feature_table_ready", False),
        ready_for_phase120=True,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase120=False
    )

    is_valid, warnings = feature_enrichment_supports_phase120(payload)
    if not is_valid:
        result.valid_for_phase120 = False
        result.errors.extend(warnings)
        result.ready_for_phase120 = False
    else:
        result.valid_for_phase120 = True

    validate_feature_enrichment_ingestion_result(result)
    return result

def ingest_latest_feature_enrichment_review_from_store(data_root: Path) -> FeatureEnrichmentIngestionResult:
    # We will assume a mock path for the latest feature enrichment for this phase.
    # Usually this would parse directories to find the latest valid json.
    # Implementing a stub that raises exception if not found, since phase 119 storage is abstracted.
    import glob
    import os
    reviews_dir = data_root / "feature_engine" / "enriched_features" / "reviews"
    if not reviews_dir.exists():
        raise FileNotFoundError(f"Reviews dir not found: {reviews_dir}")

    files = glob.glob(os.path.join(reviews_dir, "*.json"))
    if not files:
        raise FileNotFoundError(f"No feature enrichment reviews found in {reviews_dir}")

    latest_file = max(files, key=os.path.getctime)
    with open(latest_file, 'r') as f:
        payload = json.load(f)

    result = ingest_feature_enrichment_review_payload(payload)
    result.source_path = str(latest_file)
    return result

def feature_enrichment_ingestion_to_text(result: FeatureEnrichmentIngestionResult) -> str:
    lines = [
        f"Feature Enrichment Ingestion: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Valid for Phase 120: {result.valid_for_phase120}",
        f"Ready for Phase 120: {result.ready_for_phase120}"
    ]
    if result.errors:
        lines.append("Errors:")
        for err in result.errors:
            lines.append(f"  - {err}")
    return "\n".join(lines)
