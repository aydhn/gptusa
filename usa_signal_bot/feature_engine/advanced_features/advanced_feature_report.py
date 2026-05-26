from typing import List, Dict, Any, Optional
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    AdvancedFeatureContext,
    AdvancedFeatureFullReview,
    create_advanced_feature_context_id,
    create_advanced_feature_full_review_id,
    AdvancedFeatureStatus,
    AdvancedFeatureDecision,
    AdvancedFeatureReportType,
    CoreIndicatorIngestionResult,
    CrossSectionalUniverse,
    create_core_indicator_ingestion_id,
    create_cross_sectional_universe_id,
    CrossSectionalUniverseStatus
)
import datetime

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_advanced_feature_context() -> AdvancedFeatureContext:
    return AdvancedFeatureContext(
        context_id=create_advanced_feature_context_id(),
        created_at_utc=_now(),
        status=AdvancedFeatureStatus.CREATED,
        decision=AdvancedFeatureDecision.INCONCLUSIVE,
        source_core_indicator_review_id=None,
        ingestion=CoreIndicatorIngestionResult(
            ingestion_id=create_core_indicator_ingestion_id(),
            created_at_utc=_now(),
            source_path=None, source_review_id=None, source_context_id=None,
            available=False, core_indicators_ready=False, rolling_window_engine_ready=False,
            feature_table_ready=False, ready_for_phase118=False, metadata_only=True,
            research_data_only=True, activation_allowed=False, active_paper_enabled=False,
            broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False,
            telegram_real_send_enabled=False, scraping_enabled=False, html_parse_enabled=False,
            paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False,
            produces_trade_signal=False, produces_order_decision=False, network_used=False,
            paid_api_used=False, scraping_used=False, html_parsing_used=False, broker_used=False,
            order_created=False, paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False,
            valid_for_phase118=False, risk_flags=[], warnings=[], errors=[], metadata={}
        ),
        specs=[],
        universe=CrossSectionalUniverse(
            universe_id=create_cross_sectional_universe_id(),
            created_at_utc=_now(),
            name="Empty", symbols=[], min_required_symbols=2,
            status=CrossSectionalUniverseStatus.EMPTY, research_data_only=True,
            contains_benchmark_symbol=False, benchmark_symbol=None,
            warnings=[], errors=[], risk_flags=[], metadata={}
        ),
        requests=[],
        results=[],
        feature_tables=[],
        audits=[],
        advanced_features_ready=False,
        cross_sectional_features_ready=False,
        multi_symbol_feature_table_ready=False,
        ready_for_phase119=False,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
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

def build_advanced_feature_full_review() -> AdvancedFeatureFullReview:
    ctx = build_advanced_feature_context()
    return AdvancedFeatureFullReview(
        review_id=create_advanced_feature_full_review_id(),
        created_at_utc=_now(),
        report_type=AdvancedFeatureReportType.FULL_PHASE118_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        specs=[],
        universe=ctx.universe,
        results=[],
        feature_tables=[],
        audits=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def advanced_feature_full_review_summary(review: AdvancedFeatureFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "specs_count": len(review.specs),
        "results_count": len(review.results),
        "feature_tables_count": len(review.feature_tables),
        "ready_for_phase119": review.context.ready_for_phase119
    }

def advanced_feature_limitations_text() -> str:
    return (
        "LIMITATIONS: Phase 118 is for research data only. It does not provide trade signals, "
        "strategy activations, broker execution, or investment advice. Do not use advanced features "
        "for live trading."
    )

def advanced_feature_full_review_to_text(review: AdvancedFeatureFullReview, limit: int = 300) -> str:
    return (
        f"Advanced Feature Review {review.review_id}\n"
        f"Type: {review.report_type.value}\n"
        f"Specs Computed: {len(review.specs)}\n"
        f"Ready for Phase 119: {review.context.ready_for_phase119}\n\n"
        f"{advanced_feature_limitations_text()}"
    )
