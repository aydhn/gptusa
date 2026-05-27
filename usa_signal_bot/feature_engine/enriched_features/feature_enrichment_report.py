from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import FeatureEnrichmentStatus, FeatureEnrichmentDecision, FeatureEnrichmentReportType
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureEnrichmentContext,
    FeatureEnrichmentFullReview,
    AdvancedFeatureIngestionResult,
    create_feature_enrichment_context_id,
    create_feature_enrichment_full_review_id,
    create_advanced_feature_ingestion_id
)

def build_feature_enrichment_context() -> FeatureEnrichmentContext:
    ingestion = AdvancedFeatureIngestionResult(
        ingestion_id=create_advanced_feature_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        available=True,
        advanced_features_ready=True,
        cross_sectional_features_ready=True,
        multi_symbol_feature_table_ready=True,
        ready_for_phase119=True,
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
        valid_for_phase119=True
    )

    return FeatureEnrichmentContext(
        context_id=create_feature_enrichment_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=FeatureEnrichmentStatus.CREATED,
        decision=FeatureEnrichmentDecision.ENRICH_FEATURES,
        ingestion=ingestion,
        event_enrichment_ready=True,
        quality_enrichment_ready=True,
        calendar_enrichment_ready=True,
        interactions_ready=True,
        enriched_feature_table_ready=True,
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
    )

def build_feature_enrichment_full_review() -> FeatureEnrichmentFullReview:
    ctx = build_feature_enrichment_context()
    return FeatureEnrichmentFullReview(
        review_id=create_feature_enrichment_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=FeatureEnrichmentReportType.FULL_PHASE119_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx
    )

def feature_enrichment_full_review_summary(review: FeatureEnrichmentFullReview) -> dict[str, Any]:
    return {"review_id": review.review_id}

def feature_enrichment_limitations_text() -> str:
    return "Phase 119 is not activation, no trade signals, no broker execution."

def feature_enrichment_full_review_to_text(review: FeatureEnrichmentFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id} created."
