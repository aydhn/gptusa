import pytest
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FreezePreparationIngestionResult,
    validate_freeze_preparation_ingestion_result
)

def test_validate_freeze_preparation_ingestion_result():
    valid = FreezePreparationIngestionResult(
        ingestion_id="i", created_at_utc="u", source_path="s", source_review_id="r",
        source_context_id="c", available=True, artifact_chain_ready=True,
        integration_rehearsal_ready=True, report_qa_accepted=True, freeze_candidate_ready=True,
        freeze_readiness_gate_ready=True, ready_for_phase125=True, metadata_only=True,
        research_data_only=True, activation_allowed=False, strategy_activation_allowed=False,
        active_paper_enabled=False, broker_execution_enabled=False, order_creation_enabled=False,
        paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False,
        html_parse_enabled=False, paid_api_enabled=False, dashboard_enabled=False,
        network_default_enabled=False, produces_trade_signal=False, produces_order_decision=False,
        produces_portfolio_weights=False, investment_advice=False, deployment_allowed=False,
        network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
        broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False,
        dashboard_started=False, valid_for_phase125=True, risk_flags=[], warnings=[], errors=[], metadata={}
    )
    validate_freeze_preparation_ingestion_result(valid)

    with pytest.raises(Exception):
        invalid = valid
        invalid.activation_allowed = True
        validate_freeze_preparation_ingestion_result(invalid)
