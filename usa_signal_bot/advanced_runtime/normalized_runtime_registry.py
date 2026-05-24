from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.advanced_runtime.phase102_models import (
    NormalizedRuntimeRegistry, TransitionReviewIngestionResult, RuntimeModeRecord,
    CapabilityPolicyRecord, ConfigSurfaceRecord, ProviderCapabilityManifest,
    ProviderSafetyManifest, AdvancedRuntimeRegistryStatus, AdvancedRuntimeRegistryDecision,
    create_normalized_runtime_registry_id, create_transition_review_ingestion_id
)
from usa_signal_bot.advanced_runtime.transition_review_ingestion import ingest_advanced_transition_review_payload
from usa_signal_bot.advanced_runtime.runtime_mode_registry import build_phase102_runtime_modes
from usa_signal_bot.advanced_runtime.capability_policy import build_phase102_capability_policies
from usa_signal_bot.advanced_runtime.config_surface import build_config_surface_records

def build_normalized_runtime_registry(
    transition_ingestion: TransitionReviewIngestionResult | None = None,
    config: dict[str, Any] | None = None
) -> NormalizedRuntimeRegistry:

    if not transition_ingestion:
         transition_ingestion = TransitionReviewIngestionResult(
             ingestion_id=create_transition_review_ingestion_id(),
             created_at_utc=datetime.now(timezone.utc).isoformat(),
             source_path=None,
             source_review_id=None,
             available=False,
             advanced_transition_ready=False,
             current_phase=102,
             final_phase=160,
             activation_allowed=False,
             active_paper_enabled=False,
             broker_execution_enabled=False,
             paper_state_mutation_enabled=False,
             telegram_real_send_enabled=False,
             scraping_enabled=False,
             dashboard_enabled=False,
             valid_for_phase102=False,
             risk_flags=[],
             warnings=[],
             errors=[],
             metadata={}
         )

    return NormalizedRuntimeRegistry(
        registry_id=create_normalized_runtime_registry_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=AdvancedRuntimeRegistryStatus.NORMALIZED,
        decision=AdvancedRuntimeRegistryDecision.NORMALIZE_RUNTIME_REGISTRY,
        transition_ingestion=transition_ingestion,
        runtime_modes=build_phase102_runtime_modes(),
        capability_policies=build_phase102_capability_policies(),
        config_surface=build_config_surface_records(config or {}),
        provider_capability_manifests=[],
        provider_safety_manifests=[],
        registry_normalized=True,
        config_surface_clean=True,
        provider_interfaces_ready=True,
        safety_policy_valid=True,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        risk_flags=transition_ingestion.risk_flags,
        warnings=[],
        errors=[],
        metadata={}
    )

def build_default_normalized_runtime_registry() -> NormalizedRuntimeRegistry:
    return build_normalized_runtime_registry()

def normalized_runtime_registry_summary(registry: NormalizedRuntimeRegistry) -> dict[str, Any]:
    return {
        "registry_id": registry.registry_id,
        "status": registry.status.value,
        "normalized": registry.registry_normalized,
        "safety_valid": registry.safety_policy_valid
    }

def normalized_runtime_registry_to_text(registry: NormalizedRuntimeRegistry, limit: int = 200) -> str:
    return f"NormalizedRuntimeRegistry {registry.registry_id} - Normalized: {registry.registry_normalized}"
