import pytest
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderQualityContext, ProviderCacheIngestionResult, DataQualityScoreComponent, ProviderQualityFullReview,
)
from usa_signal_bot.core.enums import DataQualityGrade, DataQualityComponent, ProviderQualityStatus, ProviderQualityDecision, ProviderQualityReportType
from usa_signal_bot.provider_quality.provider_quality_reporting import (
    data_quality_score_component_to_text,
    provider_quality_context_to_text,
    provider_quality_full_review_to_text,
    provider_quality_store_summary_to_text,
    provider_quality_limitations_text
)

def test_data_quality_score_component_to_text():
    comp = DataQualityScoreComponent(
        component_id="comp_1",
        created_at_utc="2023-01-01T00:00:00Z",
        provider_name="TestProvider",
        symbol="AAPL",
        component=DataQualityComponent.COMPLETENESS,
        raw_value=1.0,
        score=95.5,
        weight=1.0,
        weighted_score=95.5,
        grade=DataQualityGrade.EXCELLENT,
        explanation="Test explanation"
    )
    result = data_quality_score_component_to_text(comp)
    assert result == "COMPLETENESS: 95.5 (EXCELLENT) - Test explanation"

def test_provider_quality_context_to_text():
    ingestion = ProviderCacheIngestionResult(
        ingestion_id="ingest_1",
        created_at_utc="2023-01-01T00:00:00Z",
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        provider_cache_ready=True,
        stale_fresh_policy_valid=True,
        fallback_dry_run_ready=True,
        source_comparison_ready=True,
        metadata_only=True,
        network_enabled_by_default=False,
        paid_api_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        dashboard_enabled=False,
        cache_only_default=True,
        valid_for_phase109=True
    )

    ctx = ProviderQualityContext(
        context_id="ctx_1",
        created_at_utc="2023-01-01T00:00:00Z",
        status=ProviderQualityStatus.VALIDATED,
        decision=ProviderQualityDecision.APPROVED,
        source_provider_cache_review_id=None,
        ingestion=ingestion,
        data_quality_scores=[],
        trust_profiles=[],
        selection_scores=[],
        rankings=[],
        provider_quality_ready=True,
        source_trust_ready=True,
        provider_selection_scoring_ready=True,
        metadata_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        errors=["Err1"],
        warnings=["Warn1"]
    )
    result = provider_quality_context_to_text(ctx)
    assert "Provider Quality Context: ctx_1" in result
    assert "Status: VALIDATED" in result
    assert "Ingestion: ingest_1" in result
    assert "Errors: ['Err1']" in result
    assert "Warnings: ['Warn1']" in result

    # Test with no errors or warnings
    ctx.errors = []
    ctx.warnings = []
    result = provider_quality_context_to_text(ctx)
    assert "Errors" not in result
    assert "Warnings" not in result

def test_provider_quality_full_review_to_text():
    ingestion = ProviderCacheIngestionResult(
        ingestion_id="ingest_1",
        created_at_utc="2023-01-01T00:00:00Z",
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        provider_cache_ready=True,
        stale_fresh_policy_valid=True,
        fallback_dry_run_ready=True,
        source_comparison_ready=True,
        metadata_only=True,
        network_enabled_by_default=False,
        paid_api_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        dashboard_enabled=False,
        cache_only_default=True,
        valid_for_phase109=True
    )

    ctx = ProviderQualityContext(
        context_id="ctx_1",
        created_at_utc="2023-01-01T00:00:00Z",
        status=ProviderQualityStatus.VALIDATED,
        decision=ProviderQualityDecision.APPROVED,
        source_provider_cache_review_id=None,
        ingestion=ingestion,
        data_quality_scores=[],
        trust_profiles=[],
        selection_scores=[],
        rankings=[],
        provider_quality_ready=True,
        source_trust_ready=True,
        provider_selection_scoring_ready=True,
        metadata_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False
    )

    rev = ProviderQualityFullReview(
        review_id="rev_1",
        created_at_utc="2023-01-01T00:00:00Z",
        report_type=ProviderQualityReportType.FULL,
        ingestion=ingestion,
        context=ctx,
        data_quality_scores=[],
        trust_profiles=[],
        selection_scores=[],
        rankings=[],
        warnings=["Warn1"],
        errors=["Err1"]
    )
    result = provider_quality_full_review_to_text(rev)
    assert "Provider Quality Full Review: rev_1" in result
    assert "Context ID: ctx_1" in result
    assert "Report Type: FULL" in result
    assert "Warnings: 1" in result
    assert "Errors: 1" in result

def test_provider_quality_store_summary_to_text():
    summary = {
        'contexts_count': 10,
        'reviews_count': 5,
        'data_quality_scores_count': 20,
        'source_trust_profiles_count': 15,
        'provider_selection_scores_count': 30,
        'provider_rankings_count': 25
    }
    result = provider_quality_store_summary_to_text(summary)
    assert "Contexts: 10" in result
    assert "Reviews: 5" in result
    assert "Data Quality Scores: 20" in result
    assert "Source Trust Profiles: 15" in result
    assert "Selection Scores: 30" in result
    assert "Rankings: 25" in result

    # Test missing keys
    empty_summary = {}
    result = provider_quality_store_summary_to_text(empty_summary)
    assert "Contexts: 0" in result
    assert "Reviews: 0" in result

def test_provider_quality_limitations_text():
    result = provider_quality_limitations_text()
    assert "Phase 109 Limitations" in result
    assert "Research Data Selection" in result
