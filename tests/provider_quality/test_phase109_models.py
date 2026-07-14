import pytest
from unittest.mock import patch, MagicMock

import usa_signal_bot.provider_quality.phase109_models as models
from usa_signal_bot.core.exceptions import ProviderQualityValidationError

# -- ID Generation Tests --

def test_create_provider_cache_ingestion_id():
    id_val = models.create_provider_cache_ingestion_id()
    assert id_val.startswith("cache_ingest_")

def test_create_data_quality_component_id():
    id_val = models.create_data_quality_component_id()
    assert id_val.startswith("dq_comp_")

def test_create_provider_data_quality_score_id():
    id_val = models.create_provider_data_quality_score_id()
    assert id_val.startswith("pdqs_")

def test_create_source_trust_profile_id():
    id_val = models.create_source_trust_profile_id()
    assert id_val.startswith("trust_prof_")

def test_create_provider_selection_score_id():
    id_val = models.create_provider_selection_score_id()
    assert id_val.startswith("psel_score_")

def test_create_provider_ranking_id():
    id_val = models.create_provider_ranking_id()
    assert id_val.startswith("prank_")

def test_create_provider_quality_context_id():
    id_val = models.create_provider_quality_context_id()
    assert id_val.startswith("pq_ctx_")

def test_create_provider_quality_full_review_id():
    id_val = models.create_provider_quality_full_review_id()
    assert id_val.startswith("pq_review_")


# -- Validation Tests --

def test_validate_provider_cache_ingestion_result_valid():
    item = models.ProviderCacheIngestionResult(
        ingestion_id="test_id",
        created_at_utc="now",
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        provider_cache_ready=True,
        stale_fresh_policy_valid=True,
        fallback_dry_run_ready=True,
        source_comparison_ready=True,
        metadata_only=True,
        cache_only_default=False,
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
    # Should not raise exception
    models.validate_provider_cache_ingestion_result(item)

def test_validate_provider_cache_ingestion_result_invalid():
    item = models.ProviderCacheIngestionResult(
        ingestion_id="test_id",
        created_at_utc="now",
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        provider_cache_ready=False,  # Invalid
        stale_fresh_policy_valid=True,
        fallback_dry_run_ready=True,
        source_comparison_ready=True,
        metadata_only=True,
        cache_only_default=False,
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
    with pytest.raises(ProviderQualityValidationError):
        models.validate_provider_cache_ingestion_result(item)

    item.provider_cache_ready = True
    item.metadata_only = False
    with pytest.raises(ProviderQualityValidationError):
        models.validate_provider_cache_ingestion_result(item)

def test_validate_data_quality_score_component():
    valid_item = models.DataQualityScoreComponent(component_id="id", created_at_utc="now", provider_name="p", symbol="s", component=MagicMock(), raw_value=50.0, score=50.0, weight=0.5, weighted_score=25.0, grade=MagicMock(), explanation="exp")
    models.validate_data_quality_score_component(valid_item)

    invalid_item_score = models.DataQualityScoreComponent(component_id="id", created_at_utc="now", provider_name="p", symbol="s", component=MagicMock(), raw_value=150.0, score=150.0, weight=0.5, weighted_score=75.0, grade=MagicMock(), explanation="exp")
    with pytest.raises(ProviderQualityValidationError):
        models.validate_data_quality_score_component(invalid_item_score)

    invalid_item_weight = models.DataQualityScoreComponent(component_id="id", created_at_utc="now", provider_name="p", symbol="s", component=MagicMock(), raw_value=50.0, score=50.0, weight=2.5, weighted_score=125.0, grade=MagicMock(), explanation="exp")
    with pytest.raises(ProviderQualityValidationError):
        models.validate_data_quality_score_component(invalid_item_weight)

def test_validate_provider_data_quality_score():
    valid_item = models.ProviderDataQualityScore(score_id="id", created_at_utc="now", provider_name="p", symbol="s", capability="cap", components=[], total_score=50.0, grade=MagicMock(), usable_for_research=True, use_with_warning=False, blocked=False, explanation="", risk_flags=[], warnings=[], errors=[], metadata={})
    models.validate_provider_data_quality_score(valid_item)

    invalid_score = models.ProviderDataQualityScore(score_id="id", created_at_utc="now", provider_name="p", symbol="s", capability="cap", components=[], total_score=-10.0, grade=MagicMock(), usable_for_research=True, use_with_warning=False, blocked=False, explanation="", risk_flags=[], warnings=[], errors=[], metadata={})
    with pytest.raises(ProviderQualityValidationError):
        models.validate_provider_data_quality_score(invalid_score)

    invalid_blocked = models.ProviderDataQualityScore(score_id="id", created_at_utc="now", provider_name="p", symbol="s", capability="cap", components=[], total_score=50.0, grade=MagicMock(), usable_for_research=True, use_with_warning=False, blocked=True, explanation="", risk_flags=[], warnings=[], errors=[], metadata={})
    with pytest.raises(ProviderQualityValidationError):
        models.validate_provider_data_quality_score(invalid_blocked)

def test_validate_source_trust_profile():
    valid_item = models.SourceTrustProfile(profile_id="id", created_at_utc="now", provider_name="test.com", provider_kind="kind", historical_score=None, schema_reliability_score=None, freshness_reliability_score=None, agreement_reliability_score=None, cache_reliability_score=None, safety_reliability_score=None, trust_score=50.0, trust_level=MagicMock(), default_use_case="default", warnings=[], errors=[], risk_flags=[], metadata={})
    models.validate_source_trust_profile(valid_item)

    invalid_item = models.SourceTrustProfile(profile_id="id", created_at_utc="now", provider_name="test.com", provider_kind="kind", historical_score=None, schema_reliability_score=None, freshness_reliability_score=None, agreement_reliability_score=None, cache_reliability_score=None, safety_reliability_score=None, trust_score=150.0, trust_level=MagicMock(), default_use_case="default", warnings=[], errors=[], risk_flags=[], metadata={})
    with pytest.raises(ProviderQualityValidationError):
        models.validate_source_trust_profile(invalid_item)


def test_validate_provider_selection_score():
    valid_item = models.ProviderSelectionScore(selection_score_id="id", created_at_utc="now", provider_name="p", symbol="s", capability="cap", data_quality_score_id=None, trust_profile_id=None, quality_score=50.0, trust_score=50.0, freshness_score=50.0, safety_score=50.0, availability_score=50.0, final_selection_score=50.0, status=MagicMock(), decision=MagicMock(), rank=None, selectable_for_research=True, use_as_fallback=False, blocked=False, explanation="", risk_flags=[], warnings=[], errors=[], metadata={})
    models.validate_provider_selection_score(valid_item)

    invalid_item = models.ProviderSelectionScore(selection_score_id="id", created_at_utc="now", provider_name="p", symbol="s", capability="cap", data_quality_score_id=None, trust_profile_id=None, quality_score=50.0, trust_score=50.0, freshness_score=50.0, safety_score=50.0, availability_score=50.0, final_selection_score=150.0, status=MagicMock(), decision=MagicMock(), rank=None, selectable_for_research=True, use_as_fallback=False, blocked=False, explanation="", risk_flags=[], warnings=[], errors=[], metadata={})
    with pytest.raises(ProviderQualityValidationError):
        models.validate_provider_selection_score(invalid_item)


def test_validate_provider_ranking():
    valid_item = models.ProviderRanking(
        ranking_id="id", created_at_utc="now", symbol=None, capability="cap",
        scores=[], ranked_provider_names=[], preferred_provider=None,
        fallback_providers=[], blocked_providers=[], ranking_valid=True,
        ranking_is_research_data_only=True, produces_trade_signal=False,
        produces_order_decision=False, risk_flags=[], warnings=[], errors=[], metadata={}
    )
    models.validate_provider_ranking(valid_item)

    invalid_item = models.ProviderRanking(
        ranking_id="id", created_at_utc="now", symbol=None, capability="cap",
        scores=[], ranked_provider_names=[], preferred_provider=None,
        fallback_providers=[], blocked_providers=[], ranking_valid=True,
        ranking_is_research_data_only=False, produces_trade_signal=False,
        produces_order_decision=False, risk_flags=[], warnings=[], errors=[], metadata={}
    )
    with pytest.raises(ProviderQualityValidationError):
        models.validate_provider_ranking(invalid_item)

def test_validate_provider_quality_context():
    valid_item = models.ProviderQualityContext(
        context_id="id", created_at_utc="now", status=MagicMock(), decision=MagicMock(),
        source_provider_cache_review_id=None, ingestion=MagicMock(),
        data_quality_scores=[], trust_profiles=[], selection_scores=[], rankings=[],
        provider_quality_ready=True, source_trust_ready=True,
        provider_selection_scoring_ready=True, metadata_only=True,
        research_data_only=True, produces_trade_signal=False, produces_order_decision=False,
        network_used=False, paid_api_used=False, scraping_used=False,
        html_parsing_used=False, broker_used=False, order_created=False,
        paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False,
        risk_flags=[], warnings=[], errors=[], metadata={}
    )
    models.validate_provider_quality_context(valid_item)

    invalid_item = models.ProviderQualityContext(
        context_id="id", created_at_utc="now", status=MagicMock(), decision=MagicMock(),
        source_provider_cache_review_id=None, ingestion=MagicMock(),
        data_quality_scores=[], trust_profiles=[], selection_scores=[], rankings=[],
        provider_quality_ready=True, source_trust_ready=True,
        provider_selection_scoring_ready=True, metadata_only=True,
        research_data_only=False, produces_trade_signal=False, produces_order_decision=False,
        network_used=False, paid_api_used=False, scraping_used=False,
        html_parsing_used=False, broker_used=False, order_created=False,
        paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False,
        risk_flags=[], warnings=[], errors=[], metadata={}
    )
    with pytest.raises(ProviderQualityValidationError):
        models.validate_provider_quality_context(invalid_item)


# -- Serialization Tests --
@patch('usa_signal_bot.core.serialization.to_dict_clean')
def test_serialization_wrappers(mock_to_dict):
    mock_to_dict.return_value = {"key": "value"}

    res = models.provider_cache_ingestion_result_to_dict(MagicMock())
    assert res == {"key": "value"}

    res = models.data_quality_score_component_to_dict(MagicMock())
    assert res == {"key": "value"}

    res = models.provider_data_quality_score_to_dict(MagicMock())
    assert res == {"key": "value"}

    res = models.source_trust_profile_to_dict(MagicMock())
    assert res == {"key": "value"}

    res = models.provider_selection_score_to_dict(MagicMock())
    assert res == {"key": "value"}

    res = models.provider_ranking_to_dict(MagicMock())
    assert res == {"key": "value"}

    res = models.provider_quality_context_to_dict(MagicMock())
    assert res == {"key": "value"}

    res = models.provider_quality_full_review_to_dict(MagicMock())
    assert res == {"key": "value"}
