import pytest
from usa_signal_bot.feature_engine.integration_freeze.phase124_models import (
    ExplainabilityIngestionResult, FreezeCandidateManifest,
    FreezePreparationRiskFlag, validate_explainability_ingestion_result,
    validate_freeze_candidate_manifest
)

def test_explainability_ingestion_result_validation():
    # Setup safe ingestion
    ingest = ExplainabilityIngestionResult(
        ingestion_id="i1",
        created_at_utc="now",
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        attribution_ready=True,
        contribution_ready=True,
        interpretation_ready=True,
        research_report_ready=True,
        report_qa_passed=True,
        ready_for_phase124=True,
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
        valid_for_phase124=True
    )
    validate_explainability_ingestion_result(ingest) # Should not raise

    # Check activation allowed failure
    ingest.activation_allowed = True
    with pytest.raises(ValueError):
        validate_explainability_ingestion_result(ingest)

def test_freeze_candidate_manifest_validation():
    manifest = FreezeCandidateManifest(
        manifest_id="m1",
        created_at_utc="now",
        status="MANIFESTED",
        artifacts=[],
        total_artifacts=0,
        included_artifacts=0,
        missing_required_artifacts=0,
        manifest_hash="hash",
        immutable=True,
        research_data_only=True,
        no_secret_leak=True,
        no_forbidden_columns=True,
        no_execution_language=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        ready_for_final_closure=True
    )
    validate_freeze_candidate_manifest(manifest)

    manifest.activation_allowed = True
    with pytest.raises(ValueError):
        validate_freeze_candidate_manifest(manifest)
