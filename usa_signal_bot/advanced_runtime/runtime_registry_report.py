from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.advanced_runtime.phase102_models import (
    RuntimeRegistryFullReview, RuntimeRegistryReportType,
    create_runtime_registry_full_review_id
)
from usa_signal_bot.advanced_runtime.normalized_runtime_registry import build_normalized_runtime_registry

def build_runtime_registry_full_review(config: dict[str, Any] | None = None) -> RuntimeRegistryFullReview:
    registry = build_normalized_runtime_registry(config=config)
    return RuntimeRegistryFullReview(
        review_id=create_runtime_registry_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=RuntimeRegistryReportType.FULL_PHASE102_REVIEW,
        registry=registry,
        transition_ingestion=registry.transition_ingestion,
        config_surface=registry.config_surface,
        provider_manifests=registry.provider_capability_manifests,
        provider_safety_manifests=registry.provider_safety_manifests,
        output_paths={},
        warnings=registry.warnings,
        errors=registry.errors
    )

def runtime_registry_full_review_summary(review: RuntimeRegistryFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "registry_id": review.registry.registry_id,
        "valid": review.registry.registry_normalized and review.registry.safety_policy_valid
    }

def runtime_registry_limitations_text() -> str:
    return (
        "LIMITATIONS: Phase 102 is NOT activation. "
        "No live broker API. No paper order execution. No paper state mutation. "
        "No Telegram real send. No scraping. No dashboards."
    )

def runtime_registry_full_review_to_text(review: RuntimeRegistryFullReview, limit: int = 300) -> str:
    lines = [
        "--- Runtime Registry Full Review ---",
        f"Review ID: {review.review_id}",
        f"Registry ID: {review.registry.registry_id}",
        runtime_registry_limitations_text()
    ]
    return "\n".join(lines)
