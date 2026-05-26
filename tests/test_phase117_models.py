from usa_signal_bot.feature_engine.core_indicators.phase117_models import (
    FeatureFoundationIngestionResult,
    create_feature_foundation_ingestion_id,
    validate_feature_foundation_ingestion_result
)

def test_feature_foundation_ingestion_result_valid():
    res = FeatureFoundationIngestionResult(
        ingestion_id=create_feature_foundation_ingestion_id(),
        created_at_utc="2023-01-01T00:00:00Z",
        source_path=None, source_review_id=None, source_context_id=None,
        available=True, feature_foundation_ready=True, indicator_registry_ready=True,
        feature_registry_ready=True, factor_registry_ready=True, input_contract_ready=True,
        output_schema_ready=True, ready_for_phase117=True, metadata_only=True,
        research_data_only=True, activation_allowed=False, active_paper_enabled=False,
        broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False, scraping_enabled=False, html_parse_enabled=False,
        paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False,
        produces_trade_signal=False, produces_order_decision=False, network_used=False,
        paid_api_used=False, scraping_used=False, html_parsing_used=False, broker_used=False,
        order_created=False, paper_state_mutated=False, telegram_real_sent=False,
        dashboard_started=False, valid_for_phase117=True
    )
    validate_feature_foundation_ingestion_result(res)
    assert not res.errors
