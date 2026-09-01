import pytest
import datetime
from typing import List
from unittest.mock import patch, MagicMock
from usa_signal_bot.core.enums import ProviderQualityStatus, ProviderQualityDecision
from usa_signal_bot.provider_quality.phase109_models import ProviderCacheIngestionResult, ProviderDataQualityScore
from usa_signal_bot.provider_quality.provider_quality_report import build_provider_quality_context

@patch('usa_signal_bot.provider_quality.provider_quality_report.datetime')
def test_build_provider_quality_context_happy_path(mock_datetime):
    mock_datetime.datetime.utcnow.return_value = datetime.datetime(2023, 1, 1)
    ingest = ProviderCacheIngestionResult(ingestion_id='1', created_at_utc='2023', source_path=None, source_review_id='review1', source_context_id=None, available=True, provider_cache_ready=True, stale_fresh_policy_valid=True, fallback_dry_run_ready=True, source_comparison_ready=True, metadata_only=True, cache_only_default=False, network_enabled_by_default=False, paid_api_enabled=False, scraping_enabled=False, html_parse_enabled=False, broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False, dashboard_enabled=False, valid_for_phase109=True, warnings=[], errors=[], risk_flags=[])
    context = build_provider_quality_context(ingestion=ingest)
    assert context.status == ProviderQualityStatus.VALIDATED
    assert context.decision == ProviderQualityDecision.RANK_PROVIDERS

def test_build_provider_quality_context_with_ingestion_error():
    ingest = ProviderCacheIngestionResult(ingestion_id='1', created_at_utc='2023', source_path=None, source_review_id='review1', source_context_id=None, available=True, provider_cache_ready=True, stale_fresh_policy_valid=True, fallback_dry_run_ready=True, source_comparison_ready=True, metadata_only=True, cache_only_default=False, network_enabled_by_default=False, paid_api_enabled=False, scraping_enabled=False, html_parse_enabled=False, broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False, dashboard_enabled=False, valid_for_phase109=True, warnings=[], errors=['Some error'], risk_flags=[])
    context = build_provider_quality_context(ingestion=ingest)
    assert context.status == ProviderQualityStatus.FAILED
    assert context.decision == ProviderQualityDecision.BLOCK
