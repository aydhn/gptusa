from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorValidationContext,
    FactorValidationFullReview,
    FactorValidationStatus,
    FactorValidationDecision,
    FactorValidationReportType,
    create_factor_validation_context_id,
    create_factor_validation_full_review_id,
    FactorScoringIngestionResult,
    FactorValidationResult,
    FactorDriftBaseline,
    FactorDriftReport,
    FactorSchemaSignature,
    FactorVersionMetadata,
    FactorArtifactManifest,
    FactorStoreSnapshot,
    FactorRollbackMetadata,
    FactorStoreHardeningResult
)

def build_factor_validation_context(
    ingestion: FactorScoringIngestionResult,
    validation_results: list[FactorValidationResult],
    drift_baselines: list[FactorDriftBaseline],
    drift_reports: list[FactorDriftReport],
    schema_signatures: list[FactorSchemaSignature],
    version_metadata: FactorVersionMetadata,
    artifact_manifest: FactorArtifactManifest,
    store_snapshot: FactorStoreSnapshot,
    rollback_metadata: FactorRollbackMetadata,
    hardening_result: FactorStoreHardeningResult
) -> FactorValidationContext:

    ready = (
        hardening_result.store_hardened and
        all(r.validation_passed for r in validation_results) and
        manifest_is_clean(artifact_manifest)
    )

    return FactorValidationContext(
        context_id=create_factor_validation_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=FactorValidationStatus.STORE_HARDENED if ready else FactorValidationStatus.FAILED,
        decision=FactorValidationDecision.HARDEN_FACTOR_STORE,
        source_factor_scoring_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        validation_results=validation_results,
        drift_baselines=drift_baselines,
        drift_reports=drift_reports,
        schema_signatures=schema_signatures,
        version_metadata=version_metadata,
        artifact_manifest=artifact_manifest,
        store_snapshot=store_snapshot,
        rollback_metadata=rollback_metadata,
        hardening_result=hardening_result,
        factor_validation_ready=all(r.validation_passed for r in validation_results),
        drift_monitoring_ready=True,
        factor_versioning_ready=version_metadata.sealed,
        factor_store_hardened=hardening_result.store_hardened,
        ready_for_phase123=ready,
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

def manifest_is_clean(manifest: FactorArtifactManifest) -> bool:
    return manifest.manifest_valid and manifest.secret_violation_count == 0 and manifest.forbidden_column_violation_count == 0

def build_factor_validation_full_review(context: FactorValidationContext) -> FactorValidationFullReview:
    return FactorValidationFullReview(
        review_id=create_factor_validation_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=FactorValidationReportType.FULL_PHASE122_REVIEW,
        ingestion=context.ingestion,
        context=context,
        validation_results=context.validation_results,
        drift_reports=context.drift_reports,
        schema_signatures=context.schema_signatures,
        version_metadata=context.version_metadata,
        artifact_manifest=context.artifact_manifest,
        hardening_result=context.hardening_result,
        output_paths={},
        warnings=[],
        errors=[]
    )

def factor_validation_full_review_summary(review: FactorValidationFullReview) -> dict[str, Any]:
    return {"status": review.context.status.name, "ready_for_phase123": review.context.ready_for_phase123}

def factor_validation_limitations_text() -> str:
    return "Phase 122 limitations: No live trading, no execution."

def factor_validation_full_review_to_text(review: FactorValidationFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id}: Ready={review.context.ready_for_phase123}"
