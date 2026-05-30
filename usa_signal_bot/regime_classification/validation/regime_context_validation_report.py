from typing import Any
from usa_signal_bot.core.enums import RegimeContextValidationStatus, RegimeContextValidationDecision, RegimeContextValidationReportType
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeAlignmentIngestionResult,
    CompatibilityValidationResult,
    ConditionalDiagnosticSpec,
    ConditionalDiagnosticResult,
    ConditionalDiagnosticsProfile,
    RegimeAwareAcceptanceGate,
    RegimeContextValidationContext,
    RegimeContextValidationFullReview,
    create_regime_context_validation_context_id,
    create_regime_context_validation_full_review_id,
    _now_utc
)

def build_regime_context_validation_context(
    ingestion: RegimeAlignmentIngestionResult,
    validation_result: CompatibilityValidationResult,
    diagnostic_specs: list[ConditionalDiagnosticSpec],
    conditional_diagnostics: list[ConditionalDiagnosticResult],
    diagnostics_profiles: list[ConditionalDiagnosticsProfile],
    acceptance_gate: RegimeAwareAcceptanceGate
) -> RegimeContextValidationContext:
    passed = validation_result.validation_passed and acceptance_gate.ready_for_phase133
    status = RegimeContextValidationStatus.VALIDATED if passed else RegimeContextValidationStatus.FAILED
    decision = RegimeContextValidationDecision.BUILD_ACCEPTANCE_GATE if passed else RegimeContextValidationDecision.BLOCK

    return RegimeContextValidationContext(
        context_id=create_regime_context_validation_context_id(),
        created_at_utc=_now_utc(),
        status=status,
        decision=decision,
        source_regime_alignment_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        validation_result=validation_result,
        diagnostic_specs=diagnostic_specs,
        conditional_diagnostics=conditional_diagnostics,
        diagnostics_profiles=diagnostics_profiles,
        acceptance_gate=acceptance_gate,
        alignment_ingested=True,
        alignment_artifacts_loaded=True,
        validation_specs_ready=True,
        compatibility_validated=True,
        conditional_diagnostics_built=True,
        acceptance_gate_built=True,
        acceptance_gate_passed=acceptance_gate.ready_for_phase133,
        ready_for_phase133=acceptance_gate.ready_for_phase133,
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
        risk_flags=list(set(ingestion.risk_flags + validation_result.risk_flags + acceptance_gate.risk_flags)),
        metadata={}
    )

def build_regime_context_validation_full_review(context: RegimeContextValidationContext, output_paths: dict[str, str] = None) -> RegimeContextValidationFullReview:
    return RegimeContextValidationFullReview(
        review_id=create_regime_context_validation_full_review_id(),
        created_at_utc=_now_utc(),
        report_type=RegimeContextValidationReportType.FULL_PHASE132_REVIEW,
        ingestion=context.ingestion,
        context=context,
        validation_result=context.validation_result,
        conditional_diagnostics=context.conditional_diagnostics,
        diagnostics_profiles=context.diagnostics_profiles,
        acceptance_gate=context.acceptance_gate,
        output_paths=output_paths or {},
        warnings=list(context.warnings),
        errors=list(context.errors)
    )

def regime_context_validation_full_review_summary(review: RegimeContextValidationFullReview) -> dict[str, Any]:
    return {
        "ready_for_phase133": review.context.ready_for_phase133,
        "diagnostics_count": len(review.conditional_diagnostics),
        "validation_passed": review.validation_result.validation_passed
    }

def regime_context_validation_limitations_text() -> str:
    return (
        "Phase 132 Limitations:\n"
        "1. This is not strategy activation or deployment.\n"
        "2. This is purely read-only metadata validation.\n"
        "3. No real trades, signals, orders, or portfolio weights are produced.\n"
        "4. No live or paper execution."
    )

def regime_context_validation_full_review_to_text(review: RegimeContextValidationFullReview, limit: int = 300) -> str:
    s = regime_context_validation_full_review_summary(review)
    return (
        f"Regime Context Validation Full Review\n"
        f"Validation Passed: {s['validation_passed']}\n"
        f"Diagnostics count: {s['diagnostics_count']}\n"
        f"Ready for Phase 133: {s['ready_for_phase133']}\n"
    )
