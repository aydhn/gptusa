from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import json
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import (
    ProviderRuntimeIngestionResult,
    create_provider_runtime_ingestion_id,
    ProviderCacheRiskFlag
)
from usa_signal_bot.core.exceptions import ProviderRuntimeIngestionError

def extract_provider_runtime_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_provider_runtime_adapter_specs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("adapter_spec_evaluations", [])

def provider_runtime_supports_phase108(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []
    if "context" not in payload:
        return False, ["No context found in provider runtime review."]
    ctx = payload["context"]

    if not ctx.get("provider_runtime_ready", False):
        return False, ["provider_runtime_ready is not true."]
    if not ctx.get("adapter_contracts_valid", False):
        return False, ["adapter_contracts_valid is not true."]
    if not ctx.get("cache_aware_dry_run_ready", False):
        return False, ["cache_aware_dry_run_ready is not true."]
    if not ctx.get("metadata_only", False):
        return False, ["metadata_only is not true."]
    if ctx.get("network_enabled_by_default", True):
        return False, ["network_enabled_by_default is true."]

    unsafe_keys = ["paid_api_enabled", "scraping_enabled", "html_parse_enabled",
                   "broker_execution_enabled", "order_creation_enabled",
                   "paper_state_mutation_enabled", "telegram_real_send_enabled", "dashboard_enabled"]
    for k in unsafe_keys:
        if ctx.get(k, False):
            return False, [f"{k} is true."]

    return True, []

def ingest_provider_runtime_review_payload(payload: dict[str, Any]) -> ProviderRuntimeIngestionResult:
    ctx = extract_provider_runtime_context(payload)
    if not ctx:
        return ProviderRuntimeIngestionResult(
            ingestion_id=create_provider_runtime_ingestion_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            source_path=None, source_review_id=None, source_context_id=None,
            available=False, provider_runtime_ready=False, adapter_contracts_valid=False,
            cache_aware_dry_run_ready=False, metadata_only=False,
            network_enabled_by_default=True, paid_api_enabled=True, scraping_enabled=True,
            html_parse_enabled=True, broker_execution_enabled=True, order_creation_enabled=True,
            paper_state_mutation_enabled=True, telegram_real_send_enabled=True, dashboard_enabled=True,
            valid_for_phase108=False,
            risk_flags=[ProviderCacheRiskFlag.PROVIDER_RUNTIME_MISSING],
            warnings=["No context available."], errors=["Invalid payload structure."], metadata={}
        )

    valid, validation_errors = provider_runtime_supports_phase108(payload)
    risk_flags = []
    if not valid:
        risk_flags.append(ProviderCacheRiskFlag.PROVIDER_RUNTIME_INVALID)

    return ProviderRuntimeIngestionResult(
        ingestion_id=create_provider_runtime_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=payload.get("source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=True,
        provider_runtime_ready=ctx.get("provider_runtime_ready", False),
        adapter_contracts_valid=ctx.get("adapter_contracts_valid", False),
        cache_aware_dry_run_ready=ctx.get("cache_aware_dry_run_ready", False),
        metadata_only=ctx.get("metadata_only", False),
        network_enabled_by_default=ctx.get("network_enabled_by_default", True),
        paid_api_enabled=ctx.get("paid_api_enabled", False),
        scraping_enabled=ctx.get("scraping_enabled", False),
        html_parse_enabled=ctx.get("html_parse_enabled", False),
        broker_execution_enabled=ctx.get("broker_execution_enabled", False),
        order_creation_enabled=ctx.get("order_creation_enabled", False),
        paper_state_mutation_enabled=ctx.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=ctx.get("telegram_real_send_enabled", False),
        dashboard_enabled=ctx.get("dashboard_enabled", False),
        valid_for_phase108=valid,
        risk_flags=risk_flags,
        warnings=validation_errors,
        errors=validation_errors,
        metadata={"ingested_from": "payload"}
    )

def ingest_latest_provider_runtime_review_from_store(data_root: Path) -> ProviderRuntimeIngestionResult:
    # Phase 107 reviews are in data/provider_runtime/reviews
    reviews_dir = data_root / "provider_runtime" / "reviews"
    if not reviews_dir.exists():
        return ingest_provider_runtime_review_payload({})

    reviews = list(reviews_dir.glob("provider_runtime_full_review_*.json"))
    if not reviews:
        return ingest_provider_runtime_review_payload({})

    latest_review = max(reviews, key=lambda p: p.stat().st_mtime)
    with open(latest_review, 'r') as f:
        try:
            payload = json.load(f)
            payload["source_path"] = str(latest_review)
            return ingest_provider_runtime_review_payload(payload)
        except json.JSONDecodeError:
             return ingest_provider_runtime_review_payload({})

def provider_runtime_ingestion_to_text(result: ProviderRuntimeIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - Available: {result.available}, Valid for P108: {result.valid_for_phase108}"
