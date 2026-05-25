
import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from usa_signal_bot.core.enums import (
    EventMetadataStatus, EventMetadataDecision, MarketEventKind,
    MarketEventSource, MarketEventImportance, MarketEventTimingStatus,
    EventScheduleStatus, NewsMetadataStatus, EventMetadataRiskFlag,
    EventMetadataReportType
)

@dataclass
class ProviderOrchestrationIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    provider_orchestration_ready: bool
    source_blending_ready: bool
    availability_monitor_ready: bool
    refresh_planning_ready: bool
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
    valid_for_phase111: bool
    risk_flags: List[EventMetadataRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class MacroSeriesMetadata:
    series_id: str
    created_at_utc: str
    name: str
    source: MarketEventSource
    category: str
    frequency: str
    units: Optional[str]
    country: str
    provider_hint: Optional[str]
    requires_api_key: bool
    paid_api: bool
    network_enabled_now: bool
    scraping_required: bool
    html_parsing_required: bool
    metadata_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EconomicEventMetadata:
    event_id: str
    created_at_utc: str
    event_name: str
    event_kind: MarketEventKind
    scheduled_at_utc: Optional[str]
    country: str
    currency: Optional[str]
    importance: MarketEventImportance
    source: MarketEventSource
    actual_value: Optional[float]
    forecast_value: Optional[float]
    previous_value: Optional[float]
    unit: Optional[str]
    metadata_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EarningsCalendarMetadata:
    event_id: str
    created_at_utc: str
    symbol: str
    company_name: Optional[str]
    scheduled_at_utc: Optional[str]
    fiscal_period: Optional[str]
    importance: MarketEventImportance
    source: MarketEventSource
    eps_estimate: Optional[float]
    eps_actual: Optional[float]
    revenue_estimate: Optional[float]
    revenue_actual: Optional[float]
    metadata_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CorporateActionMetadata:
    event_id: str
    created_at_utc: str
    symbol: str
    event_kind: MarketEventKind
    effective_at_utc: Optional[str]
    declared_at_utc: Optional[str]
    source: MarketEventSource
    dividend_amount: Optional[float]
    split_ratio: Optional[str]
    metadata_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NewsMetadataItem:
    news_id: str
    created_at_utc: str
    symbol: Optional[str]
    provider_name: Optional[str]
    published_at_utc: Optional[str]
    title_metadata: Optional[str]
    category: Optional[str]
    source: MarketEventSource
    url_hash: Optional[str]
    content_fetched: bool
    network_used: bool
    scraping_used: bool
    html_parsing_used: bool
    paid_api_used: bool
    metadata_only: bool
    status: NewsMetadataStatus
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class UnifiedMarketEvent:
    unified_event_id: str
    created_at_utc: str
    event_kind: MarketEventKind
    source: MarketEventSource
    symbol: Optional[str]
    country: Optional[str]
    event_name: str
    scheduled_at_utc: Optional[str]
    timing_status: MarketEventTimingStatus
    importance: MarketEventImportance
    metadata_only: bool
    source_ref_id: Optional[str]
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EventSchedule:
    schedule_id: str
    created_at_utc: str
    status: EventScheduleStatus
    events: List[UnifiedMarketEvent]
    total_events: int
    macro_event_count: int
    earnings_event_count: int
    corporate_action_count: int
    news_metadata_count: int
    duplicate_count: int
    invalid_time_count: int
    metadata_only: bool
    research_context_only: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EventScheduleIndex:
    index_id: str
    created_at_utc: str
    schedule_id: Optional[str]
    by_symbol: Dict[str, List[str]]
    by_date: Dict[str, List[str]]
    by_kind: Dict[str, List[str]]
    by_importance: Dict[str, List[str]]
    total_indexed_events: int
    index_valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EventMetadataRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EventMetadataContext:
    context_id: str
    created_at_utc: str
    status: EventMetadataStatus
    decision: EventMetadataDecision
    source_provider_orchestration_review_id: Optional[str]
    ingestion: ProviderOrchestrationIngestionResult
    macro_series: List[MacroSeriesMetadata]
    economic_events: List[EconomicEventMetadata]
    earnings_events: List[EarningsCalendarMetadata]
    corporate_actions: List[CorporateActionMetadata]
    news_metadata: List[NewsMetadataItem]
    schedule: EventSchedule
    schedule_index: EventScheduleIndex
    event_metadata_ready: bool
    macro_metadata_ready: bool
    calendar_metadata_ready: bool
    news_metadata_ready: bool
    event_schedule_ready: bool
    metadata_only: bool
    research_context_only: bool
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
    risk_flags: List[EventMetadataRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class EventMetadataFullReview:
    review_id: str
    created_at_utc: str
    report_type: EventMetadataReportType
    ingestion: ProviderOrchestrationIngestionResult
    context: EventMetadataContext
    schedule: EventSchedule
    schedule_index: EventScheduleIndex
    macro_series: List[MacroSeriesMetadata]
    economic_events: List[EconomicEventMetadata]
    earnings_events: List[EarningsCalendarMetadata]
    corporate_actions: List[CorporateActionMetadata]
    news_metadata: List[NewsMetadataItem]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def create_provider_orchestration_ingestion_id() -> str:
    return f"poi_{uuid.uuid4().hex}"

def create_macro_series_id() -> str:
    return f"macro_{uuid.uuid4().hex}"

def create_event_id(prefix: str = "event") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_news_id() -> str:
    return f"news_{uuid.uuid4().hex}"

def create_unified_event_id() -> str:
    return f"uev_{uuid.uuid4().hex}"

def create_event_schedule_id() -> str:
    return f"esch_{uuid.uuid4().hex}"

def create_event_schedule_index_id() -> str:
    return f"esidx_{uuid.uuid4().hex}"

def create_event_metadata_context_id() -> str:
    return f"emctx_{uuid.uuid4().hex}"

def create_event_metadata_full_review_id() -> str:
    return f"emrev_{uuid.uuid4().hex}"

import dataclasses

def _to_dict(obj):
    if obj is None:
        return None
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    return obj

def provider_orchestration_ingestion_result_to_dict(item) -> dict: return _to_dict(item)
def macro_series_metadata_to_dict(item) -> dict: return _to_dict(item)
def economic_event_metadata_to_dict(item) -> dict: return _to_dict(item)
def earnings_calendar_metadata_to_dict(item) -> dict: return _to_dict(item)
def corporate_action_metadata_to_dict(item) -> dict: return _to_dict(item)
def news_metadata_item_to_dict(item) -> dict: return _to_dict(item)
def unified_market_event_to_dict(item) -> dict: return _to_dict(item)
def event_schedule_to_dict(item) -> dict: return _to_dict(item)
def event_schedule_index_to_dict(item) -> dict: return _to_dict(item)
def event_metadata_context_to_dict(item) -> dict: return _to_dict(item)
def event_metadata_full_review_to_dict(item) -> dict: return _to_dict(item)

def validate_provider_orchestration_ingestion_result(item: ProviderOrchestrationIngestionResult) -> None:
    if not item.provider_orchestration_ready: raise ValueError("provider_orchestration_ready must be True")
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

def validate_macro_series_metadata(item: MacroSeriesMetadata) -> None:
    if not item.metadata_only: raise ValueError("metadata_only must be True")

def validate_economic_event_metadata(item: EconomicEventMetadata) -> None:
    if not item.metadata_only: raise ValueError("metadata_only must be True")

def validate_earnings_calendar_metadata(item: EarningsCalendarMetadata) -> None:
    if not item.metadata_only: raise ValueError("metadata_only must be True")

def validate_corporate_action_metadata(item: CorporateActionMetadata) -> None:
    if not item.metadata_only: raise ValueError("metadata_only must be True")

def validate_news_metadata_item(item: NewsMetadataItem) -> None:
    if not item.metadata_only: raise ValueError("metadata_only must be True")
    if item.content_fetched: raise ValueError("content_fetched must be False")
    if item.network_used: raise ValueError("network_used must be False")
    if item.scraping_used: raise ValueError("scraping_used must be False")
    if item.html_parsing_used: raise ValueError("html_parsing_used must be False")

def validate_event_schedule(item: EventSchedule) -> None:
    if not item.metadata_only: raise ValueError("metadata_only must be True")
    if not item.research_context_only: raise ValueError("research_context_only must be True")
    if item.produces_trade_signal: raise ValueError("produces_trade_signal must be False")
    if item.produces_order_decision: raise ValueError("produces_order_decision must be False")

def validate_event_metadata_context(item: EventMetadataContext) -> None:
    if not item.metadata_only: raise ValueError("metadata_only must be True")

def validate_event_metadata_full_review(item: EventMetadataFullReview) -> None:
    validate_event_metadata_context(item.context)
