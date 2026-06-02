from typing import Any

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    AdvancedMLClosureContext,
    AdvancedMLClosureFullReview,
    MLGovernanceClosureReportType,
    MLGovernanceClosureStatus,
    MLGovernanceClosureDecision,
    create_advanced_ml_closure_context_id,
    create_advanced_ml_closure_full_review_id,
    current_time,
    DriftMonitoringIngestionResult,
    ExplainabilityReport,
    AdvancedMLArtifactLineage,
    MLGovernanceClosureResult,
    AdvancedMLFinalAuditResult,
    NonActivationMLClosureBoundaryResult,
    FinalMLModelCardClosure,
    AdvancedMLAcceptanceGate
)

# In a real implementation this would build out the full structure
# taking all the dependencies as input.
# To keep this mock simple, we just assume they are passed in if needed.

def build_advanced_ml_closure_context(
    ingestion: DriftMonitoringIngestionResult,
    explainability_report: ExplainabilityReport,
    artifact_lineage: AdvancedMLArtifactLineage,
    governance_closure: MLGovernanceClosureResult,
    final_audit: AdvancedMLFinalAuditResult,
    non_activation_boundary: NonActivationMLClosureBoundaryResult,
    final_model_card_closure: FinalMLModelCardClosure,
    acceptance_gate: AdvancedMLAcceptanceGate
) -> AdvancedMLClosureContext:

    passed = acceptance_gate.ready_for_phase146

    return AdvancedMLClosureContext(
        context_id=create_advanced_ml_closure_context_id(),
        created_at_utc=current_time(),
        status=MLGovernanceClosureStatus.VALIDATED if passed else MLGovernanceClosureStatus.FAILED,
        decision=MLGovernanceClosureDecision.BUILD_ACCEPTANCE_GATE,
        source_drift_monitoring_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        input_references=explainability_report.input_references,
        explainability_report=explainability_report,
        artifact_lineage=artifact_lineage,
        governance_closure=governance_closure,
        final_audit=final_audit,
        non_activation_boundary=non_activation_boundary,
        final_model_card_closure=final_model_card_closure,
        acceptance_gate=acceptance_gate,
        drift_monitoring_ingested=True,
        drift_artifacts_loaded=True,
        explainability_inputs_resolved=True,
        feature_attribution_built=True,
        factor_contribution_built=True,
        model_behavior_explanation_built=True,
        regime_aware_explanation_built=True,
        calibration_aware_explanation_built=True,
        ensemble_explanation_built=True,
        explainability_report_built=True,
        artifact_lineage_built=True,
        ml_governance_closure_built=True,
        advanced_ml_final_audit_built=True,
        non_activation_boundary_validated=True,
        final_model_cards_updated=True,
        acceptance_gate_built=True,
        acceptance_gate_passed=passed,
        ready_for_phase146=passed,
        phase136_to_145_closed=passed,
        metadata_only=True,
        research_data_only=True,
        offline_ml_research_only=True,
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
        live_monitoring_enabled=False,
        alert_sender_enabled=False,
        daemon_started=False,
        scheduler_enabled=False,
        live_inference_enabled=False,
        online_inference_enabled=False,
        threshold_optimization_performed=False,
        backtest_executed=False,
        heavy_ml_dependency_used=False,
        shap_lime_dependency_used=False,
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

def build_advanced_ml_closure_full_review(context: AdvancedMLClosureContext) -> AdvancedMLClosureFullReview:
    return AdvancedMLClosureFullReview(
        review_id=create_advanced_ml_closure_full_review_id(),
        created_at_utc=current_time(),
        report_type=MLGovernanceClosureReportType.FULL_PHASE145_REVIEW,
        ingestion=context.ingestion,
        context=context,
        explainability_report=context.explainability_report,
        governance_closure=context.governance_closure,
        artifact_lineage=context.artifact_lineage,
        final_audit=context.final_audit,
        non_activation_boundary=context.non_activation_boundary,
        final_model_card_closure=context.final_model_card_closure,
        acceptance_gate=context.acceptance_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def advanced_ml_closure_full_review_summary(review: AdvancedMLClosureFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase146": review.context.ready_for_phase146,
        "phase136_to_145_closed": review.context.phase136_to_145_closed
    }

def advanced_ml_closure_limitations_text() -> str:
    return (
        "Phase 145 LIMITATIONS:\n"
        "- This phase is for explainability metadata and governance closure only.\n"
        "- It does NOT enable active paper trading, deployment, or live inference.\n"
        "- The outputs of this phase are research diagnostics, NOT trade signals or investment advice.\n"
        "- Backtesting, transaction costs, and walk-forward analysis will begin in Phase 146."
    )

def advanced_ml_closure_full_review_to_text(review: AdvancedMLClosureFullReview, limit: int = 300) -> str:
    summary = advanced_ml_closure_full_review_summary(review)
    status = "PASSED" if summary["ready_for_phase146"] else "FAILED"
    return f"Full Review {summary['review_id']} - Status: {status}\nReady for Phase 146: {summary['ready_for_phase146']}"
