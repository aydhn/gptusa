from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
from usa_signal_bot.core.enums import (
    AdvancedFeatureStatus,
    AdvancedFeatureDecision,
    AdvancedFeatureFamily,
    NormalizationMethod,
    CrossSectionalUniverseStatus,
    CrossSectionalAlignmentStatus,
    AdvancedFeatureQuality,
    AdvancedFeatureRiskFlag,
    AdvancedFeatureReportType
)
import uuid
import datetime

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class CoreIndicatorIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
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
    valid_for_phase118: bool
    risk_flags: List[AdvancedFeatureRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class AdvancedFeatureSpec:
    spec_id: str
    created_at_utc: str
    feature_name: str
    family: AdvancedFeatureFamily
    normalization_method: NormalizationMethod
    input_columns: List[str]
    output_columns: List[str]
    parameters: Dict[str, Any]
    min_required_rows: int
    min_required_symbols: int
    local_pandas_only: bool
    cross_sectional: bool
    requires_network: bool
    requires_paid_api: bool
    requires_scraping: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CrossSectionalUniverse:
    universe_id: str
    created_at_utc: str
    name: str
    symbols: List[str]
    min_required_symbols: int
    status: CrossSectionalUniverseStatus
    research_data_only: bool
    contains_benchmark_symbol: bool
    benchmark_symbol: Optional[str]
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CrossSectionalAlignmentResult:
    alignment_id: str
    created_at_utc: str
    universe_id: Optional[str]
    symbols: List[str]
    aligned_timestamps: List[str]
    input_table_count: int
    aligned_table_count: int
    missing_symbol_count: int
    timestamp_mismatch_count: int
    status: CrossSectionalAlignmentStatus
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NormalizationResult:
    normalization_id: str
    created_at_utc: str
    method: NormalizationMethod
    input_column: str
    output_column: str
    row_count: int
    null_count: int
    finite_value_count: int
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AdvancedFeatureComputationRequest:
    request_id: str
    created_at_utc: str
    symbols: List[str]
    feature_names: List[str]
    families: List[AdvancedFeatureFamily]
    input_paths: Dict[str, str]
    compute_cross_sectional: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AdvancedFeatureComputationResult:
    result_id: str
    created_at_utc: str
    request_id: Optional[str]
    symbols: List[str]
    computed_feature_columns: List[str]
    computed_family_counts: Dict[str, int]
    input_rows_by_symbol: Dict[str, int]
    output_rows_by_symbol: Dict[str, int]
    normalization_results: List[NormalizationResult]
    cross_sectional_alignment: Optional[CrossSectionalAlignmentResult]
    quality: AdvancedFeatureQuality
    output_paths: Dict[str, str]
    metadata_only: bool
    dry_run_only: bool
    research_data_only: bool
    computed_values: bool
    produced_trade_signal: bool
    produced_order_decision: bool
    produced_portfolio_weights: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AdvancedFeatureTableResult:
    table_id: str
    created_at_utc: str
    symbol: str
    rows: int
    columns: List[str]
    advanced_feature_columns: List[str]
    cross_sectional_columns: List[str]
    feature_family_counts: Dict[str, int]
    null_summary: Dict[str, Any]
    quality: AdvancedFeatureQuality
    output_path: Optional[str]
    metadata_only: bool
    research_data_only: bool
    produced_trade_signal: bool
    produced_order_decision: bool
    produced_portfolio_weights: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AdvancedFeatureAudit:
    audit_id: str
    created_at_utc: str
    symbols: List[str]
    input_hashes: Dict[str, str]
    output_hashes: Dict[str, str]
    advanced_feature_column_count: int
    cross_sectional_feature_column_count: int
    computation_deterministic: bool
    local_only: bool
    no_network: bool
    no_broker: bool
    no_order: bool
    no_paper_mutation: bool
    no_trade_signal: bool
    no_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AdvancedFeatureContext:
    context_id: str
    created_at_utc: str
    status: AdvancedFeatureStatus
    decision: AdvancedFeatureDecision
    source_core_indicator_review_id: Optional[str]
    ingestion: CoreIndicatorIngestionResult
    specs: List[AdvancedFeatureSpec]
    universe: CrossSectionalUniverse
    requests: List[AdvancedFeatureComputationRequest]
    results: List[AdvancedFeatureComputationResult]
    feature_tables: List[AdvancedFeatureTableResult]
    audits: List[AdvancedFeatureAudit]
    advanced_features_ready: bool
    cross_sectional_features_ready: bool
    multi_symbol_feature_table_ready: bool
    ready_for_phase119: bool
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
    produces_portfolio_weights: bool
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
    risk_flags: List[AdvancedFeatureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AdvancedFeatureFullReview:
    review_id: str
    created_at_utc: str
    report_type: AdvancedFeatureReportType
    ingestion: CoreIndicatorIngestionResult
    context: AdvancedFeatureContext
    specs: List[AdvancedFeatureSpec]
    universe: CrossSectionalUniverse
    results: List[AdvancedFeatureComputationResult]
    feature_tables: List[AdvancedFeatureTableResult]
    audits: List[AdvancedFeatureAudit]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]


# ID Generators
def create_core_indicator_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:8]}"

def create_advanced_feature_spec_id() -> str:
    return f"spec_{uuid.uuid4().hex[:8]}"

def create_cross_sectional_universe_id() -> str:
    return f"univ_{uuid.uuid4().hex[:8]}"

def create_cross_sectional_alignment_id() -> str:
    return f"align_{uuid.uuid4().hex[:8]}"

def create_normalization_result_id() -> str:
    return f"norm_{uuid.uuid4().hex[:8]}"

def create_advanced_feature_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:8]}"

def create_advanced_feature_result_id() -> str:
    return f"res_{uuid.uuid4().hex[:8]}"

def create_advanced_feature_table_id() -> str:
    return f"tbl_{uuid.uuid4().hex[:8]}"

def create_advanced_feature_audit_id() -> str:
    return f"audit_{uuid.uuid4().hex[:8]}"

def create_advanced_feature_context_id() -> str:
    return f"ctx_{uuid.uuid4().hex[:8]}"

def create_advanced_feature_full_review_id() -> str:
    return f"rev_{uuid.uuid4().hex[:8]}"

# Dict Conversions
from dataclasses import asdict

def core_indicator_ingestion_result_to_dict(item: CoreIndicatorIngestionResult) -> dict:
    return asdict(item)
def advanced_feature_spec_to_dict(item: AdvancedFeatureSpec) -> dict:
    return asdict(item)
def cross_sectional_universe_to_dict(item: CrossSectionalUniverse) -> dict:
    return asdict(item)
def cross_sectional_alignment_result_to_dict(item: CrossSectionalAlignmentResult) -> dict:
    return asdict(item)
def normalization_result_to_dict(item: NormalizationResult) -> dict:
    return asdict(item)
def advanced_feature_computation_request_to_dict(item: AdvancedFeatureComputationRequest) -> dict:
    return asdict(item)
def advanced_feature_computation_result_to_dict(item: AdvancedFeatureComputationResult) -> dict:
    return asdict(item)
def advanced_feature_table_result_to_dict(item: AdvancedFeatureTableResult) -> dict:
    return asdict(item)
def advanced_feature_audit_to_dict(item: AdvancedFeatureAudit) -> dict:
    return asdict(item)
def advanced_feature_context_to_dict(item: AdvancedFeatureContext) -> dict:
    return asdict(item)
def advanced_feature_full_review_to_dict(item: AdvancedFeatureFullReview) -> dict:
    return asdict(item)

# Validators (Simple wrappers around logic from prompts)
from usa_signal_bot.core.exceptions import AdvancedFeatureValidationError

def validate_core_indicator_ingestion_result(item: CoreIndicatorIngestionResult) -> None:
    if not item.core_indicators_ready:
        raise AdvancedFeatureValidationError("core_indicators_ready must be True")
    if not item.feature_table_ready:
        raise AdvancedFeatureValidationError("feature_table_ready must be True")
    if not item.ready_for_phase118:
        raise AdvancedFeatureValidationError("ready_for_phase118 must be True")
    if not item.research_data_only:
        raise AdvancedFeatureValidationError("research_data_only must be True")

    if item.activation_allowed:
        raise AdvancedFeatureValidationError("activation_allowed must be False")
    if item.active_paper_enabled:
        raise AdvancedFeatureValidationError("active_paper_enabled must be False")
    if item.broker_execution_enabled:
        raise AdvancedFeatureValidationError("broker_execution_enabled must be False")
    if item.order_creation_enabled:
        raise AdvancedFeatureValidationError("order_creation_enabled must be False")
    if item.paper_state_mutation_enabled:
        raise AdvancedFeatureValidationError("paper_state_mutation_enabled must be False")
    if item.telegram_real_send_enabled:
        raise AdvancedFeatureValidationError("telegram_real_send_enabled must be False")
    if item.scraping_enabled:
        raise AdvancedFeatureValidationError("scraping_enabled must be False")
    if item.html_parse_enabled:
        raise AdvancedFeatureValidationError("html_parse_enabled must be False")
    if item.paid_api_enabled:
        raise AdvancedFeatureValidationError("paid_api_enabled must be False")
    if item.dashboard_enabled:
        raise AdvancedFeatureValidationError("dashboard_enabled must be False")
    if item.network_default_enabled:
        raise AdvancedFeatureValidationError("network_default_enabled must be False")
    if item.produces_trade_signal:
        raise AdvancedFeatureValidationError("produces_trade_signal must be False")
    if item.produces_order_decision:
        raise AdvancedFeatureValidationError("produces_order_decision must be False")

    if item.network_used:
        raise AdvancedFeatureValidationError("network_used must be False")
    if item.paid_api_used:
        raise AdvancedFeatureValidationError("paid_api_used must be False")
    if item.scraping_used:
        raise AdvancedFeatureValidationError("scraping_used must be False")
    if item.html_parsing_used:
        raise AdvancedFeatureValidationError("html_parsing_used must be False")
    if item.broker_used:
        raise AdvancedFeatureValidationError("broker_used must be False")
    if item.order_created:
        raise AdvancedFeatureValidationError("order_created must be False")
    if item.paper_state_mutated:
        raise AdvancedFeatureValidationError("paper_state_mutated must be False")
    if item.telegram_real_sent:
        raise AdvancedFeatureValidationError("telegram_real_sent must be False")
    if item.dashboard_started:
        raise AdvancedFeatureValidationError("dashboard_started must be False")

def validate_advanced_feature_spec(item: AdvancedFeatureSpec) -> None:
    if item.requires_network:
        raise AdvancedFeatureValidationError("requires_network must be False")
    if item.requires_paid_api:
        raise AdvancedFeatureValidationError("requires_paid_api must be False")
    if item.requires_scraping:
        raise AdvancedFeatureValidationError("requires_scraping must be False")

def validate_cross_sectional_universe(item: CrossSectionalUniverse) -> None:
    pass

def validate_cross_sectional_alignment_result(item: CrossSectionalAlignmentResult) -> None:
    pass

def validate_normalization_result(item: NormalizationResult) -> None:
    pass

def validate_advanced_feature_computation_request(item: AdvancedFeatureComputationRequest) -> None:
    if item.allow_network:
        raise AdvancedFeatureValidationError("allow_network must be False")

def validate_advanced_feature_computation_result(item: AdvancedFeatureComputationResult) -> None:
    if item.produced_trade_signal:
        raise AdvancedFeatureValidationError("produced_trade_signal must be False")
    if item.produced_order_decision:
        raise AdvancedFeatureValidationError("produced_order_decision must be False")
    if item.produced_portfolio_weights:
        raise AdvancedFeatureValidationError("produced_portfolio_weights must be False")

def validate_advanced_feature_table_result(item: AdvancedFeatureTableResult) -> None:
    pass

def validate_advanced_feature_audit(item: AdvancedFeatureAudit) -> None:
    if not item.no_network:
        raise AdvancedFeatureValidationError("no_network must be True")
    if not item.no_broker:
        raise AdvancedFeatureValidationError("no_broker must be True")
    if not item.no_order:
        raise AdvancedFeatureValidationError("no_order must be True")
    if not item.no_paper_mutation:
        raise AdvancedFeatureValidationError("no_paper_mutation must be True")
    if not item.no_trade_signal:
        raise AdvancedFeatureValidationError("no_trade_signal must be True")
    if not item.no_portfolio_weights:
        raise AdvancedFeatureValidationError("no_portfolio_weights must be True")

def validate_advanced_feature_context(item: AdvancedFeatureContext) -> None:
    pass

def validate_advanced_feature_full_review(item: AdvancedFeatureFullReview) -> None:
    pass
