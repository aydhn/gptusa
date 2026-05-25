from dataclasses import dataclass, field, asdict
from typing import Any, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    ProviderAbstractionStatus,
    ProviderAbstractionDecision,
    DataProviderKind,
    DataProviderName,
    DataProviderAdapterStatus,
    DataProviderAdapterDecision,
    DataProviderPermission,
    DataProviderCapability,
    ProviderDataDomain,
    ProviderSafetyStatus,
    ProviderSelectorMode,
    ProviderRiskFlag,
    ProviderReportType
)
from usa_signal_bot.core.exceptions import ProviderValidationError

@dataclass
class ProviderKickoffGateIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_gate_id: Optional[str]
    available: bool
    provider_ready: bool
    ready_for_phase106: bool
    phase106_scope_allowed: bool
    metadata_only: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    dashboard_enabled: bool
    paid_api_enabled: bool
    provider_network_fetch_required: bool
    valid_for_phase106: bool
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderAdapterSpec:
    adapter_id: str
    created_at_utc: str
    provider_name: DataProviderName
    provider_kind: DataProviderKind
    adapter_status: DataProviderAdapterStatus
    adapter_decision: DataProviderAdapterDecision
    permissions: list[DataProviderPermission]
    capabilities: list[DataProviderCapability]
    domains: list[ProviderDataDomain]
    supports_cache: bool
    supports_local_fixture: bool
    supports_rate_limit_metadata: bool
    supports_quality_hints: bool
    requires_api_key: bool
    paid_api: bool
    scraping_required: bool
    html_parsing_required: bool
    broker_related: bool
    order_related: bool
    network_fetch_enabled_now: bool
    network_fetch_future_allowed: bool
    credential_required_now: bool
    skeleton_only: bool
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderRegistryEntry:
    entry_id: str
    created_at_utc: str
    provider_name: DataProviderName
    provider_kind: DataProviderKind
    adapter_module: str
    adapter_class: str
    enabled: bool
    default_provider: bool
    priority: int
    selector_mode: ProviderSelectorMode
    adapter_spec: ProviderAdapterSpec
    safety_status: ProviderSafetyStatus
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderCapabilityMatrix:
    matrix_id: str
    created_at_utc: str
    entries: list[ProviderRegistryEntry]
    capability_to_providers: dict[str, list[str]]
    domain_to_providers: dict[str, list[str]]
    default_provider_by_kind: dict[str, str]
    matrix_valid: bool
    missing_required_capability_count: int
    unsafe_provider_count: int
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderSafetyPolicy:
    policy_id: str
    created_at_utc: str
    metadata_only_by_default: bool
    network_fetch_disabled_now: bool
    paid_api_blocked: bool
    scraping_blocked: bool
    html_parsing_blocked: bool
    broker_blocked: bool
    order_blocked: bool
    paper_mutation_blocked: bool
    telegram_real_send_blocked: bool
    dashboard_blocked: bool
    credential_required_blocked_now: bool
    unknown_license_warning: bool
    unknown_rate_limit_warning: bool
    policy_valid: bool
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderSelectionRequest:
    selection_id: str
    created_at_utc: str
    provider_kind: DataProviderKind
    capability: DataProviderCapability
    domain: ProviderDataDomain
    selector_mode: ProviderSelectorMode
    symbol: Optional[str]
    metadata_only: bool
    allow_network: bool
    allow_paid_api: bool
    allow_scraping: bool
    allow_broker: bool
    allow_order: bool
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderSelectionResult:
    result_id: str
    created_at_utc: str
    selection_id: str
    selected_provider: Optional[DataProviderName]
    selected_entry_id: Optional[str]
    fallback_providers: list[DataProviderName]
    selection_safe: bool
    metadata_only: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    broker_used: bool
    order_created: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFallbackPlan:
    plan_id: str
    created_at_utc: str
    provider_kind: DataProviderKind
    capability: DataProviderCapability
    primary_provider: Optional[DataProviderName]
    fallback_chain: list[DataProviderName]
    fallback_mode: ProviderSelectorMode
    max_attempts: int
    network_allowed: bool
    paid_api_allowed: bool
    scraping_allowed: bool
    broker_allowed: bool
    order_allowed: bool
    plan_safe: bool
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderAbstractionContext:
    context_id: str
    created_at_utc: str
    status: ProviderAbstractionStatus
    decision: ProviderAbstractionDecision
    source_kickoff_gate_id: Optional[str]
    kickoff_ingestion: ProviderKickoffGateIngestionResult
    registry_entries: list[ProviderRegistryEntry]
    capability_matrix: ProviderCapabilityMatrix
    safety_policy: ProviderSafetyPolicy
    fallback_plans: list[ProviderFallbackPlan]
    provider_abstraction_ready: bool
    provider_skeletons_ready: bool
    provider_registry_valid: bool
    provider_safety_valid: bool
    metadata_only: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    dashboard_enabled: bool
    paid_api_enabled: bool
    provider_network_fetch_enabled_now: bool
    risk_flags: list[ProviderRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderAbstractionFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderReportType
    kickoff_ingestion: ProviderKickoffGateIngestionResult
    context: ProviderAbstractionContext
    registry_entries: list[ProviderRegistryEntry]
    adapter_specs: list[ProviderAdapterSpec]
    capability_matrix: ProviderCapabilityMatrix
    safety_policy: ProviderSafetyPolicy
    fallback_plans: list[ProviderFallbackPlan]
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_provider_kickoff_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:8]}"

def create_provider_adapter_id() -> str:
    return f"adapter_{uuid.uuid4().hex[:8]}"

def create_provider_registry_entry_id() -> str:
    return f"registry_{uuid.uuid4().hex[:8]}"

def create_provider_capability_matrix_id() -> str:
    return f"matrix_{uuid.uuid4().hex[:8]}"

def create_provider_safety_policy_id() -> str:
    return f"policy_{uuid.uuid4().hex[:8]}"

def create_provider_selection_id() -> str:
    return f"sel_{uuid.uuid4().hex[:8]}"

def create_provider_selection_result_id() -> str:
    return f"selres_{uuid.uuid4().hex[:8]}"

def create_provider_fallback_plan_id() -> str:
    return f"plan_{uuid.uuid4().hex[:8]}"

def create_provider_abstraction_context_id() -> str:
    return f"ctx_{uuid.uuid4().hex[:8]}"

def create_provider_abstraction_full_review_id() -> str:
    return f"rev_{uuid.uuid4().hex[:8]}"

def provider_kickoff_gate_ingestion_result_to_dict(item: ProviderKickoffGateIngestionResult) -> dict:
    return asdict(item)

def provider_adapter_spec_to_dict(item: ProviderAdapterSpec) -> dict:
    return asdict(item)

def provider_registry_entry_to_dict(item: ProviderRegistryEntry) -> dict:
    return asdict(item)

def provider_capability_matrix_to_dict(item: ProviderCapabilityMatrix) -> dict:
    return asdict(item)

def provider_safety_policy_to_dict(item: ProviderSafetyPolicy) -> dict:
    return asdict(item)

def provider_selection_request_to_dict(item: ProviderSelectionRequest) -> dict:
    return asdict(item)

def provider_selection_result_to_dict(item: ProviderSelectionResult) -> dict:
    return asdict(item)

def provider_fallback_plan_to_dict(item: ProviderFallbackPlan) -> dict:
    return asdict(item)

def provider_abstraction_context_to_dict(item: ProviderAbstractionContext) -> dict:
    return asdict(item)

def provider_abstraction_full_review_to_dict(item: ProviderAbstractionFullReview) -> dict:
    return asdict(item)

def validate_provider_kickoff_gate_ingestion_result(item: ProviderKickoffGateIngestionResult) -> None:
    if not item.ready_for_phase106: raise ProviderValidationError("ready_for_phase106 must be true")
    if not item.phase106_scope_allowed: raise ProviderValidationError("phase106_scope_allowed must be true")
    if not item.metadata_only: raise ProviderValidationError("metadata_only must be true")
    if item.activation_allowed: raise ProviderValidationError("activation_allowed must be false")
    if item.active_paper_enabled: raise ProviderValidationError("active_paper_enabled must be false")
    if item.broker_execution_enabled: raise ProviderValidationError("broker_execution_enabled must be false")
    if item.paper_state_mutation_enabled: raise ProviderValidationError("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled: raise ProviderValidationError("telegram_real_send_enabled must be false")
    if item.scraping_enabled: raise ProviderValidationError("scraping_enabled must be false")
    if item.html_parse_enabled: raise ProviderValidationError("html_parse_enabled must be false")
    if item.dashboard_enabled: raise ProviderValidationError("dashboard_enabled must be false")
    if item.paid_api_enabled: raise ProviderValidationError("paid_api_enabled must be false")
    if item.provider_network_fetch_required: raise ProviderValidationError("provider_network_fetch_required must be false")

def validate_provider_adapter_spec(item: ProviderAdapterSpec) -> None:
    if item.paid_api and ProviderRiskFlag.PAID_API_RISK not in item.risk_flags: raise ProviderValidationError("paid_api true without risk flag")
    if item.scraping_required: raise ProviderValidationError("scraping_required true is invalid")
    if item.html_parsing_required: raise ProviderValidationError("html_parsing_required true is invalid")
    if item.broker_related: raise ProviderValidationError("broker_related true is invalid")
    if item.order_related: raise ProviderValidationError("order_related true is invalid")
    if item.network_fetch_enabled_now: raise ProviderValidationError("network_fetch_enabled_now must be false")
    if item.credential_required_now: raise ProviderValidationError("credential_required_now must be false")
    if not item.skeleton_only: raise ProviderValidationError("skeleton_only must be true")

def validate_provider_registry_entry(item: ProviderRegistryEntry) -> None:
    validate_provider_adapter_spec(item.adapter_spec)

def validate_provider_capability_matrix(item: ProviderCapabilityMatrix) -> None:
    pass

def validate_provider_safety_policy(item: ProviderSafetyPolicy) -> None:
    pass

def validate_provider_selection_request(item: ProviderSelectionRequest) -> None:
    if item.allow_network: raise ProviderValidationError("allow_network must be false")
    if item.allow_paid_api: raise ProviderValidationError("allow_paid_api must be false")
    if item.allow_scraping: raise ProviderValidationError("allow_scraping must be false")

def validate_provider_selection_result(item: ProviderSelectionResult) -> None:
    if item.network_used: raise ProviderValidationError("network_used must be false")
    if item.paid_api_used: raise ProviderValidationError("paid_api_used must be false")
    if item.scraping_used: raise ProviderValidationError("scraping_used must be false")
    if item.broker_used: raise ProviderValidationError("broker_used must be false")
    if item.order_created: raise ProviderValidationError("order_created must be false")

def validate_provider_abstraction_context(item: ProviderAbstractionContext) -> None:
    pass

def validate_provider_abstraction_full_review(item: ProviderAbstractionFullReview) -> None:
    pass
