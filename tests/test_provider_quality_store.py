import pytest
from pathlib import Path
import json


from usa_signal_bot.provider_quality.phase109_models import (
    ProviderQualityContext,
    ProviderQualityFullReview,
    ProviderDataQualityScore,
    SourceTrustProfile,
    ProviderSelectionScore,
    ProviderRanking,
    ProviderCacheIngestionResult
)

from usa_signal_bot.provider_quality.provider_quality_store import (
    provider_quality_store_dir,
    provider_quality_contexts_dir,
    provider_quality_reviews_dir,
    data_quality_scores_dir,
    source_trust_profiles_dir,
    provider_selection_scores_dir,
    provider_rankings_dir,
    write_provider_quality_context_json,
    write_provider_quality_full_review_json,
    write_data_quality_scores_jsonl,
    write_source_trust_profiles_jsonl,
    write_provider_selection_scores_jsonl,
    write_provider_rankings_jsonl,
    read_provider_quality_full_review_json,
    list_provider_quality_reviews,
    get_latest_provider_quality_review,
    provider_quality_store_summary
)

def test_directories(tmp_path):
    assert provider_quality_store_dir(tmp_path) == tmp_path / "provider_quality"
    assert provider_quality_contexts_dir(tmp_path) == tmp_path / "provider_quality" / "contexts"
    assert provider_quality_reviews_dir(tmp_path) == tmp_path / "provider_quality" / "reviews"
    assert data_quality_scores_dir(tmp_path) == tmp_path / "provider_quality" / "data_quality_scores"
    assert source_trust_profiles_dir(tmp_path) == tmp_path / "provider_quality" / "source_trust_profiles"
    assert provider_selection_scores_dir(tmp_path) == tmp_path / "provider_quality" / "provider_selection_scores"
    assert provider_rankings_dir(tmp_path) == tmp_path / "provider_quality" / "provider_rankings"
def test_store_operations(tmp_path):
    # Dummy instances for models
    dqs = ProviderDataQualityScore(
        score_id="dqs_1",
        created_at_utc="2024-01-01T00:00:00Z",
        provider_name="test_provider",
        symbol="AAPL",
        capability="test_cap",
        components=[],
        total_score=95.0,
        grade="A",
        usable_for_research=True,
        use_with_warning=False,
        blocked=False,
        explanation="test"
    )

    stp = SourceTrustProfile(
        profile_id="stp_1",
        created_at_utc="2024-01-01T00:00:00Z",
        provider_name="test_provider",
        provider_kind="mock",
        historical_score=100.0,
        schema_reliability_score=100.0,
        freshness_reliability_score=100.0,
        agreement_reliability_score=100.0,
        cache_reliability_score=100.0,
        safety_reliability_score=100.0,
        trust_score=100.0,
        trust_level="HIGH",
        default_use_case="all"
    )

    pss = ProviderSelectionScore(
        selection_score_id="pss_1",
        created_at_utc="2024-01-01T00:00:00Z",
        provider_name="test_provider",
        symbol="AAPL",
        capability="pricing",
        data_quality_score_id="dqs_1",
        trust_profile_id="stp_1",
        quality_score=95.0,
        trust_score=100.0,
        freshness_score=90.0,
        safety_score=99.0,
        availability_score=99.9,
        final_selection_score=96.0,
        status="ACTIVE",
        decision="PASS",
        rank=1,
        selectable_for_research=True,
        use_as_fallback=False,
        blocked=False,
        explanation="test"
    )

    pr = ProviderRanking(
        ranking_id="pr_1",
        created_at_utc="2024-01-01T00:00:00Z",
        symbol="AAPL",
        capability="pricing",
        scores=[pss],
        ranked_provider_names=["test_provider"],
        preferred_provider="test_provider",
        fallback_providers=[],
        blocked_providers=[],
        ranking_valid=True,
        ranking_is_research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False
    )

    ingestion = ProviderCacheIngestionResult(
        ingestion_id="test_ingest",
        created_at_utc="2024-01-01T00:00:00Z",
        source_path="test",
        source_review_id="test",
        source_context_id="test",
        available=True,
        provider_cache_ready=True,
        stale_fresh_policy_valid=True,
        fallback_dry_run_ready=True,
        source_comparison_ready=True,
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
        valid_for_phase109=True
    )

    pqc = ProviderQualityContext(
        context_id="pqc_1",
        created_at_utc="2024-01-01T00:00:00Z",
        status="OK",
        decision="PASS",
        source_provider_cache_review_id="test_ingest",
        ingestion=ingestion,
        data_quality_scores=[dqs],
        trust_profiles=[stp],
        selection_scores=[pss],
        rankings=[pr],
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

    pqfr = ProviderQualityFullReview(
        review_id="pqfr_1",
        created_at_utc="2024-01-01T00:00:00Z",
        report_type="FULL",
        ingestion=ingestion,
        context=pqc,
        data_quality_scores=[dqs],
        trust_profiles=[stp],
        selection_scores=[pss],
        rankings=[pr]
    )

    # Write files
    context_path = provider_quality_contexts_dir(tmp_path) / "pqc_1.json"
    write_provider_quality_context_json(context_path, pqc)
    assert context_path.exists()

    review_path = provider_quality_reviews_dir(tmp_path) / "pqfr_1.json"
    write_provider_quality_full_review_json(review_path, pqfr)
    assert review_path.exists()

    # Assert contents of the JSON write
    review_read = read_provider_quality_full_review_json(review_path)
    assert review_read["review_id"] == "pqfr_1"

    dqs_path = data_quality_scores_dir(tmp_path) / "dqs.jsonl"
    write_data_quality_scores_jsonl(dqs_path, [dqs])
    assert dqs_path.exists()

    stp_path = source_trust_profiles_dir(tmp_path) / "stp.jsonl"
    write_source_trust_profiles_jsonl(stp_path, [stp])
    assert stp_path.exists()

    pss_path = provider_selection_scores_dir(tmp_path) / "pss.jsonl"
    write_provider_selection_scores_jsonl(pss_path, [pss])
    assert pss_path.exists()

    pr_path = provider_rankings_dir(tmp_path) / "pr.jsonl"
    write_provider_rankings_jsonl(pr_path, [pr])
    assert pr_path.exists()

    # List reviews and latest review
    reviews = list_provider_quality_reviews(tmp_path)
    assert len(reviews) == 1
    assert reviews[0].name == "pqfr_1.json"

    latest = get_latest_provider_quality_review(tmp_path)
    assert latest.name == "pqfr_1.json"

    # Empty test for latest review
    import shutil
    shutil.rmtree(provider_quality_reviews_dir(tmp_path))
    latest_none = get_latest_provider_quality_review(tmp_path)
    assert latest_none is None

    # Summary
    # Contexts count = 1, Data quality scores = 1, Source trust profiles = 1, Provider selection scores = 1, Provider rankings = 1
    summary = provider_quality_store_summary(tmp_path)
    assert summary["contexts_count"] == 1
    assert summary["reviews_count"] == 0 # we just deleted it
    assert summary["data_quality_scores_count"] == 1
    assert summary["source_trust_profiles_count"] == 1
    assert summary["provider_selection_scores_count"] == 1
    assert summary["provider_rankings_count"] == 1
