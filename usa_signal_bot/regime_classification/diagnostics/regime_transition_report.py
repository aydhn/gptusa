from typing import Any, Dict, Optional
import pandas as pd

from usa_signal_bot.core.enums import (
    RegimeTransitionAnalyticsStatus,
    RegimeTransitionAnalyticsDecision,
    RegimeTransitionReportType,
    RegimeDiagnosticsQuality
)
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeTransitionAnalyticsResult,
    RegimeTransitionContext,
    RegimeTransitionFullReview,
    create_regime_transition_analytics_id,
    create_regime_transition_context_id,
    create_regime_transition_full_review_id,
    _now,
    RegimeLabelingIngestionResult
)
from usa_signal_bot.regime_classification.diagnostics.regime_labeling_ingestion import ingest_regime_labeling_review_payload
from usa_signal_bot.regime_classification.diagnostics.regime_transition_matrix import build_transition_matrices
from usa_signal_bot.regime_classification.diagnostics.regime_persistence_analytics import build_persistence_profiles
from usa_signal_bot.regime_classification.diagnostics.regime_duration_analytics import build_duration_profiles
from usa_signal_bot.regime_classification.diagnostics.regime_churn_diagnostics import build_churn_diagnostics
from usa_signal_bot.regime_classification.diagnostics.regime_stability_diagnostics import build_stability_diagnostics
from usa_signal_bot.regime_classification.diagnostics.regime_diagnostics_readiness_gate import build_regime_diagnostics_readiness_gate
from usa_signal_bot.regime_classification.diagnostics.regime_diagnostics_safety_validator import validate_regime_transition_analytics_safety, collect_regime_transition_risk_flags

def build_regime_transition_analytics_result(tables: Optional[Dict[str, pd.DataFrame]] = None) -> RegimeTransitionAnalyticsResult:
    if tables is None:
        tables = {}

    matrices = build_transition_matrices(tables)
    persistences = build_persistence_profiles(tables)
    durations = build_duration_profiles(tables)
    churns = build_churn_diagnostics(tables)
    stabilities = build_stability_diagnostics(tables)

    # Validation logic to ensure outputs are safe
    result = RegimeTransitionAnalyticsResult(
        analytics_id=create_regime_transition_analytics_id(),
        created_at_utc=_now(),
        transition_matrices=matrices,
        persistence_profiles=persistences,
        duration_profiles=durations,
        churn_diagnostics=churns,
        stability_diagnostics=stabilities,
        matrix_count=len(matrices),
        persistence_profile_count=len(persistences),
        duration_profile_count=len(durations),
        churn_diagnostic_count=len(churns),
        stability_diagnostic_count=len(stabilities),
        analytics_valid=True,
        quality=RegimeDiagnosticsQuality.HIGH,
        research_metadata_only=True,
        model_training_used=False,
        model_prediction_used=False,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
    )

    safety_errors = validate_regime_transition_analytics_safety(result)
    if safety_errors:
        result.analytics_valid = False
        result.quality = RegimeDiagnosticsQuality.INVALID
        result.errors.extend(safety_errors)

    return result

def build_regime_transition_context(ingestion: Optional[RegimeLabelingIngestionResult] = None, analytics: Optional[RegimeTransitionAnalyticsResult] = None) -> RegimeTransitionContext:
    if ingestion is None:
        ingestion = ingest_regime_labeling_review_payload({})
    if analytics is None:
        analytics = build_regime_transition_analytics_result()

    gate = build_regime_diagnostics_readiness_gate(ingestion, analytics)

    ctx = RegimeTransitionContext(
        context_id=create_regime_transition_context_id(),
        created_at_utc=_now(),
        status=RegimeTransitionAnalyticsStatus.READINESS_GATE_PASSED if gate.ready_for_phase130 else RegimeTransitionAnalyticsStatus.FAILED,
        decision=RegimeTransitionAnalyticsDecision.BUILD_READINESS_GATE if gate.ready_for_phase130 else RegimeTransitionAnalyticsDecision.BLOCK,
        source_regime_labeling_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        analytics_result=analytics,
        readiness_gate=gate,
        labeling_ingested=True,
        sequences_loaded=True,
        transition_matrix_built=True,
        persistence_analytics_built=True,
        duration_analytics_built=True,
        churn_diagnostics_built=True,
        stability_diagnostics_built=True,
        readiness_gate_ready=True,
        ready_for_phase130=gate.ready_for_phase130,
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
    )

    ctx.risk_flags = collect_regime_transition_risk_flags(ctx)
    return ctx

def build_regime_transition_full_review(ingestion: Optional[RegimeLabelingIngestionResult] = None, analytics: Optional[RegimeTransitionAnalyticsResult] = None) -> RegimeTransitionFullReview:
    ctx = build_regime_transition_context(ingestion, analytics)

    return RegimeTransitionFullReview(
        review_id=create_regime_transition_full_review_id(),
        created_at_utc=_now(),
        report_type=RegimeTransitionReportType.FULL_PHASE129_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        analytics_result=ctx.analytics_result,
        readiness_gate=ctx.readiness_gate,
    )

def regime_transition_full_review_summary(review: RegimeTransitionFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase130": review.context.ready_for_phase130,
        "matrices": review.analytics_result.matrix_count,
        "persistences": review.analytics_result.persistence_profile_count,
        "durations": review.analytics_result.duration_profile_count,
        "churns": review.analytics_result.churn_diagnostic_count,
        "stabilities": review.analytics_result.stability_diagnostic_count,
        "errors": len(review.errors),
        "warnings": len(review.warnings)
    }

def regime_transition_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- This phase is not an activation boundary.\n"
        "- Outputs are NOT trade signals, order decisions, or portfolio allocations.\n"
        "- Outputs are not investment advice.\n"
        "- Model training and prediction are explicitly forbidden."
    )

def regime_transition_full_review_to_text(review: RegimeTransitionFullReview, limit: int = 300) -> str:
    lines = [
        f"Regime Transition Full Review [{review.review_id}]",
        f"Ready for Phase 130: {review.readiness_gate.ready_for_phase130}",
        f"Matrices: {review.analytics_result.matrix_count}",
        f"Durations: {review.analytics_result.duration_profile_count}",
        f"Stabilities: {review.analytics_result.stability_diagnostic_count}",
        regime_transition_limitations_text()
    ]
    return "\n".join(lines)
