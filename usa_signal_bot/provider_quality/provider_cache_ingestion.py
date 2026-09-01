import datetime
from typing import Dict, Any, Optional, Tuple, List

from usa_signal_bot.provider_quality.phase109_models import ProviderCacheIngestionResult, create_provider_cache_ingestion_id

def provider_cache_supports_phase109(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []

    context = payload.get("context", {})
    if not context.get("provider_cache_ready"):
        warnings.append("provider_cache_ready is false")
    if not context.get("metadata_only", True):
        warnings.append("metadata_only is false")

    return len(warnings) == 0, warnings

def extract_provider_cache_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_source_comparisons(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("source_comparisons", [])

def extract_confidence_hints(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("confidence_hints", [])

def ingest_provider_cache_review_payload(payload: Dict[str, Any], source_path: Optional[str] = None) -> ProviderCacheIngestionResult:
    context = extract_provider_cache_context(payload)
    if not context:
        return ProviderCacheIngestionResult(
            ingestion_id=create_provider_cache_ingestion_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            source_path=source_path,
            source_review_id=payload.get("review_id"),
            source_context_id=None,
            available=False,
            provider_cache_ready=False,
            stale_fresh_policy_valid=False,
            fallback_dry_run_ready=False,
            source_comparison_ready=False,
            metadata_only=True,
            cache_only_default=True,
            network_enabled_by_default=False,
            paid_api_enabled=False,
            scraping_enabled=False,
            html_parse_enabled=False,
            broker_execution_enabled=False,
            order_creation_enabled=False,
            paper_state_mutation_enabled=False,
            telegram_real_send_enabled=False,
            dashboard_enabled=False,
            valid_for_phase109=False,
            errors=["No provider cache context found in payload"]
        )

    valid, warnings = provider_cache_supports_phase109(payload)

    return ProviderCacheIngestionResult(
        ingestion_id=create_provider_cache_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        source_path=source_path,
        source_review_id=payload.get("review_id"),
        source_context_id=context.get("context_id"),
        available=True,
        provider_cache_ready=context.get("provider_cache_ready", False),
        stale_fresh_policy_valid=context.get("stale_fresh_policy_valid", False),
        fallback_dry_run_ready=context.get("fallback_dry_run_ready", False),
        source_comparison_ready=context.get("source_comparison_ready", False),
        metadata_only=context.get("metadata_only", True),
        cache_only_default=context.get("cache_only_default", True),
        network_enabled_by_default=context.get("network_enabled_by_default", False),
        paid_api_enabled=context.get("paid_api_enabled", False),
        scraping_enabled=context.get("scraping_enabled", False),
        html_parse_enabled=context.get("html_parse_enabled", False),
        broker_execution_enabled=context.get("broker_execution_enabled", False),
        order_creation_enabled=context.get("order_creation_enabled", False),
        paper_state_mutation_enabled=context.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=context.get("telegram_real_send_enabled", False),
        dashboard_enabled=context.get("dashboard_enabled", False),
        valid_for_phase109=valid,
        warnings=warnings
    )

def ingest_latest_provider_cache_review_from_store(data_root: Any) -> ProviderCacheIngestionResult:
    # We will implement the file read in the store module and pass the dict here
    pass

def provider_cache_ingestion_to_text(result: ProviderCacheIngestionResult) -> str:
    return f"Ingestion ID: {result.ingestion_id} | Valid: {result.valid_for_phase109} | Cache Ready: {result.provider_cache_ready}"
