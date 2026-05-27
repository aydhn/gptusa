from dataclasses import dataclass, field
from typing import Any
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    FactorScoringStatus,
    FactorScoringDecision,
    FactorScoreKind,
    FactorNormalizationMethod,
    FactorDiagnosticsKind,
    FactorTableStatus,
    FactorScoreQuality,
    FactorOutputKind,
    FactorBlockedOutputKind,
    FactorScoringRiskFlag,
    FactorScoringReportType
)

@dataclass
class FactorCompositionIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    feature_groups_ready: bool
    factor_candidates_ready: bool
    selection_metadata_ready: bool
    factor_readiness_gate_ready: bool
    ready_for_phase121: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
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
    valid_for_phase121: bool
    risk_flags: list[FactorScoringRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class FactorScoringSpec:
    spec_id: str
    created_at_utc: str
    factor_name: str
    score_kind: FactorScoreKind
    input_feature_columns: list[str]
    output_raw_column: str
    output_normalized_column: str
    output_percentile_column: str
    output_rank_column: str
    component_weights: dict[str, float]
    normalization_method: FactorNormalizationMethod
    min_required_rows: int
    min_required_symbols: int
    local_pandas_only: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorScoringRequest:
    request_id: str
    created_at_utc: str
    symbols: list[str]
    factor_names: list[str]
    input_paths: dict[str, str]
    compute_cross_sectional: bool
    compute_diagnostics: bool
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
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorNormalizationResult:
    normalization_id: str
    created_at_utc: str
    symbol: str | None
    factor_name: str
    method: FactorNormalizationMethod
    input_column: str
    output_column: str
    row_count: int
    null_count: int
    finite_value_count: int
    min_value: float | None
    max_value: float | None
    mean_value: float | None
    std_value: float | None
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorDiagnosticsProfile:
    diagnostics_id: str
    created_at_utc: str
    symbol: str | None
    factor_name: str
    diagnostics_kinds: list[FactorDiagnosticsKind]
    row_count: int
    coverage_ratio: float
    missingness_ratio: float
    finite_ratio: float
    outlier_ratio: float
    stability_score: float
    correlation_warnings: list[dict[str, Any]]
    redundancy_score: float
    distribution_summary: dict[str, Any]
    quality: FactorScoreQuality
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorScoringResult:
    result_id: str
    created_at_utc: str
    request_id: str | None
    symbols: list[str]
    factor_names: list[str]
    factor_columns: list[str]
    raw_factor_columns: list[str]
    normalized_factor_columns: list[str]
    percentile_factor_columns: list[str]
    rank_factor_columns: list[str]
    normalization_results: list[FactorNormalizationResult]
    diagnostics_profiles: list[FactorDiagnosticsProfile]
    quality: FactorScoreQuality
    output_paths: dict[str, str]
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
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorTableSchema:
    schema_id: str
    created_at_utc: str
    required_base_columns: list[str]
    factor_columns: list[str]
    allowed_output_kinds: list[FactorOutputKind]
    blocked_output_kinds: list[FactorBlockedOutputKind]
    symbol_column: str
    timestamp_column: str
    schema_valid: bool
    trade_signal_columns_present: bool
    order_decision_columns_present: bool
    portfolio_weight_columns_present: bool
    broker_columns_present: bool
    paper_mutation_columns_present: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorTableResult:
    table_id: str
    created_at_utc: str
    symbol: str
    rows: int
    columns: list[str]
    factor_columns: list[str]
    raw_factor_columns: list[str]
    normalized_factor_columns: list[str]
    percentile_factor_columns: list[str]
    rank_factor_columns: list[str]
    diagnostics_columns: list[str]
    null_summary: dict[str, Any]
    quality: FactorScoreQuality
    schema: FactorTableSchema
    output_path: str | None
    research_data_only: bool
    produced_trade_signal: bool
    produced_order_decision: bool
    produced_portfolio_weights: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorComputationAudit:
    audit_id: str
    created_at_utc: str
    symbols: list[str]
    input_hashes: dict[str, str]
    output_hashes: dict[str, str]
    factor_count: int
    factor_column_count: int
    computation_deterministic: bool
    local_only: bool
    no_network: bool
    no_broker: bool
    no_order: bool
    no_paper_mutation: bool
    no_trade_signal: bool
    no_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorScoringContext:
    context_id: str
    created_at_utc: str
    status: FactorScoringStatus
    decision: FactorScoringDecision
    source_factor_composition_review_id: str | None
    ingestion: FactorCompositionIngestionResult
    scoring_specs: list[FactorScoringSpec]
    requests: list[FactorScoringRequest]
    results: list[FactorScoringResult]
    factor_tables: list[FactorTableResult]
    diagnostics_profiles: list[FactorDiagnosticsProfile]
    audits: list[FactorComputationAudit]
    factor_scoring_ready: bool
    factor_normalization_ready: bool
    factor_diagnostics_ready: bool
    factor_table_ready: bool
    ready_for_phase122: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
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
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorScoringRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorScoringFullReview:
    review_id: str
    created_at_utc: str
    report_type: FactorScoringReportType
    ingestion: FactorCompositionIngestionResult
    context: FactorScoringContext
    scoring_specs: list[FactorScoringSpec]
    results: list[FactorScoringResult]
    factor_tables: list[FactorTableResult]
    diagnostics_profiles: list[FactorDiagnosticsProfile]
    audits: list[FactorComputationAudit]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]


def create_factor_composition_ingestion_id() -> str:
    return f"factor-comp-ingest-{uuid.uuid4().hex[:8]}"

def create_factor_scoring_spec_id() -> str:
    return f"factor-spec-{uuid.uuid4().hex[:8]}"

def create_factor_scoring_request_id() -> str:
    return f"factor-req-{uuid.uuid4().hex[:8]}"

def create_factor_normalization_result_id() -> str:
    return f"factor-norm-{uuid.uuid4().hex[:8]}"

def create_factor_diagnostics_profile_id() -> str:
    return f"factor-diag-{uuid.uuid4().hex[:8]}"

def create_factor_scoring_result_id() -> str:
    return f"factor-result-{uuid.uuid4().hex[:8]}"

def create_factor_table_schema_id() -> str:
    return f"factor-schema-{uuid.uuid4().hex[:8]}"

def create_factor_table_id() -> str:
    return f"factor-table-{uuid.uuid4().hex[:8]}"

def create_factor_computation_audit_id() -> str:
    return f"factor-audit-{uuid.uuid4().hex[:8]}"

def create_factor_scoring_context_id() -> str:
    return f"factor-context-{uuid.uuid4().hex[:8]}"

def create_factor_scoring_full_review_id() -> str:
    return f"factor-review-{uuid.uuid4().hex[:8]}"


from usa_signal_bot.core.serialization import dataclass_to_dict

def factor_composition_ingestion_result_to_dict(item: FactorCompositionIngestionResult) -> dict:
    return dataclass_to_dict(item)

def factor_scoring_spec_to_dict(item: FactorScoringSpec) -> dict:
    return dataclass_to_dict(item)

def factor_scoring_request_to_dict(item: FactorScoringRequest) -> dict:
    return dataclass_to_dict(item)

def factor_normalization_result_to_dict(item: FactorNormalizationResult) -> dict:
    return dataclass_to_dict(item)

def factor_diagnostics_profile_to_dict(item: FactorDiagnosticsProfile) -> dict:
    return dataclass_to_dict(item)

def factor_scoring_result_to_dict(item: FactorScoringResult) -> dict:
    return dataclass_to_dict(item)

def factor_table_schema_to_dict(item: FactorTableSchema) -> dict:
    return dataclass_to_dict(item)

def factor_table_result_to_dict(item: FactorTableResult) -> dict:
    return dataclass_to_dict(item)

def factor_computation_audit_to_dict(item: FactorComputationAudit) -> dict:
    return dataclass_to_dict(item)

def factor_scoring_context_to_dict(item: FactorScoringContext) -> dict:
    return dataclass_to_dict(item)

def factor_scoring_full_review_to_dict(item: FactorScoringFullReview) -> dict:
    return dataclass_to_dict(item)

from usa_signal_bot.core.exceptions import FactorComputationValidationError

def validate_factor_composition_ingestion_result(item: FactorCompositionIngestionResult) -> None:
    if not item.factor_readiness_gate_ready:
        item.valid_for_phase121 = False
    if not item.ready_for_phase121:
        item.valid_for_phase121 = False
    if not item.research_data_only:
        item.valid_for_phase121 = False
    if item.activation_allowed or item.strategy_activation_allowed or item.active_paper_enabled:
        item.valid_for_phase121 = False
    if item.broker_execution_enabled or item.order_creation_enabled or item.paper_state_mutation_enabled:
        item.valid_for_phase121 = False
    if item.telegram_real_send_enabled or item.scraping_enabled or item.html_parse_enabled or item.paid_api_enabled:
        item.valid_for_phase121 = False
    if item.dashboard_enabled or item.network_default_enabled:
        item.valid_for_phase121 = False
    if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
        item.valid_for_phase121 = False
    if item.network_used or item.paid_api_used or item.scraping_used or item.html_parsing_used:
        item.valid_for_phase121 = False
    if item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.dashboard_started:
        item.valid_for_phase121 = False

def validate_factor_scoring_spec(item: FactorScoringSpec) -> None:
    if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
        raise FactorComputationValidationError("Spec produces execution language")

def validate_factor_scoring_request(item: FactorScoringRequest) -> None:
    if item.allow_network or item.allow_paid_api or item.allow_scraping or item.allow_html_parsing:
        raise FactorComputationValidationError("Request allows external calls")
    if item.allow_broker or item.allow_order or item.allow_paper_mutation or item.allow_telegram_real_send or item.allow_dashboard:
        raise FactorComputationValidationError("Request allows execution")

def validate_factor_normalization_result(item: FactorNormalizationResult) -> None:
    pass

def validate_factor_diagnostics_profile(item: FactorDiagnosticsProfile) -> None:
    pass

def validate_factor_scoring_result(item: FactorScoringResult) -> None:
    if item.produced_trade_signal or item.produced_order_decision or item.produced_portfolio_weights:
         raise FactorComputationValidationError("Result produced execution items")

def validate_factor_table_schema(item: FactorTableSchema) -> None:
    if item.trade_signal_columns_present or item.order_decision_columns_present or item.portfolio_weight_columns_present:
         raise FactorComputationValidationError("Schema contains execution columns")

def validate_factor_table_result(item: FactorTableResult) -> None:
    if item.produced_trade_signal or item.produced_order_decision or item.produced_portfolio_weights:
         raise FactorComputationValidationError("Table produced execution items")

def validate_factor_computation_audit(item: FactorComputationAudit) -> None:
    if not item.no_network or not item.no_broker or not item.no_order or not item.no_paper_mutation:
        raise FactorComputationValidationError("Audit failed execution guard")

def validate_factor_scoring_context(item: FactorScoringContext) -> None:
    if not item.research_data_only or item.activation_allowed:
        raise FactorComputationValidationError("Context failed safety")

def validate_factor_scoring_full_review(item: FactorScoringFullReview) -> None:
    pass
