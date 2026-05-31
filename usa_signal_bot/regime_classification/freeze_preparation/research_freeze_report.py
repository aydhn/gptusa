from typing import Any, Dict, Optional
from pathlib import Path
from usa_signal_bot.core.enums import RegimeResearchFreezeStatus, RegimeResearchFreezeDecision, RegimeResearchFreezeReportType
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeResearchFreezeContext,
    RegimeResearchFreezeFullReview,
    create_regime_research_freeze_context_id,
    create_regime_research_freeze_full_review_id,
    _now_utc_str
)

def build_regime_research_freeze_context() -> RegimeResearchFreezeContext:
    from usa_signal_bot.regime_classification.freeze_preparation.regime_monitoring_ingestion import ingest_regime_monitoring_review_payload
    from usa_signal_bot.regime_classification.freeze_preparation.monitoring_validation_runner import run_monitoring_validation
    from usa_signal_bot.regime_classification.freeze_preparation.drift_report_builder import build_drift_report_document
    from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_package_builder import build_research_freeze_package
    from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_readiness_gate import build_research_freeze_readiness_gate
    from usa_signal_bot.regime_classification.freeze_preparation.drift_report_qa_validator import run_drift_report_qa

    ingest = ingest_regime_monitoring_review_payload({})
    validation = run_monitoring_validation(ingest, None, None, None, [], [], None)
    doc = build_drift_report_document(ingest, validation, None, None, None, [], [])
    qa = run_drift_report_qa(doc)
    pkg = build_research_freeze_package(ingest, validation, doc)
    gate = build_research_freeze_readiness_gate(validation, doc, qa, pkg)

    return RegimeResearchFreezeContext(
        context_id=create_regime_research_freeze_context_id(),
        created_at_utc=_now_utc_str(),
        status=RegimeResearchFreezeStatus.CREATED,
        decision=RegimeResearchFreezeDecision.VALIDATE_MONITORING,
        source_regime_monitoring_review_id=ingest.source_review_id,
        ingestion=ingest,
        monitoring_validation=validation,
        drift_report=doc,
        drift_report_qa_results=qa,
        freeze_package=pkg,
        readiness_gate=gate,
        monitoring_ingested=True,
        monitoring_artifacts_loaded=True,
        monitoring_validated=validation.validation_passed,
        drift_report_built=True,
        drift_report_qa_passed=all(q.passed for q in qa),
        freeze_package_built=True,
        freeze_package_validated=pkg.package_valid,
        readiness_gate_built=True,
        readiness_gate_passed=gate.status.value == "PASSED" if hasattr(gate.status, 'value') else gate.status == "PASSED",
        ready_for_phase135=gate.ready_for_phase135,
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
        daemon_started=False,
        scheduler_enabled=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_regime_research_freeze_full_review() -> RegimeResearchFreezeFullReview:
    ctx = build_regime_research_freeze_context()
    return RegimeResearchFreezeFullReview(
        review_id=create_regime_research_freeze_full_review_id(),
        created_at_utc=_now_utc_str(),
        report_type=RegimeResearchFreezeReportType.FULL_PHASE134_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        monitoring_validation=ctx.monitoring_validation,
        drift_report=ctx.drift_report,
        drift_report_qa_results=ctx.drift_report_qa_results,
        freeze_package=ctx.freeze_package,
        readiness_gate=ctx.readiness_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def regime_research_freeze_full_review_summary(review: RegimeResearchFreezeFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase135": review.context.ready_for_phase135
    }

def regime_research_freeze_limitations_text() -> str:
    return "This is a local metadata review only. No real execution, deployment, or investment advice."

def regime_research_freeze_full_review_to_text(review: RegimeResearchFreezeFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id} - Ready: {review.context.ready_for_phase135}"[:limit]
