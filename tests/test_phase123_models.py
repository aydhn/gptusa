import pytest
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    FactorValidationIngestionResult,
    create_factor_validation_ingestion_id,
    validate_factor_validation_ingestion_result
)

def test_factor_validation_ingestion_result():
    res = FactorValidationIngestionResult(
        ingestion_id=create_factor_validation_ingestion_id(),
        created_at_utc="",
        source_path=None,
        source_review_id="rev",
        source_context_id="ctx",
        available=True,
        factor_validation_ready=True,
        drift_monitoring_ready=True,
        factor_versioning_ready=True,
        factor_store_hardened=True,
        ready_for_phase123=True,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
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
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase123=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )
    validate_factor_validation_ingestion_result(res)
    assert not res.errors

def test_factor_validation_ingestion_result_invalid():
    res = FactorValidationIngestionResult(
        ingestion_id="i", created_at_utc="", source_path=None, source_review_id=None, source_context_id=None,
        available=True, factor_validation_ready=False, drift_monitoring_ready=True, factor_versioning_ready=True,
        factor_store_hardened=True, ready_for_phase123=True, metadata_only=True, research_data_only=True,
        activation_allowed=True, strategy_activation_allowed=False, active_paper_enabled=False, broker_execution_enabled=False,
        order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False,
        html_parse_enabled=False, paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False, produces_trade_signal=False,
        produces_order_decision=False, produces_portfolio_weights=False, network_used=False, paid_api_used=False, scraping_used=False,
        html_parsing_used=False, broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False,
        valid_for_phase123=True, risk_flags=[], warnings=[], errors=[], metadata={}
    )
    validate_factor_validation_ingestion_result(res)
    assert "factor_validation_ready false" in res.errors
    assert "activation_allowed true" in res.errors
