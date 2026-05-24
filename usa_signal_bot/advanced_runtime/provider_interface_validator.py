from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import (
    ProviderCapabilityManifest, ProviderSafetyManifest, ProviderDataRequest, ProviderDataResponse
)
from usa_signal_bot.advanced_runtime.provider_capability_manifest import validate_provider_capability_manifest_safety
from usa_signal_bot.advanced_runtime.provider_safety_manifest import validate_provider_safety_manifest_safety

def validate_provider_interface_contract(provider: Any) -> list[str]:
    # In a real implementation this would reflect on the provider class
    return []

def validate_provider_manifests(capability_manifest: ProviderCapabilityManifest, safety_manifest: ProviderSafetyManifest) -> list[str]:
    errors = []
    errors.extend(validate_provider_capability_manifest_safety(capability_manifest))
    errors.extend(validate_provider_safety_manifest_safety(safety_manifest))
    if capability_manifest.paid_api and safety_manifest.safe_for_phase102:
        errors.append("paid_api is true but safe_for_phase102 is true")
    return errors

def validate_provider_request_response_contract(request: ProviderDataRequest, response: ProviderDataResponse | None = None) -> list[str]:
    errors = []
    if request.allow_network and not request.metadata_only:
        errors.append("allow_network is true and metadata_only is false in Phase 102")
    if response and response.network_used:
        errors.append("network_used is true in response")
    return errors

def provider_interface_validation_summary(errors: list[str]) -> dict[str, Any]:
    return {"errors": errors, "is_valid": len(errors) == 0}

def provider_interface_validator_to_text(errors: list[str]) -> str:
    return "Valid" if not errors else "Invalid:\n" + "\n".join(errors)
