from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import (
    ProviderSafetyManifest, ProviderCapabilityManifest, ProviderSafetyFlag,
    create_provider_safety_manifest_id
)

def build_provider_safety_manifest(provider_name: str, manifest: ProviderCapabilityManifest | None = None) -> ProviderSafetyManifest:
    flags = manifest.safety_flags if manifest else []
    safe_for_102 = True
    if manifest and (manifest.paid_api or manifest.scraping_required or manifest.broker_related or manifest.order_related):
        safe_for_102 = False

    return ProviderSafetyManifest(
        manifest_id=create_provider_safety_manifest_id(),
        provider_name=provider_name,
        safe_for_phase102=safe_for_102,
        metadata_only_by_default=True,
        network_disabled_by_default=True,
        paid_api_blocked=True,
        scraping_blocked=True,
        broker_blocked=True,
        order_blocked=True,
        paper_mutation_blocked=True,
        telegram_real_send_blocked=True,
        safety_flags=flags,
        warnings=[],
        errors=[],
        metadata={}
    )

def validate_provider_safety_manifest_safety(manifest: ProviderSafetyManifest) -> list[str]:
    errors = []
    if not manifest.metadata_only_by_default:
        errors.append("metadata_only_by_default must be True")
    if not manifest.network_disabled_by_default:
        errors.append("network_disabled_by_default must be True")
    if not manifest.broker_blocked:
        errors.append("broker_blocked must be True")
    if not manifest.order_blocked:
         errors.append("order_blocked must be True")
    return errors

def provider_safety_manifest_blocks_execution(manifest: ProviderSafetyManifest) -> bool:
    return (manifest.broker_blocked and manifest.order_blocked and manifest.paper_mutation_blocked)

def provider_safety_manifest_summary(manifest: ProviderSafetyManifest) -> dict[str, Any]:
    return {
        "provider_name": manifest.provider_name,
        "safe_for_102": manifest.safe_for_phase102,
        "blocks_execution": provider_safety_manifest_blocks_execution(manifest)
    }

def provider_safety_manifest_to_text(manifest: ProviderSafetyManifest) -> str:
    return f"Provider Safety Manifest [{manifest.provider_name}] - Safe for Phase 102: {manifest.safe_for_phase102}"
