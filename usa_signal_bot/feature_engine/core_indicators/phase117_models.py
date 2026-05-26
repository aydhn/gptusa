from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    CoreIndicatorStatus,
    CoreIndicatorDecision,
    IndicatorImplementationStatus,
    RollingWindowStatus,
    FeatureComputationQuality,
    CoreFeatureFamily,
    FeatureNullPolicy,
    CoreIndicatorRiskFlag,
    CoreIndicatorReportType
)

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

def _uuid() -> str:
    return str(uuid.uuid4())

def create_feature_foundation_ingestion_id() -> str: return f"ffing_{_uuid()}"
def create_indicator_computation_spec_id() -> str: return f"ics_{_uuid()}"
def create_rolling_window_spec_id() -> str: return f"rws_{_uuid()}"
def create_core_indicator_request_id() -> str: return f"cireq_{_uuid()}"
def create_core_indicator_result_id() -> str: return f"cires_{_uuid()}"
def create_feature_table_schema_id() -> str: return f"fts_{_uuid()}"
def create_feature_table_id() -> str: return f"ft_{_uuid()}"
def create_feature_computation_audit_id() -> str: return f"fca_{_uuid()}"
def create_core_indicator_context_id() -> str: return f"cic_{_uuid()}"
def create_core_indicator_full_review_id() -> str: return f"cifr_{_uuid()}"

def _enum_val(v):
    return v.value if hasattr(v, "value") else v

def feature_foundation_ingestion_result_to_dict(item: FeatureFoundationIngestionResult) -> dict:
    d = item.__dict__.copy()
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def indicator_computation_spec_to_dict(item: IndicatorComputationSpec) -> dict:
    d = item.__dict__.copy()
    d["feature_family"] = _enum_val(d["feature_family"])
    d["implementation_status"] = _enum_val(d["implementation_status"])
    d["null_policy"] = _enum_val(d["null_policy"])
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def rolling_window_spec_to_dict(item: RollingWindowSpec) -> dict:
    d = item.__dict__.copy()
    d["status"] = _enum_val(d["status"])
    d["null_policy"] = _enum_val(d["null_policy"])
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def core_indicator_computation_request_to_dict(item: CoreIndicatorComputationRequest) -> dict:
    d = item.__dict__.copy()
    d["feature_families"] = [_enum_val(x) for x in d["feature_families"]]
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def core_indicator_computation_result_to_dict(item: CoreIndicatorComputationResult) -> dict:
    d = item.__dict__.copy()
    d["quality"] = _enum_val(d["quality"])
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def feature_table_schema_to_dict(item: FeatureTableSchema) -> dict:
    d = item.__dict__.copy()
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def feature_table_result_to_dict(item: FeatureTableResult) -> dict:
    d = item.__dict__.copy()
    d["schema"] = feature_table_schema_to_dict(d["schema"])
    d["quality"] = _enum_val(d["quality"])
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def feature_computation_audit_to_dict(item: FeatureComputationAudit) -> dict:
    d = item.__dict__.copy()
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def core_indicator_context_to_dict(item: CoreIndicatorContext) -> dict:
    d = item.__dict__.copy()
    d["status"] = _enum_val(d["status"])
    d["decision"] = _enum_val(d["decision"])
    d["ingestion"] = feature_foundation_ingestion_result_to_dict(d["ingestion"])
    d["indicator_specs"] = [indicator_computation_spec_to_dict(x) for x in d["indicator_specs"]]
    d["rolling_specs"] = [rolling_window_spec_to_dict(x) for x in d["rolling_specs"]]
    d["requests"] = [core_indicator_computation_request_to_dict(x) for x in d["requests"]]
    d["results"] = [core_indicator_computation_result_to_dict(x) for x in d["results"]]
    d["feature_tables"] = [feature_table_result_to_dict(x) for x in d["feature_tables"]]
    d["audits"] = [feature_computation_audit_to_dict(x) for x in d["audits"]]
    d["risk_flags"] = [_enum_val(x) for x in d["risk_flags"]]
    return d

def core_indicator_full_review_to_dict(item: CoreIndicatorFullReview) -> dict:
    d = item.__dict__.copy()
    d["report_type"] = _enum_val(d["report_type"])
    d["ingestion"] = feature_foundation_ingestion_result_to_dict(d["ingestion"])
    d["context"] = core_indicator_context_to_dict(d["context"])
    d["indicator_specs"] = [indicator_computation_spec_to_dict(x) for x in d["indicator_specs"]]
    d["rolling_specs"] = [rolling_window_spec_to_dict(x) for x in d["rolling_specs"]]
    d["results"] = [core_indicator_computation_result_to_dict(x) for x in d["results"]]
    d["feature_tables"] = [feature_table_result_to_dict(x) for x in d["feature_tables"]]
    d["audits"] = [feature_computation_audit_to_dict(x) for x in d["audits"]]
    return d

def validate_feature_foundation_ingestion_result(item: FeatureFoundationIngestionResult) -> None:
    if not item.feature_foundation_ready:
        item.errors.append("feature_foundation_ready must be True")
    if not item.ready_for_phase117:
        item.errors.append("ready_for_phase117 must be True")
    if not item.metadata_only or not item.research_data_only:
        item.errors.append("metadata_only and research_data_only must be True")
    if item.activation_allowed or item.active_paper_enabled or item.broker_execution_enabled or item.order_creation_enabled or item.paper_state_mutation_enabled:
        item.errors.append("Execution enablements must be False")
    if item.telegram_real_send_enabled or item.scraping_enabled or item.html_parse_enabled or item.paid_api_enabled or item.dashboard_enabled or item.network_default_enabled:
        item.errors.append("External integrations must be disabled")
    if item.produces_trade_signal or item.produces_order_decision:
        item.errors.append("produces_trade_signal and produces_order_decision must be False")

def validate_indicator_computation_spec(item: IndicatorComputationSpec) -> None:
    if item.requires_network or item.requires_paid_api or item.requires_scraping:
        item.errors.append("Specs cannot require network, paid API, or scraping")
    if item.produces_trade_signal or item.produces_order_decision:
        item.errors.append("produces_trade_signal and produces_order_decision must be False")

def validate_rolling_window_spec(item: RollingWindowSpec) -> None:
    pass

def validate_core_indicator_computation_request(item: CoreIndicatorComputationRequest) -> None:
    if item.allow_network:
        item.errors.append("allow_network must be False")

def validate_core_indicator_computation_result(item: CoreIndicatorComputationResult) -> None:
    if item.produced_trade_signal or item.produced_order_decision:
        item.errors.append("produced_trade_signal and produced_order_decision must be False")

def validate_feature_table_schema(item: FeatureTableSchema) -> None:
    if item.blocked_columns:
        item.errors.append("blocked_columns must be empty")

def validate_feature_table_result(item: FeatureTableResult) -> None:
    validate_feature_table_schema(item.schema)
    if item.schema.errors:
        item.errors.extend(item.schema.errors)

def validate_feature_computation_audit(item: FeatureComputationAudit) -> None:
    if not (item.no_network and item.no_broker and item.no_order and item.no_paper_mutation and item.no_trade_signal):
        item.errors.append("Audit must assert no_network, no_broker, no_order, no_paper_mutation, and no_trade_signal are True")

def validate_core_indicator_context(item: CoreIndicatorContext) -> None:
    if item.activation_allowed or item.active_paper_enabled or item.broker_execution_enabled:
        item.errors.append("Context activation and execution must be False")

def validate_core_indicator_full_review(item: CoreIndicatorFullReview) -> None:
    validate_core_indicator_context(item.context)
    if item.context.errors:
        item.errors.extend(item.context.errors)
