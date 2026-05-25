import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Dict, List

from usa_signal_bot.core.enums import (
    ProviderRuntimeStatus,
    ProviderRuntimeDecision,
    ProviderImplementationStatus,
    ProviderFetchMode,
    ProviderCacheLookupStatus,
    ProviderFetchDryRunStatus,
    ProviderContractTestStatus,
    ProviderRuntimeRiskFlag,
    ProviderRuntimeReportType
)


@dataclass
class ProviderAbstractionIngestionResult:
    ingestion_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_path: Optional[str] = None
    source_review_id: Optional[str] = None
    source_context_id: Optional[str] = None
    available: bool = False
    provider_abstraction_ready: bool = False
    provider_skeletons_ready: bool = False
    provider_registry_valid: bool = False
    provider_safety_valid: bool = False
    metadata_only: bool = False
    provider_network_fetch_enabled_now: bool = False
    activation_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    dashboard_enabled: bool = False
    paid_api_enabled: bool = False
    valid_for_phase107: bool = False
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderRuntimeAdapterSpec:
    runtime_adapter_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provider_name: str = ""
    adapter_module: str = ""
    adapter_class: str = ""
    implementation_status: ProviderImplementationStatus = ProviderImplementationStatus.UNKNOWN
    fetch_mode: ProviderFetchMode = ProviderFetchMode.UNKNOWN
    supports_contract_tests: bool = False
    supports_cache_key: bool = False
    supports_cache_lookup_dry_run: bool = False
    supports_local_fixture: bool = False
    supports_ohlcv_schema: bool = False
    network_guarded: bool = False
    network_enabled_by_default: bool = False
    paid_api: bool = False
    scraping_required: bool = False
    html_parsing_required: bool = False
    credential_required_now: bool = False
    broker_related: bool = False
    order_related: bool = False
    paper_mutation_related: bool = False
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderCacheKey:
    cache_key_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provider_name: str = ""
    capability: str = ""
    symbol: Optional[str] = None
    interval: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    adjusted: bool = True
    cache_namespace: str = "market_data"
    cache_key: str = ""
    cache_path: Optional[str] = None
    valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderCacheLookupResult:
    lookup_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    cache_key: ProviderCacheKey = field(default_factory=ProviderCacheKey)
    status: ProviderCacheLookupStatus = ProviderCacheLookupStatus.UNKNOWN
    dry_run_only: bool = True
    cache_enabled: bool = False
    cache_path_exists: bool = False
    rows_available: int = 0
    stale: bool = False
    fresh: bool = False
    network_required: bool = False
    network_used: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderFetchDryRunPlan:
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provider_name: str = ""
    capability: str = ""
    symbol: Optional[str] = None
    interval: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    fetch_mode: ProviderFetchMode = ProviderFetchMode.METADATA_ONLY
    metadata_only: bool = True
    dry_run_only: bool = True
    allow_cache: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    cache_key: Optional[ProviderCacheKey] = None
    expected_schema: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFetchDryRunResult:
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    plan_id: Optional[str] = None
    status: ProviderFetchDryRunStatus = ProviderFetchDryRunStatus.UNKNOWN
    provider_name: str = ""
    cache_lookup: Optional[ProviderCacheLookupResult] = None
    rows_returned: int = 0
    schema_valid: bool = False
    normalized: bool = False
    fetch_performed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    passed: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderContractTestItem:
    test_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provider_name: str = ""
    adapter_class: str = ""
    test_name: str = ""
    status: ProviderContractTestStatus = ProviderContractTestStatus.UNKNOWN
    required: bool = True
    message: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderContractTestReport:
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: ProviderRuntimeStatus = ProviderRuntimeStatus.UNKNOWN
    items: List[ProviderContractTestItem] = field(default_factory=list)
    total_tests: int = 0
    passed_tests: int = 0
    warning_tests: int = 0
    failed_tests: int = 0
    blocked_tests: int = 0
    skipped_tests: int = 0
    contract_tests_passed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderRuntimeContext:
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: ProviderRuntimeStatus = ProviderRuntimeStatus.UNKNOWN
    decision: ProviderRuntimeDecision = ProviderRuntimeDecision.UNKNOWN
    source_provider_abstraction_review_id: Optional[str] = None
    ingestion: ProviderAbstractionIngestionResult = field(default_factory=ProviderAbstractionIngestionResult)
    adapter_specs: List[ProviderRuntimeAdapterSpec] = field(default_factory=list)
    dry_run_plans: List[ProviderFetchDryRunPlan] = field(default_factory=list)
    dry_run_results: List[ProviderFetchDryRunResult] = field(default_factory=list)
    contract_test_report: ProviderContractTestReport = field(default_factory=ProviderContractTestReport)
    provider_runtime_ready: bool = False
    adapter_contracts_valid: bool = False
    cache_aware_dry_run_ready: bool = False
    metadata_only: bool = True
    network_enabled_by_default: bool = False
    paid_api_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    dashboard_enabled: bool = False
    risk_flags: List[ProviderRuntimeRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderRuntimeFullReview:
    review_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    report_type: ProviderRuntimeReportType = ProviderRuntimeReportType.FULL_PHASE107_REVIEW
    ingestion: ProviderAbstractionIngestionResult = field(default_factory=ProviderAbstractionIngestionResult)
    context: ProviderRuntimeContext = field(default_factory=ProviderRuntimeContext)
    adapter_specs: List[ProviderRuntimeAdapterSpec] = field(default_factory=list)
    dry_run_plans: List[ProviderFetchDryRunPlan] = field(default_factory=list)
    dry_run_results: List[ProviderFetchDryRunResult] = field(default_factory=list)
    contract_test_report: ProviderContractTestReport = field(default_factory=ProviderContractTestReport)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def create_provider_abstraction_ingestion_id() -> str:
    return str(uuid.uuid4())

def create_provider_runtime_adapter_id() -> str:
    return str(uuid.uuid4())

def create_provider_cache_key_id() -> str:
    return str(uuid.uuid4())

def create_provider_cache_lookup_id() -> str:
    return str(uuid.uuid4())

def create_provider_fetch_dry_run_plan_id() -> str:
    return str(uuid.uuid4())

def create_provider_fetch_dry_run_result_id() -> str:
    return str(uuid.uuid4())

def create_provider_contract_test_id() -> str:
    return str(uuid.uuid4())

def create_provider_contract_test_report_id() -> str:
    return str(uuid.uuid4())

def create_provider_runtime_context_id() -> str:
    return str(uuid.uuid4())

def create_provider_runtime_full_review_id() -> str:
    return str(uuid.uuid4())


import dataclasses

def provider_abstraction_ingestion_result_to_dict(item: ProviderAbstractionIngestionResult) -> dict:
    return dataclasses.asdict(item)

def provider_runtime_adapter_spec_to_dict(item: ProviderRuntimeAdapterSpec) -> dict:
    return dataclasses.asdict(item)

def provider_cache_key_to_dict(item: ProviderCacheKey) -> dict:
    return dataclasses.asdict(item)

def provider_cache_lookup_result_to_dict(item: ProviderCacheLookupResult) -> dict:
    return dataclasses.asdict(item)

def provider_fetch_dry_run_plan_to_dict(item: ProviderFetchDryRunPlan) -> dict:
    return dataclasses.asdict(item)

def provider_fetch_dry_run_result_to_dict(item: ProviderFetchDryRunResult) -> dict:
    return dataclasses.asdict(item)

def provider_contract_test_item_to_dict(item: ProviderContractTestItem) -> dict:
    return dataclasses.asdict(item)

def provider_contract_test_report_to_dict(item: ProviderContractTestReport) -> dict:
    return dataclasses.asdict(item)

def provider_runtime_context_to_dict(item: ProviderRuntimeContext) -> dict:
    return dataclasses.asdict(item)

def provider_runtime_full_review_to_dict(item: ProviderRuntimeFullReview) -> dict:
    return dataclasses.asdict(item)

from usa_signal_bot.core.exceptions import ProviderRuntimeValidationError

def validate_provider_abstraction_ingestion_result(item: ProviderAbstractionIngestionResult) -> None:
    if not item.provider_abstraction_ready:
        raise ProviderRuntimeValidationError("provider_abstraction_ready must be True")
    if not item.provider_registry_valid:
        raise ProviderRuntimeValidationError("provider_registry_valid must be True")
    if not item.provider_safety_valid:
        raise ProviderRuntimeValidationError("provider_safety_valid must be True")
    if not item.metadata_only:
        raise ProviderRuntimeValidationError("metadata_only must be True")
    if item.provider_network_fetch_enabled_now:
        raise ProviderRuntimeValidationError("provider_network_fetch_enabled_now must be False")
    if item.activation_allowed:
        raise ProviderRuntimeValidationError("activation_allowed must be False")
    if item.active_paper_enabled:
        raise ProviderRuntimeValidationError("active_paper_enabled must be False")
    if item.broker_execution_enabled:
        raise ProviderRuntimeValidationError("broker_execution_enabled must be False")
    if item.paper_state_mutation_enabled:
        raise ProviderRuntimeValidationError("paper_state_mutation_enabled must be False")
    if item.telegram_real_send_enabled:
        raise ProviderRuntimeValidationError("telegram_real_send_enabled must be False")
    if item.scraping_enabled:
        raise ProviderRuntimeValidationError("scraping_enabled must be False")
    if item.html_parse_enabled:
        raise ProviderRuntimeValidationError("html_parse_enabled must be False")
    if item.dashboard_enabled:
        raise ProviderRuntimeValidationError("dashboard_enabled must be False")
    if item.paid_api_enabled:
        raise ProviderRuntimeValidationError("paid_api_enabled must be False")


def validate_provider_runtime_adapter_spec(item: ProviderRuntimeAdapterSpec) -> None:
    if item.network_enabled_by_default:
        raise ProviderRuntimeValidationError("network_enabled_by_default must be False")
    if item.paid_api:
        raise ProviderRuntimeValidationError("paid_api must be False")
    if item.scraping_required:
        raise ProviderRuntimeValidationError("scraping_required must be False")
    if item.html_parsing_required:
        raise ProviderRuntimeValidationError("html_parsing_required must be False")
    if item.credential_required_now:
        raise ProviderRuntimeValidationError("credential_required_now must be False")
    if item.broker_related or item.order_related or item.paper_mutation_related:
        raise ProviderRuntimeValidationError("broker/order/paper mutation related must be False")

def validate_provider_cache_key(item: ProviderCacheKey) -> None:
    if not item.valid:
        raise ProviderRuntimeValidationError("Provider cache key is not valid")

def validate_provider_fetch_dry_run_plan(item: ProviderFetchDryRunPlan) -> None:
    if not item.dry_run_only:
        raise ProviderRuntimeValidationError("dry_run_only must be True in dry run plan")
    if item.allow_network:
        raise ProviderRuntimeValidationError("allow_network must be False in dry run plan default")

def validate_provider_fetch_dry_run_result(item: ProviderFetchDryRunResult) -> None:
    if item.fetch_performed:
        raise ProviderRuntimeValidationError("fetch_performed must be False")
    if item.network_used:
        raise ProviderRuntimeValidationError("network_used must be False")
    if item.paid_api_used:
        raise ProviderRuntimeValidationError("paid_api_used must be False")
    if item.scraping_used or item.html_parsing_used or item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.dashboard_started:
        raise ProviderRuntimeValidationError("Unauthorized usage in dry run result")

def validate_provider_contract_test_report(item: ProviderContractTestReport) -> None:
    if item.network_used:
        raise ProviderRuntimeValidationError("network_used must be False in contract tests")
    if item.paid_api_used:
        raise ProviderRuntimeValidationError("paid_api_used must be False in contract tests")
    if item.scraping_used or item.html_parsing_used or item.broker_used or item.order_created or item.paper_state_mutated:
        raise ProviderRuntimeValidationError("Unauthorized usage in contract tests")


def validate_provider_runtime_context(item: ProviderRuntimeContext) -> None:
    validate_provider_abstraction_ingestion_result(item.ingestion)
    for spec in item.adapter_specs:
        validate_provider_runtime_adapter_spec(spec)
    for plan in item.dry_run_plans:
        validate_provider_fetch_dry_run_plan(plan)
    for res in item.dry_run_results:
        validate_provider_fetch_dry_run_result(res)
    validate_provider_contract_test_report(item.contract_test_report)


def validate_provider_runtime_full_review(item: ProviderRuntimeFullReview) -> None:
    validate_provider_abstraction_ingestion_result(item.ingestion)
    validate_provider_runtime_context(item.context)
