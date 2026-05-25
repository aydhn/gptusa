from pathlib import Path
from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.provider_cache.phase108_models import (
    ProviderCacheFullReview,
    ProviderCacheContext,
    ProviderCacheStatus,
    ProviderCacheDecision,
    ProviderCacheReportType,
    create_provider_cache_context_id,
    create_provider_cache_full_review_id
)
from usa_signal_bot.provider_cache.provider_runtime_ingestion import ingest_latest_provider_runtime_review_from_store
from usa_signal_bot.provider_cache.cache_path_resolver import default_provider_cache_root
from usa_signal_bot.provider_cache.cache_index import build_provider_cache_index
from usa_signal_bot.provider_cache.stale_fresh_policy import build_default_stale_fresh_policy
from usa_signal_bot.provider_cache.stale_fresh_evaluator import evaluate_cache_index_stale_fresh
from usa_signal_bot.provider_cache.fallback_dry_run_plan import build_default_fallback_dry_run_plans
from usa_signal_bot.provider_cache.fallback_dry_run_engine import ProviderFallbackDryRunEngine
from usa_signal_bot.provider_cache.source_comparison import build_source_comparison_input, run_source_comparison
from usa_signal_bot.provider_cache.data_confidence_hints import build_confidence_hints_from_comparison
from usa_signal_bot.provider_cache.cache_safety_validator import collect_cache_risk_flags

def build_provider_cache_context(cache_root: Path | None = None) -> ProviderCacheContext:
    if not cache_root:
        # Default mock root
        cache_root = Path("data/market_data/cache")

    ingestion = ingest_latest_provider_runtime_review_from_store(cache_root.parent.parent)
    index = build_provider_cache_index(cache_root)
    policy = build_default_stale_fresh_policy()
    evals = evaluate_cache_index_stale_fresh(index, policy)

    fallback_plans = build_default_fallback_dry_run_plans()
    engine = ProviderFallbackDryRunEngine(index, policy)
    fallback_results = engine.run_batch(fallback_plans)

    source_comparisons = []
    hints = []

    # Just run comparison on AAPL if available in index, or dummy
    aapl_records = [r for r in index.records if r.symbol == "AAPL"]
    if aapl_records:
        comp_input = build_source_comparison_input("AAPL", aapl_records)
        comp_res = run_source_comparison(comp_input, cache_root)
        source_comparisons.append(comp_res)
        hints.extend(build_confidence_hints_from_comparison(comp_res))

    risk_flags = []
    if not ingestion.valid_for_phase108:
        risk_flags.append("PROVIDER_RUNTIME_INVALID")

    ctx = ProviderCacheContext(
        context_id=create_provider_cache_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=ProviderCacheStatus.VALIDATED if ingestion.valid_for_phase108 else ProviderCacheStatus.BLOCKED,
        decision=ProviderCacheDecision.REQUEST_MANUAL_REVIEW,
        source_provider_runtime_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        cache_index=index,
        stale_fresh_policy=policy,
        stale_fresh_evaluations=evals,
        fallback_plans=fallback_plans,
        fallback_results=fallback_results,
        source_comparisons=source_comparisons,
        confidence_hints=hints,
        provider_cache_ready=True,
        stale_fresh_policy_valid=True,
        fallback_dry_run_ready=True,
        source_comparison_ready=True,
        metadata_only=True,
        cache_only_default=True,
        network_enabled_by_default=False,
        paid_api_enabled=False, scraping_enabled=False, html_parse_enabled=False,
        broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False, dashboard_enabled=False,
        risk_flags=risk_flags, warnings=[], errors=[], metadata={}
    )
    # Add collected flags
    from usa_signal_bot.provider_cache.phase108_models import ProviderCacheRiskFlag
    collected = collect_cache_risk_flags(ctx)
    ctx.risk_flags = collected

    return ctx

def build_provider_cache_full_review(cache_root: Path | None = None) -> ProviderCacheFullReview:
    ctx = build_provider_cache_context(cache_root)
    return ProviderCacheFullReview(
        review_id=create_provider_cache_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=ProviderCacheReportType.FULL_PHASE108_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        cache_index=ctx.cache_index,
        stale_fresh_policy=ctx.stale_fresh_policy,
        fallback_results=ctx.fallback_results,
        source_comparisons=ctx.source_comparisons,
        confidence_hints=ctx.confidence_hints,
        output_paths={},
        warnings=ctx.warnings,
        errors=ctx.errors
    )

def provider_cache_full_review_summary(review: ProviderCacheFullReview) -> dict[str, Any]:
    return {"id": review.review_id, "status": review.context.status.value}

def provider_cache_limitations_text() -> str:
    return "Phase 108 is a data caching phase. It does NOT enable live trading, real network fetch, or real paper state mutation."

def provider_cache_full_review_to_text(review: ProviderCacheFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id} - P108: {review.context.status.value}"
