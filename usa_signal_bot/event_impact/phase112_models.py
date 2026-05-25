
import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
from usa_signal_bot.core.enums import (
    EventImpactStatus, EventImpactDecision, EventImpactCategory, EventImpactDirection,
    EventImpactConfidence, MacroRegimeMetadataLabel, CalendarValidationStatus,
    CalendarAnomalyKind, CalendarValidationExplanationType, EventImpactRiskFlag,
    EventImpactReportType
)

def _now() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"

@dataclass
class EventMetadataIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
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
    valid_for_phase112: bool
    risk_flags: List[EventImpactRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventImpactTag:
    impact_tag_id: str
    created_at_utc: str
    source_event_id: Optional[str]
    symbol: Optional[str]
    event_name: str
    event_kind: str
    impact_category: EventImpactCategory
    impact_direction: EventImpactDirection
    impact_confidence: EventImpactConfidence
    importance_score: float
    timing_score: float
    context_score: float
    research_context_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    explanation: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[EventImpactRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SymbolEventExposure:
    exposure_id: str
    created_at_utc: str
    symbol: str
    event_ids: List[str]
    high_impact_event_count: int
    medium_impact_event_count: int
    low_impact_event_count: int
    nearest_event_at_utc: Optional[str]
    exposure_score: float
    exposure_label: str
    research_context_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[EventImpactRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MacroRegimeMetadata:
    regime_id: str
    created_at_utc: str
    label: MacroRegimeMetadataLabel
    source_event_ids: List[str]
    macro_series_ids: List[str]
    confidence: EventImpactConfidence
    confidence_score: float
    description: str
    research_context_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[EventImpactRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CalendarAwareAnomaly:
    anomaly_id: str
    created_at_utc: str
    symbol: str
    anomaly_kind: CalendarAnomalyKind
    timestamp_utc: Optional[str]
    severity: str
    observed_value: Optional[float]
    expected_value: Optional[float]
    related_event_ids: List[str]
    explained_by_event: bool
    explanation_type: CalendarValidationExplanationType
    explanation: str
    research_context_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[EventImpactRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CalendarAwareValidationResult:
    validation_id: str
    created_at_utc: str
    symbol: str
    status: CalendarValidationStatus
    anomalies: List[CalendarAwareAnomaly]
    explained_anomaly_count: int
    unexplained_anomaly_count: int
    schema_error_count: int
    timestamp_error_count: int
    event_context_used: bool
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
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[EventImpactRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventImpactContext:
    context_id: str
    created_at_utc: str
    status: EventImpactStatus
    decision: EventImpactDecision
    source_event_metadata_review_id: Optional[str]
    ingestion: EventMetadataIngestionResult
    impact_tags: List[EventImpactTag]
    symbol_exposures: List[SymbolEventExposure]
    macro_regimes: List[MacroRegimeMetadata]
    calendar_validation_results: List[CalendarAwareValidationResult]
    event_impact_ready: bool
    macro_regime_metadata_ready: bool
    calendar_aware_validation_ready: bool
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
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[EventImpactRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventImpactFullReview:
    review_id: str
    created_at_utc: str
    report_type: EventImpactReportType
    ingestion: EventMetadataIngestionResult
    context: EventImpactContext
    impact_tags: List[EventImpactTag]
    symbol_exposures: List[SymbolEventExposure]
    macro_regimes: List[MacroRegimeMetadata]
    calendar_validation_results: List[CalendarAwareValidationResult]
    output_paths: Dict[str, str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_event_metadata_ingestion_id() -> str: return f"em_ingest_{uuid.uuid4().hex[:8]}"
def create_event_impact_tag_id() -> str: return f"ei_tag_{uuid.uuid4().hex[:8]}"
def create_symbol_event_exposure_id() -> str: return f"se_exp_{uuid.uuid4().hex[:8]}"
def create_macro_regime_id() -> str: return f"mr_meta_{uuid.uuid4().hex[:8]}"
def create_calendar_aware_anomaly_id() -> str: return f"ca_anom_{uuid.uuid4().hex[:8]}"
def create_calendar_aware_validation_id() -> str: return f"ca_val_{uuid.uuid4().hex[:8]}"
def create_event_impact_context_id() -> str: return f"ei_ctx_{uuid.uuid4().hex[:8]}"
def create_event_impact_full_review_id() -> str: return f"ei_rev_{uuid.uuid4().hex[:8]}"

def _to_dict(obj: Any) -> Any:
    if hasattr(obj, '__dataclass_fields__'):
        return {k: _to_dict(getattr(obj, k)) for k in obj.__dataclass_fields__}
    elif isinstance(obj, list):
        return [_to_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, 'value'):
        return obj.value
    return obj

def event_metadata_ingestion_result_to_dict(item: EventMetadataIngestionResult) -> dict: return _to_dict(item)
def event_impact_tag_to_dict(item: EventImpactTag) -> dict: return _to_dict(item)
def symbol_event_exposure_to_dict(item: SymbolEventExposure) -> dict: return _to_dict(item)
def macro_regime_metadata_to_dict(item: MacroRegimeMetadata) -> dict: return _to_dict(item)
def calendar_aware_anomaly_to_dict(item: CalendarAwareAnomaly) -> dict: return _to_dict(item)
def calendar_aware_validation_result_to_dict(item: CalendarAwareValidationResult) -> dict: return _to_dict(item)
def event_impact_context_to_dict(item: EventImpactContext) -> dict: return _to_dict(item)
def event_impact_full_review_to_dict(item: EventImpactFullReview) -> dict: return _to_dict(item)

def validate_event_metadata_ingestion_result(item: EventMetadataIngestionResult) -> None:
    if not item.metadata_only or not item.research_context_only:
        raise ValueError("Must be metadata_only and research_context_only")
    if item.produces_trade_signal or item.produces_order_decision:
        raise ValueError("Cannot produce trade signal or order decision")

def validate_event_impact_tag(item: EventImpactTag) -> None:
    if item.produces_trade_signal or item.produces_order_decision:
        raise ValueError("Tag cannot produce trade signal")
    if not (0 <= item.importance_score <= 100) or not (0 <= item.timing_score <= 100) or not (0 <= item.context_score <= 100):
        raise ValueError("Scores must be 0-100")

def validate_symbol_event_exposure(item: SymbolEventExposure) -> None:
    if item.produces_trade_signal or item.produces_order_decision:
        raise ValueError("Exposure cannot produce trade signal")

def validate_macro_regime_metadata(item: MacroRegimeMetadata) -> None:
    if item.produces_trade_signal or item.produces_order_decision:
        raise ValueError("Regime cannot produce trade signal")

def validate_calendar_aware_validation_result(item: CalendarAwareValidationResult) -> None:
    if item.produces_trade_signal or item.produces_order_decision:
        raise ValueError("Calendar validation cannot produce trade signal")
    if item.network_used or item.broker_used:
        raise ValueError("No network or broker usage allowed in calendar validation")

def validate_event_impact_context(item: EventImpactContext) -> None:
    if not item.metadata_only or not item.research_context_only:
        raise ValueError("Context must be metadata only")
    if item.produces_trade_signal or item.produces_order_decision:
        raise ValueError("Context cannot produce signals")

def validate_event_impact_full_review(item: EventImpactFullReview) -> None:
    validate_event_impact_context(item.context)
