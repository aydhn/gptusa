from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import (
    ProviderCapabilityManifest, ProviderInterfaceKind, ProviderCapability,
    ProviderPermission, ProviderSafetyFlag, ProviderContractStatus,
    create_provider_capability_manifest_id
)

def build_provider_capability_manifest(
    provider_name: str,
    interface_kind: ProviderInterfaceKind,
    capabilities: list[ProviderCapability] | None = None,
    permissions: list[ProviderPermission] | None = None,
    supports_cache: bool = True,
    supports_rate_limit_metadata: bool = True,
    supports_quality_hints: bool = True,
    requires_api_key: bool = False,
    paid_api: bool = False,
    scraping_required: bool = False,
    broker_related: bool = False,
    order_related: bool = False
) -> ProviderCapabilityManifest:
    flags = []
    if paid_api:
        flags.append(ProviderSafetyFlag.PAID_API_RISK)
    if scraping_required:
        flags.append(ProviderSafetyFlag.SCRAPING_RISK)
    if broker_related:
        flags.append(ProviderSafetyFlag.BROKER_RISK)
    if order_related:
        flags.append(ProviderSafetyFlag.ORDER_RISK)

    return ProviderCapabilityManifest(
        manifest_id=create_provider_capability_manifest_id(),
        provider_name=provider_name,
        interface_kind=interface_kind,
        permissions=permissions or [ProviderPermission.METADATA_ONLY],
        capabilities=capabilities or [],
        supports_cache=supports_cache,
        supports_rate_limit_metadata=supports_rate_limit_metadata,
        supports_quality_hints=supports_quality_hints,
        requires_api_key=requires_api_key,
        paid_api=paid_api,
        scraping_required=scraping_required,
        broker_related=broker_related,
        order_related=order_related,
        status=ProviderContractStatus.READY,
        safety_flags=flags,
        warnings=[],
        errors=[],
        metadata={}
    )

def default_market_data_provider_manifest(provider_name: str) -> ProviderCapabilityManifest:
    return build_provider_capability_manifest(
        provider_name=provider_name,
        interface_kind=ProviderInterfaceKind.MARKET_DATA,
        capabilities=[ProviderCapability.GET_DAILY_BARS, ProviderCapability.SYMBOL_SEARCH]
    )

def default_metadata_only_provider_manifest(provider_name: str, interface_kind: ProviderInterfaceKind) -> ProviderCapabilityManifest:
    return build_provider_capability_manifest(
        provider_name=provider_name,
        interface_kind=interface_kind,
        capabilities=[ProviderCapability.GET_PROVIDER_STATUS]
    )

def validate_provider_capability_manifest_safety(manifest: ProviderCapabilityManifest) -> list[str]:
    errors = []
    if manifest.broker_related or manifest.order_related:
        errors.append(f"{manifest.provider_name} has broker/order capabilities which are forbidden")
    if manifest.scraping_required and ProviderSafetyFlag.SCRAPING_RISK not in manifest.safety_flags:
         errors.append(f"{manifest.provider_name} is missing scraping risk flag")
    return errors

def provider_capability_manifest_summary(manifest: ProviderCapabilityManifest) -> dict[str, Any]:
    return {
        "provider_name": manifest.provider_name,
        "kind": manifest.interface_kind.value,
        "capabilities_count": len(manifest.capabilities),
        "safety_flags": [f.value for f in manifest.safety_flags]
    }

def provider_capability_manifest_to_text(manifest: ProviderCapabilityManifest) -> str:
    return f"Provider Capability Manifest [{manifest.provider_name}] - Kind: {manifest.interface_kind.value}"
