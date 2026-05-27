
import pandas as pd
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    AdvancedFeatureIngestionResult,
    FeatureEnrichmentSpec,
    FeatureInteractionSpec,
    FeatureConfidenceProfile,
    FeatureFreshnessProfile,
    FeatureEnrichmentRequest,
    FeatureEnrichmentResult,
    EnrichedFeatureTableResult,
    FeatureEnrichmentAudit,
    FeatureEnrichmentContext,
    FeatureEnrichmentFullReview,
    create_advanced_feature_ingestion_id,
    validate_advanced_feature_ingestion_result
)
from usa_signal_bot.feature_engine.enriched_features.advanced_feature_ingestion import (
    ingest_advanced_feature_review_payload
)
from usa_signal_bot.feature_engine.enriched_features.event_enrichment_specs import build_event_enrichment_specs
from usa_signal_bot.feature_engine.enriched_features.quality_enrichment_specs import build_quality_enrichment_specs
from usa_signal_bot.feature_engine.enriched_features.calendar_enrichment_specs import build_calendar_enrichment_specs
from usa_signal_bot.feature_engine.enriched_features.feature_interaction_specs import build_default_feature_interaction_specs
from usa_signal_bot.feature_engine.enriched_features.event_aware_features import add_event_aware_features
from usa_signal_bot.feature_engine.enriched_features.quality_aware_features import add_quality_aware_features
from usa_signal_bot.feature_engine.enriched_features.calendar_aware_features import add_calendar_aware_features
from usa_signal_bot.feature_engine.enriched_features.feature_freshness import build_feature_freshness_profile
from usa_signal_bot.feature_engine.enriched_features.feature_confidence import build_feature_confidence_profile
from usa_signal_bot.feature_engine.enriched_features.feature_anomaly_context import add_feature_anomaly_context
from usa_signal_bot.feature_engine.enriched_features.feature_interaction_builder import add_feature_interactions
from usa_signal_bot.feature_engine.enriched_features.enriched_feature_table_builder import build_enriched_feature_table

def test_ingest_advanced_feature_review_payload():
    payload = {
        "advanced_features_ready": True,
        "cross_sectional_features_ready": True,
        "multi_symbol_feature_table_ready": True,
        "ready_for_phase119": True,
        "metadata_only": True,
        "research_data_only": True,
        "activation_allowed": False,
        "active_paper_enabled": False,
        "broker_execution_enabled": False,
        "order_creation_enabled": False,
        "paper_state_mutation_enabled": False,
        "telegram_real_send_enabled": False,
        "scraping_enabled": False,
        "html_parse_enabled": False,
        "paid_api_enabled": False,
        "dashboard_enabled": False,
        "network_default_enabled": False,
        "produces_trade_signal": False,
        "produces_order_decision": False,
        "produces_portfolio_weights": False,
        "network_used": False,
        "paid_api_used": False,
        "scraping_used": False,
        "html_parsing_used": False,
        "broker_used": False,
        "order_created": False,
        "paper_state_mutated": False,
        "telegram_real_sent": False,
        "dashboard_started": False,
    }
    result = ingest_advanced_feature_review_payload(payload)
    assert result.valid_for_phase119 is True
    assert not result.errors

def test_ingest_invalid_payload():
    payload = {
        "advanced_features_ready": False,
        "activation_allowed": True
    }
    result = ingest_advanced_feature_review_payload(payload)
    assert result.valid_for_phase119 is False
    assert len(result.errors) > 0

def test_build_specs():
    assert len(build_event_enrichment_specs()) >= 11
    assert len(build_quality_enrichment_specs()) >= 6
    assert len(build_calendar_enrichment_specs()) >= 7
    assert len(build_default_feature_interaction_specs()) >= 10

def test_feature_builders():
    df = pd.DataFrame({"close": [1, 2, 3]})
    df = add_event_aware_features(df, {}, "AAPL")
    assert "event_day_flag" in df.columns

    df = add_quality_aware_features(df, {}, "AAPL")
    assert "provider_quality_score_feature" in df.columns

    df = add_calendar_aware_features(df, {}, "AAPL")
    assert "timestamp_quality_score" in df.columns

    df = add_feature_anomaly_context(df)
    assert "feature_anomaly_penalty" in df.columns

def test_interaction_builder():
    df = pd.DataFrame({"momentum_60": [1, 2], "data_confidence_score_feature": [100, 50]})
    specs = build_default_feature_interaction_specs()
    df = add_feature_interactions(df, specs)
    assert "momentum_60_x_quality_confidence" in df.columns

def test_enriched_feature_table_builder():
    df = pd.DataFrame({"close": [1, 2, 3], "momentum_60": [1, 2, 3], "data_confidence_score_feature": [100, 100, 100]})
    res_df, res = build_enriched_feature_table(df, "AAPL", None, None, None, None, build_default_feature_interaction_specs())
    assert "event_day_flag" in res_df.columns
    assert "momentum_60_x_quality_confidence" in res_df.columns
    assert res.produced_trade_signal is False

def test_profiles():
    df = pd.DataFrame({"close": [1, 2]})
    fresh = build_feature_freshness_profile("AAPL", df)
    assert fresh.freshness_score == 100.0

    conf = build_feature_confidence_profile("AAPL", df, None, fresh)
    assert conf.confidence_score == 100.0
