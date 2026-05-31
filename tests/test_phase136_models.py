import pytest
from usa_signal_bot.ml_research.foundation.phase136_models import (
    RegimeFinalClosureIngestionResult, MLDatasetContract, MLFoundationReadinessGate,
    create_regime_final_closure_ingestion_id
)

def test_ingestion_result_creation():
    res = RegimeFinalClosureIngestionResult(
        ingestion_id=create_regime_final_closure_ingestion_id(),
        created_at_utc="2023-01-01T00:00:00Z",
        source_path=None, source_review_id=None, source_context_id=None,
        available=True, research_freeze_ingested=True, artifact_chain_loaded=True,
        artifact_chain_validated=True, final_closure_validated=True, freeze_seal_created=True,
        final_safety_audit_passed=True, ml_input_contract_built=True, ml_kickoff_gate_built=True,
        ml_kickoff_gate_passed=True, ready_for_phase136=True, metadata_only=True,
        research_data_only=True, activation_allowed=False, strategy_activation_allowed=False,
        deployment_allowed=False, active_paper_enabled=False, broker_execution_enabled=False,
        order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False,
        scraping_enabled=False, html_parse_enabled=False, paid_api_enabled=False, dashboard_enabled=False,
        network_default_enabled=False, daemon_started=False, scheduler_enabled=False, model_training_used=False,
        model_prediction_used=False, heavy_ml_dependency_used=False, produces_trade_signal=False,
        produces_order_decision=False, produces_portfolio_weights=False, investment_advice=False,
        network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
        broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False,
        dashboard_started=False, valid_for_phase136=True
    )
    assert res.valid_for_phase136 is True
    assert res.model_training_used is False
    assert res.activation_allowed is False
