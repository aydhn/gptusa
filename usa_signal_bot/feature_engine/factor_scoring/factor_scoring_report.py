from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringContext,
    FactorScoringFullReview,
    FactorScoringReportType,
    FactorScoringStatus,
    FactorScoringDecision,
    FactorCompositionIngestionResult,
    create_factor_scoring_context_id,
    create_factor_scoring_full_review_id,
    create_factor_composition_ingestion_id
)

def build_factor_scoring_context() -> FactorScoringContext:
    return FactorScoringContext(
        context_id=create_factor_scoring_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=FactorScoringStatus.CREATED,
        decision=FactorScoringDecision.INCONCLUSIVE,
        source_factor_composition_review_id=None,
        ingestion=FactorCompositionIngestionResult(
            ingestion_id=create_factor_composition_ingestion_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            source_path=None,
            source_review_id=None,
            source_context_id=None,
            available=False,
            feature_groups_ready=False,
            factor_candidates_ready=False,
            selection_metadata_ready=False,
            factor_readiness_gate_ready=False,
            ready_for_phase121=False,
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
            valid_for_phase121=False,
            risk_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        ),
        scoring_specs=[],
        requests=[],
        results=[],
        factor_tables=[],
        diagnostics_profiles=[],
        audits=[],
        factor_scoring_ready=False,
        factor_normalization_ready=False,
        factor_diagnostics_ready=False,
        factor_table_ready=False,
        ready_for_phase122=False,
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
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_factor_scoring_full_review() -> FactorScoringFullReview:
    context = build_factor_scoring_context()
    return FactorScoringFullReview(
        review_id=create_factor_scoring_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=FactorScoringReportType.FULL_PHASE121_REVIEW,
        ingestion=context.ingestion,
        context=context,
        scoring_specs=[],
        results=[],
        factor_tables=[],
        diagnostics_profiles=[],
        audits=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def factor_scoring_full_review_summary(review: FactorScoringFullReview) -> dict[str, Any]:
    return {"status": "ok"}

def factor_scoring_limitations_text() -> str:
    return "Phase 121 is not activation. Factor scores are not trade signals."

def factor_scoring_full_review_to_text(review: FactorScoringFullReview, limit: int = 300) -> str:
    return "Review OK."
