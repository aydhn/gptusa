from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RuntimeRegistryRiskFlag, RuntimeMode, ConfigSurfaceDomain, ConfigSurfaceStatus,
    ProviderInterfaceKind, ProviderCapability, ProviderPermission, ProviderContractStatus,
    ProviderSafetyFlag, AdvancedRuntimeRegistryStatus, AdvancedRuntimeRegistryDecision,
    RuntimeRegistryReportType
)

def create_transition_review_ingestion_id() -> str:
    return f"TR_INGEST_{uuid.uuid4().hex[:8].upper()}"

def create_provider_data_request_id() -> str:
    return f"PROV_REQ_{uuid.uuid4().hex[:8].upper()}"

def create_provider_data_response_id() -> str:
    return f"PROV_RESP_{uuid.uuid4().hex[:8].upper()}"

def create_provider_capability_manifest_id() -> str:
    return f"PROV_CAP_{uuid.uuid4().hex[:8].upper()}"

def create_provider_safety_manifest_id() -> str:
    return f"PROV_SAF_{uuid.uuid4().hex[:8].upper()}"

def create_normalized_runtime_registry_id() -> str:
    return f"NORM_REG_{uuid.uuid4().hex[:8].upper()}"

def create_runtime_registry_full_review_id() -> str:
    return f"REG_REV_{uuid.uuid4().hex[:8].upper()}"

@dataclass
class TransitionReviewIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    available: bool
    advanced_transition_ready: bool
    current_phase: int
    final_phase: int
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    dashboard_enabled: bool
    valid_for_phase102: bool
    risk_flags: list[RuntimeRegistryRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class RuntimeModeRecord:
    mode: RuntimeMode
    enabled: bool
    allowed_in_phase102: bool
    description: str
    blocked_capabilities: list[str]
    allowed_capabilities: list[str]
    risk_flags: list[RuntimeRegistryRiskFlag]
    metadata: dict[str, Any]

@dataclass
class CapabilityPolicyRecord:
    capability_name: str
    status: str
    allowed: bool
    metadata_only: bool
    read_only: bool
    future_phase_allowed: bool
    blocked_reason: str | None
    risk_flags: list[RuntimeRegistryRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ConfigSurfaceRecord:
    domain: ConfigSurfaceDomain
    status: ConfigSurfaceStatus
    required_keys: list[str]
    present_keys: list[str]
    missing_keys: list[str]
    unsafe_keys: list[str]
    conflict_keys: list[str]
    normalized_values: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ProviderDataRequest:
    request_id: str
    provider_name: str
    interface_kind: ProviderInterfaceKind
    capability: ProviderCapability
    symbol: str | None
    symbols: list[str]
    start_date: str | None
    end_date: str | None
    interval: str | None
    adjusted: bool
    metadata_only: bool
    allow_network: bool
    allow_cache: bool
    parameters: dict[str, Any]
    metadata: dict[str, Any]

@dataclass
class ProviderDataResponse:
    response_id: str
    request_id: str
    provider_name: str
    success: bool
    rows_returned: int
    from_cache: bool
    network_used: bool
    data: Any | None
    data_quality_hints: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ProviderCapabilityManifest:
    manifest_id: str
    provider_name: str
    interface_kind: ProviderInterfaceKind
    permissions: list[ProviderPermission]
    capabilities: list[ProviderCapability]
    supports_cache: bool
    supports_rate_limit_metadata: bool
    supports_quality_hints: bool
    requires_api_key: bool
    paid_api: bool
    scraping_required: bool
    broker_related: bool
    order_related: bool
    status: ProviderContractStatus
    safety_flags: list[ProviderSafetyFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ProviderSafetyManifest:
    manifest_id: str
    provider_name: str
    safe_for_phase102: bool
    metadata_only_by_default: bool
    network_disabled_by_default: bool
    paid_api_blocked: bool
    scraping_blocked: bool
    broker_blocked: bool
    order_blocked: bool
    paper_mutation_blocked: bool
    telegram_real_send_blocked: bool
    safety_flags: list[ProviderSafetyFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class NormalizedRuntimeRegistry:
    registry_id: str
    created_at_utc: str
    status: AdvancedRuntimeRegistryStatus
    decision: AdvancedRuntimeRegistryDecision
    transition_ingestion: TransitionReviewIngestionResult
    runtime_modes: list[RuntimeModeRecord]
    capability_policies: list[CapabilityPolicyRecord]
    config_surface: list[ConfigSurfaceRecord]
    provider_capability_manifests: list[ProviderCapabilityManifest]
    provider_safety_manifests: list[ProviderSafetyManifest]
    registry_normalized: bool
    config_surface_clean: bool
    provider_interfaces_ready: bool
    safety_policy_valid: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    dashboard_enabled: bool
    risk_flags: list[RuntimeRegistryRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class RuntimeRegistryFullReview:
    review_id: str
    created_at_utc: str
    report_type: RuntimeRegistryReportType
    registry: NormalizedRuntimeRegistry
    transition_ingestion: TransitionReviewIngestionResult
    config_surface: list[ConfigSurfaceRecord]
    provider_manifests: list[ProviderCapabilityManifest]
    provider_safety_manifests: list[ProviderSafetyManifest]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def transition_review_ingestion_result_to_dict(item: TransitionReviewIngestionResult) -> dict:
    return {
        "ingestion_id": item.ingestion_id,
        "created_at_utc": item.created_at_utc,
        "source_path": item.source_path,
        "source_review_id": item.source_review_id,
        "available": item.available,
        "advanced_transition_ready": item.advanced_transition_ready,
        "current_phase": item.current_phase,
        "final_phase": item.final_phase,
        "activation_allowed": item.activation_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "scraping_enabled": item.scraping_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "valid_for_phase102": item.valid_for_phase102,
        "risk_flags": [flag.value for flag in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def runtime_mode_record_to_dict(item: RuntimeModeRecord) -> dict:
    return {
        "mode": item.mode.value,
        "enabled": item.enabled,
        "allowed_in_phase102": item.allowed_in_phase102,
        "description": item.description,
        "blocked_capabilities": item.blocked_capabilities,
        "allowed_capabilities": item.allowed_capabilities,
        "risk_flags": [flag.value for flag in item.risk_flags],
        "metadata": item.metadata,
    }

def capability_policy_record_to_dict(item: CapabilityPolicyRecord) -> dict:
    return {
        "capability_name": item.capability_name,
        "status": item.status,
        "allowed": item.allowed,
        "metadata_only": item.metadata_only,
        "read_only": item.read_only,
        "future_phase_allowed": item.future_phase_allowed,
        "blocked_reason": item.blocked_reason,
        "risk_flags": [flag.value for flag in item.risk_flags],
        "metadata": item.metadata,
    }

def config_surface_record_to_dict(item: ConfigSurfaceRecord) -> dict:
    return {
        "domain": item.domain.value,
        "status": item.status.value,
        "required_keys": item.required_keys,
        "present_keys": item.present_keys,
        "missing_keys": item.missing_keys,
        "unsafe_keys": item.unsafe_keys,
        "conflict_keys": item.conflict_keys,
        "normalized_values": item.normalized_values,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def provider_data_request_to_dict(item: ProviderDataRequest) -> dict:
    return {
        "request_id": item.request_id,
        "provider_name": item.provider_name,
        "interface_kind": item.interface_kind.value,
        "capability": item.capability.value,
        "symbol": item.symbol,
        "symbols": item.symbols,
        "start_date": item.start_date,
        "end_date": item.end_date,
        "interval": item.interval,
        "adjusted": item.adjusted,
        "metadata_only": item.metadata_only,
        "allow_network": item.allow_network,
        "allow_cache": item.allow_cache,
        "parameters": item.parameters,
        "metadata": item.metadata,
    }

def provider_data_response_to_dict(item: ProviderDataResponse) -> dict:
    return {
        "response_id": item.response_id,
        "request_id": item.request_id,
        "provider_name": item.provider_name,
        "success": item.success,
        "rows_returned": item.rows_returned,
        "from_cache": item.from_cache,
        "network_used": item.network_used,
        "data_quality_hints": item.data_quality_hints,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def provider_capability_manifest_to_dict(item: ProviderCapabilityManifest) -> dict:
    return {
        "manifest_id": item.manifest_id,
        "provider_name": item.provider_name,
        "interface_kind": item.interface_kind.value,
        "permissions": [p.value for p in item.permissions],
        "capabilities": [c.value for c in item.capabilities],
        "supports_cache": item.supports_cache,
        "supports_rate_limit_metadata": item.supports_rate_limit_metadata,
        "supports_quality_hints": item.supports_quality_hints,
        "requires_api_key": item.requires_api_key,
        "paid_api": item.paid_api,
        "scraping_required": item.scraping_required,
        "broker_related": item.broker_related,
        "order_related": item.order_related,
        "status": item.status.value,
        "safety_flags": [f.value for f in item.safety_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def provider_safety_manifest_to_dict(item: ProviderSafetyManifest) -> dict:
    return {
        "manifest_id": item.manifest_id,
        "provider_name": item.provider_name,
        "safe_for_phase102": item.safe_for_phase102,
        "metadata_only_by_default": item.metadata_only_by_default,
        "network_disabled_by_default": item.network_disabled_by_default,
        "paid_api_blocked": item.paid_api_blocked,
        "scraping_blocked": item.scraping_blocked,
        "broker_blocked": item.broker_blocked,
        "order_blocked": item.order_blocked,
        "paper_mutation_blocked": item.paper_mutation_blocked,
        "telegram_real_send_blocked": item.telegram_real_send_blocked,
        "safety_flags": [f.value for f in item.safety_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def normalized_runtime_registry_to_dict(item: NormalizedRuntimeRegistry) -> dict:
    return {
        "registry_id": item.registry_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "transition_ingestion": transition_review_ingestion_result_to_dict(item.transition_ingestion),
        "runtime_modes": [runtime_mode_record_to_dict(m) for m in item.runtime_modes],
        "capability_policies": [capability_policy_record_to_dict(p) for p in item.capability_policies],
        "config_surface": [config_surface_record_to_dict(c) for c in item.config_surface],
        "provider_capability_manifests": [provider_capability_manifest_to_dict(m) for m in item.provider_capability_manifests],
        "provider_safety_manifests": [provider_safety_manifest_to_dict(m) for m in item.provider_safety_manifests],
        "registry_normalized": item.registry_normalized,
        "config_surface_clean": item.config_surface_clean,
        "provider_interfaces_ready": item.provider_interfaces_ready,
        "safety_policy_valid": item.safety_policy_valid,
        "activation_allowed": item.activation_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "scraping_enabled": item.scraping_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "risk_flags": [flag.value for flag in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def runtime_registry_full_review_to_dict(item: RuntimeRegistryFullReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "registry": normalized_runtime_registry_to_dict(item.registry),
        "transition_ingestion": transition_review_ingestion_result_to_dict(item.transition_ingestion),
        "config_surface": [config_surface_record_to_dict(c) for c in item.config_surface],
        "provider_manifests": [provider_capability_manifest_to_dict(m) for m in item.provider_manifests],
        "provider_safety_manifests": [provider_safety_manifest_to_dict(m) for m in item.provider_safety_manifests],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_transition_review_ingestion_result(item: TransitionReviewIngestionResult) -> None:
    if item.current_phase not in [101, 102]:
        raise ValueError(f"Invalid current_phase: {item.current_phase}")
    if item.final_phase != 160:
        raise ValueError(f"Invalid final_phase: {item.final_phase}")
    if item.activation_allowed:
        raise ValueError("activation_allowed must be false in phase 102")
    if item.active_paper_enabled:
        raise ValueError("active_paper_enabled must be false")
    if item.broker_execution_enabled:
        raise ValueError("broker_execution_enabled must be false")
    if item.paper_state_mutation_enabled:
        raise ValueError("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled:
        raise ValueError("telegram_real_send_enabled must be false")
    if item.scraping_enabled:
        raise ValueError("scraping_enabled must be false")
    if item.dashboard_enabled:
        raise ValueError("dashboard_enabled must be false")

def validate_provider_capability_manifest(item: ProviderCapabilityManifest) -> None:
    if item.paid_api and not any(flag == ProviderSafetyFlag.PAID_API_RISK for flag in item.safety_flags):
         raise ValueError("Paid API requires PAID_API_RISK safety flag")
    if item.scraping_required and not any(flag == ProviderSafetyFlag.SCRAPING_RISK for flag in item.safety_flags):
         raise ValueError("Scraping requires SCRAPING_RISK safety flag")
    if item.broker_related:
         raise ValueError("Broker-related providers are blocked in Phase 102")
    if item.order_related:
         raise ValueError("Order-related providers are blocked in Phase 102")

def validate_provider_safety_manifest(item: ProviderSafetyManifest) -> None:
    pass

def validate_normalized_runtime_registry(item: NormalizedRuntimeRegistry) -> None:
    if item.activation_allowed:
        raise ValueError("activation_allowed must be false in phase 102")
    if item.active_paper_enabled:
        raise ValueError("active_paper_enabled must be false")
    if item.broker_execution_enabled:
        raise ValueError("broker_execution_enabled must be false")
    if item.paper_state_mutation_enabled:
        raise ValueError("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled:
        raise ValueError("telegram_real_send_enabled must be false")
    if item.scraping_enabled:
        raise ValueError("scraping_enabled must be false")
    if item.dashboard_enabled:
        raise ValueError("dashboard_enabled must be false")
    if item.registry_normalized and not item.safety_policy_valid:
        raise ValueError("Normalized registry requires safety_policy_valid=True")

def validate_runtime_registry_full_review(item: RuntimeRegistryFullReview) -> None:
    validate_normalized_runtime_registry(item.registry)
