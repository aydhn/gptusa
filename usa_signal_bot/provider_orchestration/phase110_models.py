from dataclasses import dataclass, field
from typing import Any
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    ProviderOrchestrationStatus, ProviderOrchestrationDecision, ProviderRouteStatus,
    ProviderRouteDecision, SourceBlendMethod, SourceBlendStatus, DataAvailabilityStatus,
    RefreshPlanStatus, RefreshPriority, ProviderOrchestrationRiskFlag, ProviderOrchestrationReportType
)

@dataclass
class ProviderQualityIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    provider_quality_ready: bool
    source_trust_ready: bool
    provider_selection_scoring_ready: bool
    metadata_only: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase110: bool
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class OrchestratedDataRequest:
    request_id: str
    created_at_utc: str
    symbol: str
    capability: str
    interval: str | None
    preferred_provider: str | None
    allow_blending: bool
    allow_fallback: bool
    cache_only: bool
    local_fixture_allowed: bool
    dry_run_only: bool
    research_data_only: bool
    allow_network: bool
    allow_paid_api: bool
    allow_scraping: bool
    allow_html_parsing: bool
    allow_broker: bool
    allow_order: bool
    allow_paper_mutation: bool
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderRoutePlan:
    route_plan_id: str
    created_at_utc: str
    request_id: str | None
    symbol: str
    capability: str
    interval: str | None
    route_status: ProviderRouteStatus
    route_decision: ProviderRouteDecision
    primary_provider: str | None
    fallback_providers: list[str] = field(default_factory=list)
    candidate_providers: list[str] = field(default_factory=list)
    blocked_providers: list[str] = field(default_factory=list)
    source_blend_method: SourceBlendMethod = SourceBlendMethod.UNKNOWN
    cache_only: bool = True
    dry_run_only: bool = True
    research_data_only: bool = True
    network_required: bool = False
    refresh_required_future: bool = False
    route_score: float | None = None
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderRouteResult:
    route_result_id: str
    created_at_utc: str
    route_plan_id: str | None
    selected_provider: str | None
    selected_fallback_provider: str | None
    route_status: ProviderRouteStatus
    route_decision: ProviderRouteDecision
    used_blended_source: bool
    used_cache_only: bool
    used_local_fixture: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    passed: bool
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SourceBlendInput:
    blend_input_id: str
    created_at_utc: str
    symbol: str
    capability: str
    interval: str | None
    source_provider_names: list[str]
    source_quality_scores: dict[str, float]
    source_trust_scores: dict[str, float]
    source_records: dict[str, list[dict[str, Any]]]
    blend_method: SourceBlendMethod
    tolerance_pct: float
    dry_run_only: bool
    research_data_only: bool
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SourceBlendResult:
    blend_result_id: str
    created_at_utc: str
    blend_input_id: str | None
    symbol: str
    status: SourceBlendStatus
    method: SourceBlendMethod
    selected_primary_source: str | None
    included_sources: list[str] = field(default_factory=list)
    excluded_sources: list[str] = field(default_factory=list)
    blended_record_count: int = 0
    disagreement_warning_count: int = 0
    confidence_score: float | None = None
    blended_records_metadata: dict[str, Any] = field(default_factory=dict)
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    dry_run_only: bool = True
    research_data_only: bool = True
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DataAvailabilityItem:
    availability_id: str
    created_at_utc: str
    symbol: str
    capability: str
    interval: str | None
    provider_name: str | None
    status: DataAvailabilityStatus
    cache_available: bool
    cache_fresh: bool
    cache_stale: bool
    local_fixture_available: bool
    provider_quality_score: float | None
    source_trust_score: float | None
    rows_available: int
    last_available_timestamp: str | None
    refresh_required_future: bool
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DataAvailabilityReport:
    availability_report_id: str
    created_at_utc: str
    items: list[DataAvailabilityItem] = field(default_factory=list)
    total_items: int = 0
    available_count: int = 0
    partial_count: int = 0
    stale_count: int = 0
    missing_count: int = 0
    insufficient_quality_count: int = 0
    coverage_ratio: float = 0.0
    availability_ready: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RefreshPlanItem:
    refresh_item_id: str
    created_at_utc: str
    symbol: str
    capability: str
    interval: str | None
    provider_name: str | None
    status: RefreshPlanStatus
    priority: RefreshPriority
    reason: str
    stale: bool
    missing: bool
    low_quality: bool
    source_disagreement: bool
    refresh_required_future: bool
    dry_run_only: bool
    network_allowed_now: bool
    paid_api_allowed: bool
    scraping_allowed: bool
    html_parsing_allowed: bool
    broker_allowed: bool
    order_allowed: bool
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RefreshPlanReport:
    refresh_report_id: str
    created_at_utc: str
    items: list[RefreshPlanItem] = field(default_factory=list)
    total_items: int = 0
    refresh_required_count: int = 0
    high_priority_count: int = 0
    blocked_count: int = 0
    dry_run_only: bool = True
    network_allowed_now: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderOrchestrationContext:
    context_id: str
    created_at_utc: str
    status: ProviderOrchestrationStatus
    decision: ProviderOrchestrationDecision
    source_provider_quality_review_id: str | None
    ingestion: ProviderQualityIngestionResult | None = None
    route_plans: list[ProviderRoutePlan] = field(default_factory=list)
    route_results: list[ProviderRouteResult] = field(default_factory=list)
    blend_results: list[SourceBlendResult] = field(default_factory=list)
    availability_report: DataAvailabilityReport | None = None
    refresh_report: RefreshPlanReport | None = None
    provider_orchestration_ready: bool = False
    source_blending_ready: bool = False
    availability_monitor_ready: bool = False
    refresh_planning_ready: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    risk_flags: list[ProviderOrchestrationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderOrchestrationFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderOrchestrationReportType
    ingestion: ProviderQualityIngestionResult | None = None
    context: ProviderOrchestrationContext | None = None
    route_plans: list[ProviderRoutePlan] = field(default_factory=list)
    route_results: list[ProviderRouteResult] = field(default_factory=list)
    blend_results: list[SourceBlendResult] = field(default_factory=list)
    availability_report: DataAvailabilityReport | None = None
    refresh_report: RefreshPlanReport | None = None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_provider_quality_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:12]}"

def create_orchestrated_data_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"

def create_provider_route_plan_id() -> str:
    return f"plan_{uuid.uuid4().hex[:12]}"

def create_provider_route_result_id() -> str:
    return f"res_{uuid.uuid4().hex[:12]}"

def create_source_blend_input_id() -> str:
    return f"blendin_{uuid.uuid4().hex[:12]}"

def create_source_blend_result_id() -> str:
    return f"blendout_{uuid.uuid4().hex[:12]}"

def create_data_availability_id() -> str:
    return f"avail_{uuid.uuid4().hex[:12]}"

def create_data_availability_report_id() -> str:
    return f"availrep_{uuid.uuid4().hex[:12]}"

def create_refresh_plan_item_id() -> str:
    return f"refitem_{uuid.uuid4().hex[:12]}"

def create_refresh_plan_report_id() -> str:
    return f"refrep_{uuid.uuid4().hex[:12]}"

def create_provider_orchestration_context_id() -> str:
    return f"orchctx_{uuid.uuid4().hex[:12]}"

def create_provider_orchestration_full_review_id() -> str:
    return f"orchrev_{uuid.uuid4().hex[:12]}"

import dataclasses
def _to_dict(item):
    if item is None:
        return None
    return dataclasses.asdict(item)

def provider_quality_ingestion_result_to_dict(item) -> dict: return _to_dict(item)
def orchestrated_data_request_to_dict(item) -> dict: return _to_dict(item)
def provider_route_plan_to_dict(item) -> dict: return _to_dict(item)
def provider_route_result_to_dict(item) -> dict: return _to_dict(item)
def source_blend_input_to_dict(item) -> dict: return _to_dict(item)
def source_blend_result_to_dict(item) -> dict: return _to_dict(item)
def data_availability_item_to_dict(item) -> dict: return _to_dict(item)
def data_availability_report_to_dict(item) -> dict: return _to_dict(item)
def refresh_plan_item_to_dict(item) -> dict: return _to_dict(item)
def refresh_plan_report_to_dict(item) -> dict: return _to_dict(item)
def provider_orchestration_context_to_dict(item) -> dict: return _to_dict(item)
def provider_orchestration_full_review_to_dict(item) -> dict: return _to_dict(item)

def validate_provider_quality_ingestion_result(item: ProviderQualityIngestionResult) -> None:
    if not item.provider_quality_ready: raise ValueError("provider_quality_ready must be True")
    if not item.source_trust_ready: raise ValueError("source_trust_ready must be True")
    if not item.provider_selection_scoring_ready: raise ValueError("provider_selection_scoring_ready must be True")
    if not item.metadata_only: raise ValueError("metadata_only must be True")
    if not item.research_data_only: raise ValueError("research_data_only must be True")
    if item.produces_trade_signal: raise ValueError("produces_trade_signal must be False")
    if item.produces_order_decision: raise ValueError("produces_order_decision must be False")
    if item.network_used: raise ValueError("network_used must be False")
    if item.paid_api_used: raise ValueError("paid_api_used must be False")
    if item.scraping_used: raise ValueError("scraping_used must be False")
    if item.html_parsing_used: raise ValueError("html_parsing_used must be False")
    if item.broker_used: raise ValueError("broker_used must be False")
    if item.order_created: raise ValueError("order_created must be False")
    if item.paper_state_mutated: raise ValueError("paper_state_mutated must be False")
    if item.telegram_real_sent: raise ValueError("telegram_real_sent must be False")
    if item.dashboard_started: raise ValueError("dashboard_started must be False")

def validate_orchestrated_data_request(item: OrchestratedDataRequest) -> None:
    if item.allow_network: raise ValueError("allow_network must be False")
    if item.allow_paid_api: raise ValueError("allow_paid_api must be False")
    if item.allow_scraping: raise ValueError("allow_scraping must be False")
    if item.allow_html_parsing: raise ValueError("allow_html_parsing must be False")
    if item.allow_broker: raise ValueError("allow_broker must be False")
    if item.allow_order: raise ValueError("allow_order must be False")
    if item.allow_paper_mutation: raise ValueError("allow_paper_mutation must be False")

def validate_provider_route_plan(item: ProviderRoutePlan) -> None:
    pass

def validate_provider_route_result(item: ProviderRouteResult) -> None:
    if item.network_used: raise ValueError("network_used must be False")

def validate_source_blend_result(item: SourceBlendResult) -> None:
    if item.produces_trade_signal: raise ValueError("produces_trade_signal must be False")
    if item.produces_order_decision: raise ValueError("produces_order_decision must be False")

def validate_data_availability_report(item: DataAvailabilityReport) -> None:
    pass

def validate_refresh_plan_report(item: RefreshPlanReport) -> None:
    if item.network_allowed_now: raise ValueError("network_allowed_now must be False")
    if not item.dry_run_only: raise ValueError("dry_run_only must be True")

def validate_provider_orchestration_context(item: ProviderOrchestrationContext) -> None:
    pass

def validate_provider_orchestration_full_review(item: ProviderOrchestrationFullReview) -> None:
    pass
