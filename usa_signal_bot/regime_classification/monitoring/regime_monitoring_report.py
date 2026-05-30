import datetime
from typing import Any, Dict
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringContext,
    RegimeMonitoringFullReview,
    RegimeMonitoringStatus,
    RegimeMonitoringDecision,
    RegimeMonitoringReportType,
    create_regime_monitoring_context_id,
    create_regime_monitoring_full_review_id
)

def build_regime_monitoring_context() -> RegimeMonitoringContext:
    # Dummy context builder for the report, in reality this would compose the pieces
    return RegimeMonitoringContext(
        context_id=create_regime_monitoring_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=RegimeMonitoringStatus.DRAFT,
        decision=RegimeMonitoringDecision.UNKNOWN,
        source_context_validation_review_id=None,
        ingestion=None,
        baseline=None,
        snapshot=None,
        drift_specs=[],
        drift_result=None,
        degradation_rules=[],
        degradation_diagnostics=[],
        degradation_profiles=[],
        readiness_gate=None,
        context_validation_ingested=False,
        artifacts_loaded=False,
        baseline_built=False,
        snapshot_built=False,
        drift_tracked=False,
        degradation_diagnostics_built=False,
        readiness_gate_built=False,
        readiness_gate_passed=False,
        ready_for_phase134=False,
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
        model_prediction_used=False,
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
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_regime_monitoring_full_review() -> RegimeMonitoringFullReview:
    return RegimeMonitoringFullReview(
        review_id=create_regime_monitoring_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=RegimeMonitoringReportType.FULL_PHASE133_REVIEW,
        ingestion=None,
        context=build_regime_monitoring_context(),
        baseline=None,
        snapshot=None,
        drift_result=None,
        degradation_diagnostics=[],
        degradation_profiles=[],
        readiness_gate=None,
        output_paths={},
        warnings=[],
        errors=[]
    )

def regime_monitoring_full_review_summary(review: RegimeMonitoringFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase134": review.readiness_gate.ready_for_phase134 if review.readiness_gate else False
    }

def regime_monitoring_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- This is Phase 133: Regime-Aware Monitoring, Drift Tracking, and Context Degradation Diagnostics.\n"
        "- This is purely a local, read-only metadata generation process.\n"
        "- Outputs are NOT trade signals, order decisions, or portfolio allocations.\n"
        "- Outputs are NOT investment advice.\n"
        "- This does NOT enable active paper trading or broker execution.\n"
        "- This does NOT patch production configurations."
    )

def regime_monitoring_full_review_to_text(review: RegimeMonitoringFullReview, limit: int = 300) -> str:
    summ = regime_monitoring_full_review_summary(review)
    text = f"Full Review: {summ}\n{regime_monitoring_limitations_text()}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
