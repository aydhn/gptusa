from usa_signal_bot.regime_classification.labeling.regime_labeling_readiness_gate import build_regime_labeling_readiness_gate
from usa_signal_bot.regime_classification.labeling.phase128_models import RegimeFeatureEngineeringIngestionResult

def test_readiness_gate():
    ingestion = RegimeFeatureEngineeringIngestionResult(
        ingestion_id="test",
        created_at_utc="2023-01-01T00:00:00Z",
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        foundation_ingested=True,
        inputs_loaded=True,
        metric_specs_ready=True,
        feature_specs_ready=True,
        metrics_computed=True,
        feature_table_ready=True,
        candidates_prepared=True,
        candidate_readiness_gate_ready=True,
        ready_for_phase128=True,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
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
        model_training_used=False,
        heavy_ml_dependency_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase128=True,
    )

    # We'll pass empty lists for label results since it fails the gate if empty, but we can verify it fails gracefully
    gate = build_regime_labeling_readiness_gate(ingestion, [], [], None, [])
    assert gate.ready_for_phase129 is False
    assert gate.model_training_used is False
    assert gate.produces_trade_signal is False
