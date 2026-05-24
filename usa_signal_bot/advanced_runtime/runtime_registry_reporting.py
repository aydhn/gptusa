from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import (
    TransitionReviewIngestionResult, RuntimeModeRecord, CapabilityPolicyRecord,
    ConfigSurfaceRecord, ProviderCapabilityManifest, ProviderSafetyManifest,
    NormalizedRuntimeRegistry, RuntimeRegistryFullReview
)
from usa_signal_bot.advanced_runtime.transition_review_ingestion import transition_review_ingestion_to_text
from usa_signal_bot.advanced_runtime.runtime_mode_registry import runtime_mode_registry_to_text
from usa_signal_bot.advanced_runtime.capability_policy import capability_policy_to_text
from usa_signal_bot.advanced_runtime.config_surface import config_surface_to_text
from usa_signal_bot.advanced_runtime.provider_capability_manifest import provider_capability_manifest_to_text
from usa_signal_bot.advanced_runtime.provider_safety_manifest import provider_safety_manifest_to_text
from usa_signal_bot.advanced_runtime.normalized_runtime_registry import normalized_runtime_registry_to_text
from usa_signal_bot.advanced_runtime.runtime_registry_report import runtime_registry_full_review_to_text, runtime_registry_limitations_text

def transition_review_ingestion_result_to_text(item: TransitionReviewIngestionResult) -> str:
    return transition_review_ingestion_to_text(item)

def runtime_mode_record_to_text(item: RuntimeModeRecord) -> str:
    return f"Mode: {item.mode.value} | Enabled: {item.enabled}"

def capability_policy_record_to_text(item: CapabilityPolicyRecord) -> str:
    return f"Capability: {item.capability_name} | Status: {item.status}"

def config_surface_record_to_text(item: ConfigSurfaceRecord) -> str:
    return f"Domain: {item.domain.value} | Status: {item.status.value}"

def runtime_registry_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
