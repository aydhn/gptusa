from usa_signal_bot.regime_classification.alignment.phase131_models import MarketBehaviorIngestionResult, _now
def test_market_behavior_ingestion_result():
    res = MarketBehaviorIngestionResult(
        ingestion_id="i1", created_at_utc=_now(), source_path=None, source_review_id=None,
        source_context_id=None, available=True, transition_analytics_ingested=True,
        diagnostics_loaded=True, profile_specs_ready=True, behavior_profiles_ready=True,
        regime_summaries_ready=True, diagnostics_interpreted=True, report_built=True,
        report_qa_passed=True, readiness_gate_ready=True, ready_for_phase131=True,
        metadata_only=True, research_data_only=True, activation_allowed=False,
        strategy_activation_allowed=False, deployment_allowed=False, active_paper_enabled=False,
        broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False, scraping_enabled=False, html_parse_enabled=False,
        paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False,
        model_training_used=False, model_prediction_used=False, heavy_ml_dependency_used=False,
        produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False,
        investment_advice=False, network_used=False, paid_api_used=False, scraping_used=False,
        html_parsing_used=False, broker_used=False, order_created=False, paper_state_mutated=False,
        telegram_real_sent=False, dashboard_started=False, valid_for_phase131=True
    )
    assert res.valid_for_phase131
