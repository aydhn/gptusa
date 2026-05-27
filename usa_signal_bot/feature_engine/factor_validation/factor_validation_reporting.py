from typing import Any
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorScoringIngestionResult,
    FactorValidationRule,
    FactorValidationResult,
    FactorDriftBaseline,
    FactorDriftObservation,
    FactorDriftReport,
    FactorSchemaSignature,
    FactorVersionMetadata,
    FactorArtifactManifest,
    FactorStoreSnapshot,
    FactorRollbackMetadata,
    FactorStoreHardeningResult,
    FactorValidationContext,
    FactorValidationFullReview
)

def factor_scoring_ingestion_result_to_text(item: FactorScoringIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id}"

def factor_validation_rule_to_text(item: FactorValidationRule) -> str:
    return f"Rule {item.name}: {item.status.name}"

def factor_validation_result_to_text(item: FactorValidationResult) -> str:
    return f"Result {item.symbol}: Passed={item.validation_passed}"

def factor_drift_baseline_to_text(item: FactorDriftBaseline) -> str:
    return f"Baseline {item.symbol}: cols={len(item.factor_columns)}"

def factor_drift_observation_to_text(item: FactorDriftObservation) -> str:
    return f"Obs {item.factor_column}: {item.drift_status.name}"

def factor_drift_report_to_text(item: FactorDriftReport, limit: int = 200) -> str:
    return f"Drift {item.symbol}: {item.overall_drift_status.name}"

def factor_schema_signature_to_text(item: FactorSchemaSignature) -> str:
    return f"Schema {item.symbol}: valid={item.schema_valid}"

def factor_version_metadata_to_text(item: FactorVersionMetadata) -> str:
    return f"Version {item.version}: sealed={item.sealed}"

def factor_artifact_manifest_to_text(item: FactorArtifactManifest, limit: int = 200) -> str:
    return f"Manifest: {item.available_items}/{item.total_items}"

def factor_store_snapshot_to_text(item: FactorStoreSnapshot) -> str:
    return f"Snapshot: {item.artifact_count} artifacts"

def factor_rollback_metadata_to_text(item: FactorRollbackMetadata) -> str:
    return f"Rollback available: {item.rollback_available}"

def factor_store_hardening_result_to_text(item: FactorStoreHardeningResult, limit: int = 300) -> str:
    return f"Store Hardened: {item.store_hardened}"

def factor_validation_context_to_text(item: FactorValidationContext, limit: int = 300) -> str:
    return f"Context {item.context_id}: status={item.status.name}"

def factor_validation_full_review_to_text(item: FactorValidationFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id}: Ready={item.context.ready_for_phase123}"

def factor_validation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store has {summary.get('reviews', 0)} reviews."

def factor_validation_limitations_text() -> str:
    return "Phase 122 limitations: No live trading, no execution."
