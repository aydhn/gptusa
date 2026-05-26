from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import *

@dataclass
class FeatureFoundationIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    feature_foundation_ready: bool
    indicator_registry_ready: bool
    feature_registry_ready: bool
    factor_registry_ready: bool
    input_contract_ready: bool
    output_schema_ready: bool
    ready_for_phase117: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
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
    valid_for_phase117: bool
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class IndicatorComputationSpec:
    spec_id: str
    created_at_utc: str
    indicator_name: str
    feature_family: CoreFeatureFamily
    implementation_status: IndicatorImplementationStatus
    input_columns: List[str]
    output_columns: List[str]
    parameters: Dict[str, Any]
    min_required_rows: int
    warmup_rows: int
    null_policy: FeatureNullPolicy
    local_pandas_only: bool
    requires_network: bool
    requires_paid_api: bool
    requires_scraping: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RollingWindowSpec:
    rolling_spec_id: str
    created_at_utc: str
    name: str
    window: int
    min_periods: int
    input_column: str
    output_column: str
    operation: str
    status: RollingWindowStatus
    null_policy: FeatureNullPolicy
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreIndicatorComputationRequest:
    request_id: str
    created_at_utc: str
    symbol: str
    indicator_names: List[str]
    feature_families: List[CoreFeatureFamily]
    input_path: Optional[str]
    input_rows: Optional[int]
    metadata_only: bool
    dry_run_only: bool
    research_data_only: bool
    compute_values: bool
    allow_network: bool
    allow_paid_api: bool
    allow_scraping: bool
    allow_html_parsing: bool
    allow_broker: bool
    allow_order: bool
    allow_paper_mutation: bool
    allow_telegram_real_send: bool
    allow_dashboard: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreIndicatorComputationResult:
    result_id: str
    created_at_utc: str
    request_id: Optional[str]
    symbol: str
    computed_indicator_names: List[str]
    computed_feature_columns: List[str]
    input_rows: int
    output_rows: int
    warmup_null_count: int
    total_null_count: int
    quality: FeatureComputationQuality
    feature_table_path: Optional[str]
    metadata_only: bool
    dry_run_only: bool
    research_data_only: bool
    computed_values: bool
    produced_trade_signal: bool
    produced_order_decision: bool
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
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureTableSchema:
    schema_id: str
    created_at_utc: str
    required_base_columns: List[str]
    feature_columns: List[str]
    blocked_columns: List[str]
    symbol_column: str
    timestamp_column: str
    schema_valid: bool
    trade_signal_columns_present: bool
    order_decision_columns_present: bool
    broker_columns_present: bool
    paper_mutation_columns_present: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureTableResult:
    table_id: str
    created_at_utc: str
    symbol: str
    schema: FeatureTableSchema
    rows: int
    columns: List[str]
    feature_columns: List[str]
    feature_family_counts: Dict[str, int]
    null_summary: Dict[str, Any]
    quality: FeatureComputationQuality
    output_path: Optional[str]
    metadata_only: bool
    research_data_only: bool
    produced_trade_signal: bool
    produced_order_decision: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureComputationAudit:
    audit_id: str
    created_at_utc: str
    symbol: str
    input_hash: Optional[str]
    output_hash: Optional[str]
    indicator_count: int
    feature_column_count: int
    computation_deterministic: bool
    local_only: bool
    no_network: bool
    no_broker: bool
    no_order: bool
    no_paper_mutation: bool
    no_trade_signal: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreIndicatorContext:
    context_id: str
    created_at_utc: str
    status: CoreIndicatorStatus
    decision: CoreIndicatorDecision
    source_feature_foundation_review_id: Optional[str]
    ingestion: FeatureFoundationIngestionResult
    indicator_specs: List[IndicatorComputationSpec]
    rolling_specs: List[RollingWindowSpec]
    requests: List[CoreIndicatorComputationRequest]
    results: List[CoreIndicatorComputationResult]
    feature_tables: List[FeatureTableResult]
    audits: List[FeatureComputationAudit]
    core_indicators_ready: bool
    rolling_window_engine_ready: bool
    feature_table_ready: bool
    ready_for_phase118: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
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
    risk_flags: List[CoreIndicatorRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreIndicatorFullReview:
    review_id: str
    created_at_utc: str
    report_type: CoreIndicatorReportType
    ingestion: FeatureFoundationIngestionResult
    context: CoreIndicatorContext
    indicator_specs: List[IndicatorComputationSpec]
    rolling_specs: List[RollingWindowSpec]
    results: List[CoreIndicatorComputationResult]
    feature_tables: List[FeatureTableResult]
    audits: List[FeatureComputationAudit]
    output_paths: Dict[str, str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _dt() -> str: return datetime.now(timezone.utc).isoformat()
def _id(prefix) -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_feature_foundation_ingestion_id() -> str: return _id("ingest")
def create_indicator_computation_spec_id() -> str: return _id("ind_spec")
def create_rolling_window_spec_id() -> str: return _id("rw_spec")
def create_core_indicator_request_id() -> str: return _id("req")
def create_core_indicator_result_id() -> str: return _id("res")
def create_feature_table_schema_id() -> str: return _id("fts")
def create_feature_table_id() -> str: return _id("ft")
def create_feature_computation_audit_id() -> str: return _id("audit")
def create_core_indicator_context_id() -> str: return _id("ctx")
def create_core_indicator_full_review_id() -> str: return _id("rev")

def feature_foundation_ingestion_result_to_dict(item: FeatureFoundationIngestionResult) -> dict: return asdict(item)
def indicator_computation_spec_to_dict(item: IndicatorComputationSpec) -> dict: return asdict(item)
def rolling_window_spec_to_dict(item: RollingWindowSpec) -> dict: return asdict(item)
def core_indicator_computation_request_to_dict(item: CoreIndicatorComputationRequest) -> dict: return asdict(item)
def core_indicator_computation_result_to_dict(item: CoreIndicatorComputationResult) -> dict: return asdict(item)
def feature_table_schema_to_dict(item: FeatureTableSchema) -> dict: return asdict(item)
def feature_table_result_to_dict(item: FeatureTableResult) -> dict: return asdict(item)
def feature_computation_audit_to_dict(item: FeatureComputationAudit) -> dict: return asdict(item)
def core_indicator_context_to_dict(item: CoreIndicatorContext) -> dict: return asdict(item)
def core_indicator_full_review_to_dict(item: CoreIndicatorFullReview) -> dict: return asdict(item)

def validate_feature_foundation_ingestion_result(item: FeatureFoundationIngestionResult) -> None:
    if not item.feature_foundation_ready: raise Exception("feature_foundation_ready must be True")
    if not item.ready_for_phase117: raise Exception("ready_for_phase117 must be True")
    if not item.metadata_only: raise Exception("metadata_only must be True")
    if not item.research_data_only: raise Exception("research_data_only must be True")
    if item.activation_allowed: raise Exception("activation_allowed must be False")
    if item.active_paper_enabled: raise Exception("active_paper_enabled must be False")
    if item.broker_execution_enabled: raise Exception("broker_execution_enabled must be False")
    if item.order_creation_enabled: raise Exception("order_creation_enabled must be False")
    if item.paper_state_mutation_enabled: raise Exception("paper_state_mutation_enabled must be False")

def validate_indicator_computation_spec(item: IndicatorComputationSpec) -> None:
    if item.requires_network or item.requires_paid_api or item.requires_scraping:
        raise Exception("Requires network/api/scraping must be False")

def validate_rolling_window_spec(item: RollingWindowSpec) -> None: pass
def validate_core_indicator_computation_request(item: CoreIndicatorComputationRequest) -> None:
    if item.allow_network: raise Exception("allow_network must be False")
def validate_core_indicator_computation_result(item: CoreIndicatorComputationResult) -> None:
    if item.produced_trade_signal: raise Exception("produced_trade_signal must be False")
    if item.produced_order_decision: raise Exception("produced_order_decision must be False")
def validate_feature_table_schema(item: FeatureTableSchema) -> None: pass
def validate_feature_table_result(item: FeatureTableResult) -> None: pass
def validate_feature_computation_audit(item: FeatureComputationAudit) -> None:
    if not item.no_network or not item.no_broker or not item.no_order or not item.no_paper_mutation or not item.no_trade_signal:
        raise Exception("Audit flags must be True for no_network, no_broker, no_order, etc.")
def validate_core_indicator_context(item: CoreIndicatorContext) -> None: pass
def validate_core_indicator_full_review(item: CoreIndicatorFullReview) -> None: pass
