import datetime
from typing import Any

from usa_signal_bot.core.enums import FactorExplainabilityStatus, FactorExplainabilityDecision, FactorExplainabilityReportType, FactorExplainabilityQuality
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ExplainabilityContext,
    ExplainabilityFullReview,
    create_explainability_context_id,
    create_explainability_full_review_id,
    FactorValidationIngestionResult,
    ExplainabilityInputBundle,
    FactorExplanationReport,
    ResearchReportDocument,
    create_factor_explanation_report_id,
    create_explainability_input_bundle_id,
    create_factor_validation_ingestion_id,
    create_research_report_document_id
)

def _build_dummy_ingestion() -> FactorValidationIngestionResult:
    return FactorValidationIngestionResult(
        ingestion_id=create_factor_validation_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        source_path=None,
        source_review_id="test_review",
        source_context_id=None,
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

def _build_dummy_bundle() -> ExplainabilityInputBundle:
    return ExplainabilityInputBundle(
        bundle_id=create_explainability_input_bundle_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        source_review_id=None,
        factor_table_paths={},
        validation_result_refs=[],
        drift_report_refs=[],
        diagnostics_refs=[],
        manifest_ref=None,
        schema_signature_ref=None,
        version_ref=None,
        available=True,
        research_data_only=True,
        bundle_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def _build_dummy_report() -> FactorExplanationReport:
    from usa_signal_bot.feature_engine.factor_explainability.phase123_models import FactorExplanationReport
    return FactorExplanationReport(
        explanation_report_id=create_factor_explanation_report_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        symbol=None,
        factor_names=[],
        attribution_results=[],
        contribution_profiles=[],
        interpretation_summaries=[],
        quality=FactorExplainabilityQuality.ACCEPTABLE,
        report_valid=True,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def _build_dummy_doc() -> ResearchReportDocument:
    from usa_signal_bot.feature_engine.factor_explainability.phase123_models import ResearchReportDocument, ResearchReportFormat, ReportQaStatus
    return ResearchReportDocument(
        document_id=create_research_report_document_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        title="Empty",
        format=ResearchReportFormat.MARKDOWN,
        sections=[],
        source_explanation_report_id=None,
        source_review_id=None,
        rendered_path=None,
        document_hash=None,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        qa_status=ReportQaStatus.NOT_CHECKED,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_explainability_context() -> ExplainabilityContext:
    return ExplainabilityContext(
        context_id=create_explainability_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=FactorExplainabilityStatus.CREATED,
        decision=FactorExplainabilityDecision.BUILD_ATTRIBUTIONS,
        source_factor_validation_review_id=None,
        ingestion=_build_dummy_ingestion(),
        input_bundle=_build_dummy_bundle(),
        attribution_specs=[],
        attribution_results=[],
        contribution_profiles=[],
        interpretation_summaries=[],
        explanation_report=_build_dummy_report(),
        research_report=_build_dummy_doc(),
        qa_results=[],
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
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_explainability_full_review() -> ExplainabilityFullReview:
    ctx = build_explainability_context()
    return ExplainabilityFullReview(
        review_id=create_explainability_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        report_type=FactorExplainabilityReportType.FULL_PHASE123_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        input_bundle=ctx.input_bundle,
        attribution_specs=ctx.attribution_specs,
        explanation_report=ctx.explanation_report,
        research_report=ctx.research_report,
        qa_results=ctx.qa_results,
        output_paths={},
        warnings=[],
        errors=[]
    )

def explainability_full_review_summary(review: ExplainabilityFullReview) -> dict[str, Any]:
    return {"status": review.context.status.value, "valid": review.context.ready_for_phase124}

def explainability_limitations_text() -> str:
    return "This review is for metadata and research purposes only. No active trading."

def explainability_full_review_to_text(review: ExplainabilityFullReview, limit: int = 300) -> str:
    return f"Explainability Full Review {review.review_id} - Ready for Phase 124: {review.context.ready_for_phase124}"
