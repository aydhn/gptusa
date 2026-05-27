"""Freeze Preparation Report."""
from typing import Any
from datetime import datetime, timezone

from .phase124_models import (
    FreezePreparationContext,
    FreezePreparationFullReview,
    FreezePreparationReportType,
    FeatureFactorIntegrationStatus,
    FeatureFactorIntegrationDecision,
    create_freeze_preparation_context_id,
    create_freeze_preparation_full_review_id,
    ExplainabilityIngestionResult,
    ArtifactChainIntegrityResult,
    IntegrationRehearsalResult,
    ReportQaAcceptanceGate,
    FreezeCandidateManifest,
    FreezePreparationGate
)

def build_freeze_preparation_context(
    ingestion: ExplainabilityIngestionResult,
    artifact_chain: ArtifactChainIntegrityResult,
    rehearsal_result: IntegrationRehearsalResult,
    report_qa_gate: ReportQaAcceptanceGate,
    freeze_manifest: FreezeCandidateManifest,
    freeze_gate: FreezePreparationGate
) -> FreezePreparationContext:

    return FreezePreparationContext(
        context_id=create_freeze_preparation_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=FeatureFactorIntegrationStatus.FREEZE_PREPARED if freeze_gate.ready_for_phase125 else FeatureFactorIntegrationStatus.BLOCKED,
        decision=FeatureFactorIntegrationDecision.BUILD_FREEZE_CANDIDATE if freeze_gate.ready_for_phase125 else FeatureFactorIntegrationDecision.BLOCK,
        source_explainability_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        artifact_chain=artifact_chain,
        rehearsal_result=rehearsal_result,
        report_qa_gate=report_qa_gate,
        freeze_manifest=freeze_manifest,
        freeze_gate=freeze_gate,
        artifact_chain_ready=artifact_chain.chain_valid,
        integration_rehearsal_ready=rehearsal_result.rehearsal_passed,
        report_qa_accepted=report_qa_gate.accepted,
        freeze_candidate_ready=freeze_manifest.ready_for_final_closure,
        freeze_readiness_gate_ready=freeze_gate.ready_for_phase125,
        ready_for_phase125=freeze_gate.ready_for_phase125,
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
        dashboard_started=False
    )

def build_freeze_preparation_full_review(context: FreezePreparationContext) -> FreezePreparationFullReview:
    return FreezePreparationFullReview(
        review_id=create_freeze_preparation_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=FreezePreparationReportType.FULL_PHASE124_REVIEW,
        ingestion=context.ingestion,
        context=context,
        artifact_chain=context.artifact_chain,
        rehearsal_result=context.rehearsal_result,
        report_qa_gate=context.report_qa_gate,
        freeze_manifest=context.freeze_manifest,
        freeze_gate=context.freeze_gate
    )

def freeze_preparation_full_review_summary(review: FreezePreparationFullReview) -> dict[str, Any]:
    return {"id": review.review_id, "ready": review.context.ready_for_phase125}

def freeze_preparation_limitations_text() -> str:
    return "Phase 124 is not activation, deployment, or signal execution."

def freeze_preparation_full_review_to_text(review: FreezePreparationFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id} - Phase 125 Ready: {review.context.ready_for_phase125}"
