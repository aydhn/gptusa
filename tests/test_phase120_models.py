import pytest
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureEnrichmentIngestionResult,
    validate_feature_enrichment_ingestion_result
)

def test_feature_enrichment_ingestion_result_validation():
    # Test valid
    res = FeatureEnrichmentIngestionResult(
        ingestion_id="test", created_at_utc="test", source_path=None, source_review_id=None, source_context_id=None,
        available=True, event_enrichment_ready=True, quality_enrichment_ready=True, calendar_enrichment_ready=True,
        interactions_ready=True, enriched_feature_table_ready=True, ready_for_phase120=True,
        metadata_only=True, research_data_only=True, activation_allowed=False, active_paper_enabled=False,
        broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False, scraping_enabled=False, html_parse_enabled=False,
        paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False,
        produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False,
        network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
        broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False,
        dashboard_started=False, valid_for_phase120=True
    )
    validate_feature_enrichment_ingestion_result(res)
    assert len(res.errors) == 0

    # Test invalid activation
    res.activation_allowed = True
    validate_feature_enrichment_ingestion_result(res)
    assert "activation_allowed must be false" in res.errors
