import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, Optional

from usa_signal_bot.core.enums import (
    FeatureFoundationStatus,
    FeatureFoundationDecision,
    IndicatorCategory,
    FeatureCategory,
    FactorCategory,
    FeatureDataType,
    FeatureComputationMode,
    FeatureOutputKind,
    FeatureBlockedOutputKind,
    FeatureFoundationRiskFlag,
    FeatureFoundationReportType
)

def create_feature_factor_kickoff_ingestion_id() -> str:
    return f"kickoff_ingest_{uuid.uuid4().hex[:12]}"

def create_indicator_definition_id() -> str:
    return f"ind_def_{uuid.uuid4().hex[:12]}"

def create_feature_definition_id() -> str:
    return f"feat_def_{uuid.uuid4().hex[:12]}"

def create_factor_definition_id() -> str:
    return f"fact_def_{uuid.uuid4().hex[:12]}"

def create_feature_input_contract_id() -> str:
    return f"feat_in_contract_{uuid.uuid4().hex[:12]}"

def create_feature_output_schema_id() -> str:
    return f"feat_out_schema_{uuid.uuid4().hex[:12]}"

def create_feature_computation_request_id() -> str:
    return f"feat_req_{uuid.uuid4().hex[:12]}"

def create_feature_computation_result_id() -> str:
    return f"feat_res_{uuid.uuid4().hex[:12]}"

def create_feature_registry_id() -> str:
    return f"feat_reg_{uuid.uuid4().hex[:12]}"

def create_feature_foundation_context_id() -> str:
    return f"feat_ctx_{uuid.uuid4().hex[:12]}"

def create_feature_foundation_full_review_id() -> str:
    return f"feat_rev_{uuid.uuid4().hex[:12]}"

@dataclass
class FeatureFactorKickoffIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_gate_id: str | None
    source_review_id: str | None
    available: bool
    ready_for_phase116: bool
    phase116_scope_allowed: bool
    metadata_only: bool
    research_data_only: bool
    sealed: bool
    immutable: bool
    frozen: bool
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
    valid_for_phase116: bool
    risk_flags: list[FeatureFoundationRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class IndicatorDefinition:
    indicator_id: str
    created_at_utc: str
    name: str
    category: IndicatorCategory
    description: str
    input_columns: list[str]
    output_columns: list[str]
    parameters: dict[str, Any]
    computation_mode: FeatureComputationMode
    requires_network: bool
    requires_paid_api: bool
    requires_scraping: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    enabled_for_phase116: bool
    implementation_phase: int | None
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureDefinition:
    feature_id: str
    created_at_utc: str
    name: str
    category: FeatureCategory
    data_type: FeatureDataType
    description: str
    input_columns: list[str]
    output_column: str
    source_indicator_id: str | None
    nullable: bool
    default_value: Any | None
    computation_mode: FeatureComputationMode
    lineage_required: bool
    validation_rules: list[str]
    produces_trade_signal: bool
    produces_order_decision: bool
    enabled_for_phase116: bool
    implementation_phase: int | None
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorDefinition:
    factor_id: str
    created_at_utc: str
    name: str
    category: FactorCategory
    description: str
    input_features: list[str]
    output_column: str
    factor_direction: str
    computation_mode: FeatureComputationMode
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    enabled_for_phase116: bool
    implementation_phase: int | None
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureInputContract:
    contract_id: str
    created_at_utc: str
    allowed_input_kinds: list[str]
    required_ohlcv_columns: list[str]
    optional_metadata_inputs: list[str]
    event_context_allowed: bool
    quality_metadata_allowed: bool
    calendar_metadata_allowed: bool
    lineage_metadata_required: bool
    metadata_only_required: bool
    research_data_only_required: bool
    network_allowed: bool
    paid_api_allowed: bool
    scraping_allowed: bool
    html_parsing_allowed: bool
    broker_allowed: bool
    order_allowed: bool
    paper_mutation_allowed: bool
    telegram_real_send_allowed: bool
    dashboard_allowed: bool
    contract_valid: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureOutputSchema:
    schema_id: str
    created_at_utc: str
    feature_definitions: list[FeatureDefinition]
    factor_definitions: list[FactorDefinition]
    allowed_output_kinds: list[FeatureOutputKind]
    blocked_output_kinds: list[FeatureBlockedOutputKind]
    metadata_only_required: bool
    research_data_only_required: bool
    trade_signal_blocked: bool
    order_decision_blocked: bool
    broker_blocked: bool
    paper_mutation_blocked: bool
    telegram_real_send_blocked: bool
    scraping_blocked: bool
    html_parsing_blocked: bool
    paid_api_blocked: bool
    dashboard_blocked: bool
    network_default_enabled_blocked: bool
    schema_valid: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureComputationRequest:
    request_id: str
    created_at_utc: str
    symbol: str
    feature_names: list[str]
    factor_names: list[str]
    computation_mode: FeatureComputationMode
    input_contract_id: str | None
    schema_id: str | None
    metadata_only: bool
    dry_run_only: bool
    research_data_only: bool
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
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureComputationResult:
    result_id: str
    created_at_utc: str
    request_id: str | None
    symbol: str
    computed_feature_count: int
    computed_factor_count: int
    planned_only: bool
    metadata_only: bool
    dry_run_only: bool
    research_data_only: bool
    output_kinds: list[FeatureOutputKind]
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
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureRegistry:
    registry_id: str
    created_at_utc: str
    indicators: list[IndicatorDefinition]
    features: list[FeatureDefinition]
    factors: list[FactorDefinition]
    total_indicators: int
    total_features: int
    total_factors: int
    registry_valid: bool
    warning_count: int
    error_count: int
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureFoundationContext:
    context_id: str
    created_at_utc: str
    status: FeatureFoundationStatus
    decision: FeatureFoundationDecision
    source_kickoff_gate_id: str | None
    ingestion: FeatureFactorKickoffIngestionResult
    input_contract: FeatureInputContract
    output_schema: FeatureOutputSchema
    registry: FeatureRegistry
    computation_requests: list[FeatureComputationRequest]
    computation_results: list[FeatureComputationResult]
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
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FeatureFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureFoundationFullReview:
    review_id: str
    created_at_utc: str
    report_type: FeatureFoundationReportType
    ingestion: FeatureFactorKickoffIngestionResult
    context: FeatureFoundationContext
    input_contract: FeatureInputContract
    output_schema: FeatureOutputSchema
    registry: FeatureRegistry
    computation_requests: list[FeatureComputationRequest]
    computation_results: list[FeatureComputationResult]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def feature_factor_kickoff_ingestion_result_to_dict(item: FeatureFactorKickoffIngestionResult) -> dict:
    return {
        "ingestion_id": item.ingestion_id,
        "created_at_utc": item.created_at_utc,
        "source_path": item.source_path,
        "source_gate_id": item.source_gate_id,
        "source_review_id": item.source_review_id,
        "available": item.available,
        "ready_for_phase116": item.ready_for_phase116,
        "phase116_scope_allowed": item.phase116_scope_allowed,
        "metadata_only": item.metadata_only,
        "research_data_only": item.research_data_only,
        "sealed": item.sealed,
        "immutable": item.immutable,
        "frozen": item.frozen,
        "activation_allowed": item.activation_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "order_creation_enabled": item.order_creation_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "scraping_enabled": item.scraping_enabled,
        "html_parse_enabled": item.html_parse_enabled,
        "paid_api_enabled": item.paid_api_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "network_default_enabled": item.network_default_enabled,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "network_used": item.network_used,
        "paid_api_used": item.paid_api_used,
        "scraping_used": item.scraping_used,
        "html_parsing_used": item.html_parsing_used,
        "broker_used": item.broker_used,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "telegram_real_sent": item.telegram_real_sent,
        "dashboard_started": item.dashboard_started,
        "valid_for_phase116": item.valid_for_phase116,
        "risk_flags": [x.value for x in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def indicator_definition_to_dict(item: IndicatorDefinition) -> dict:
    return {
        "indicator_id": item.indicator_id,
        "created_at_utc": item.created_at_utc,
        "name": item.name,
        "category": item.category.value if item.category else None,
        "description": item.description,
        "input_columns": item.input_columns,
        "output_columns": item.output_columns,
        "parameters": item.parameters,
        "computation_mode": item.computation_mode.value if item.computation_mode else None,
        "requires_network": item.requires_network,
        "requires_paid_api": item.requires_paid_api,
        "requires_scraping": item.requires_scraping,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "enabled_for_phase116": item.enabled_for_phase116,
        "implementation_phase": item.implementation_phase,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_definition_to_dict(item: FeatureDefinition) -> dict:
    return {
        "feature_id": item.feature_id,
        "created_at_utc": item.created_at_utc,
        "name": item.name,
        "category": item.category.value if item.category else None,
        "data_type": item.data_type.value if item.data_type else None,
        "description": item.description,
        "input_columns": item.input_columns,
        "output_column": item.output_column,
        "source_indicator_id": item.source_indicator_id,
        "nullable": item.nullable,
        "default_value": item.default_value,
        "computation_mode": item.computation_mode.value if item.computation_mode else None,
        "lineage_required": item.lineage_required,
        "validation_rules": item.validation_rules,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "enabled_for_phase116": item.enabled_for_phase116,
        "implementation_phase": item.implementation_phase,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def factor_definition_to_dict(item: FactorDefinition) -> dict:
    return {
        "factor_id": item.factor_id,
        "created_at_utc": item.created_at_utc,
        "name": item.name,
        "category": item.category.value if item.category else None,
        "description": item.description,
        "input_features": item.input_features,
        "output_column": item.output_column,
        "factor_direction": item.factor_direction,
        "computation_mode": item.computation_mode.value if item.computation_mode else None,
        "research_metadata_only": item.research_metadata_only,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "enabled_for_phase116": item.enabled_for_phase116,
        "implementation_phase": item.implementation_phase,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_input_contract_to_dict(item: FeatureInputContract) -> dict:
    return {
        "contract_id": item.contract_id,
        "created_at_utc": item.created_at_utc,
        "allowed_input_kinds": item.allowed_input_kinds,
        "required_ohlcv_columns": item.required_ohlcv_columns,
        "optional_metadata_inputs": item.optional_metadata_inputs,
        "event_context_allowed": item.event_context_allowed,
        "quality_metadata_allowed": item.quality_metadata_allowed,
        "calendar_metadata_allowed": item.calendar_metadata_allowed,
        "lineage_metadata_required": item.lineage_metadata_required,
        "metadata_only_required": item.metadata_only_required,
        "research_data_only_required": item.research_data_only_required,
        "network_allowed": item.network_allowed,
        "paid_api_allowed": item.paid_api_allowed,
        "scraping_allowed": item.scraping_allowed,
        "html_parsing_allowed": item.html_parsing_allowed,
        "broker_allowed": item.broker_allowed,
        "order_allowed": item.order_allowed,
        "paper_mutation_allowed": item.paper_mutation_allowed,
        "telegram_real_send_allowed": item.telegram_real_send_allowed,
        "dashboard_allowed": item.dashboard_allowed,
        "contract_valid": item.contract_valid,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_output_schema_to_dict(item: FeatureOutputSchema) -> dict:
    return {
        "schema_id": item.schema_id,
        "created_at_utc": item.created_at_utc,
        "feature_definitions": [feature_definition_to_dict(f) for f in item.feature_definitions],
        "factor_definitions": [factor_definition_to_dict(f) for f in item.factor_definitions],
        "allowed_output_kinds": [x.value for x in item.allowed_output_kinds],
        "blocked_output_kinds": [x.value for x in item.blocked_output_kinds],
        "metadata_only_required": item.metadata_only_required,
        "research_data_only_required": item.research_data_only_required,
        "trade_signal_blocked": item.trade_signal_blocked,
        "order_decision_blocked": item.order_decision_blocked,
        "broker_blocked": item.broker_blocked,
        "paper_mutation_blocked": item.paper_mutation_blocked,
        "telegram_real_send_blocked": item.telegram_real_send_blocked,
        "scraping_blocked": item.scraping_blocked,
        "html_parsing_blocked": item.html_parsing_blocked,
        "paid_api_blocked": item.paid_api_blocked,
        "dashboard_blocked": item.dashboard_blocked,
        "network_default_enabled_blocked": item.network_default_enabled_blocked,
        "schema_valid": item.schema_valid,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_computation_request_to_dict(item: FeatureComputationRequest) -> dict:
    return {
        "request_id": item.request_id,
        "created_at_utc": item.created_at_utc,
        "symbol": item.symbol,
        "feature_names": item.feature_names,
        "factor_names": item.factor_names,
        "computation_mode": item.computation_mode.value if item.computation_mode else None,
        "input_contract_id": item.input_contract_id,
        "schema_id": item.schema_id,
        "metadata_only": item.metadata_only,
        "dry_run_only": item.dry_run_only,
        "research_data_only": item.research_data_only,
        "allow_network": item.allow_network,
        "allow_paid_api": item.allow_paid_api,
        "allow_scraping": item.allow_scraping,
        "allow_html_parsing": item.allow_html_parsing,
        "allow_broker": item.allow_broker,
        "allow_order": item.allow_order,
        "allow_paper_mutation": item.allow_paper_mutation,
        "allow_telegram_real_send": item.allow_telegram_real_send,
        "allow_dashboard": item.allow_dashboard,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_computation_result_to_dict(item: FeatureComputationResult) -> dict:
    return {
        "result_id": item.result_id,
        "created_at_utc": item.created_at_utc,
        "request_id": item.request_id,
        "symbol": item.symbol,
        "computed_feature_count": item.computed_feature_count,
        "computed_factor_count": item.computed_factor_count,
        "planned_only": item.planned_only,
        "metadata_only": item.metadata_only,
        "dry_run_only": item.dry_run_only,
        "research_data_only": item.research_data_only,
        "output_kinds": [x.value for x in item.output_kinds],
        "produced_trade_signal": item.produced_trade_signal,
        "produced_order_decision": item.produced_order_decision,
        "network_used": item.network_used,
        "paid_api_used": item.paid_api_used,
        "scraping_used": item.scraping_used,
        "html_parsing_used": item.html_parsing_used,
        "broker_used": item.broker_used,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "telegram_real_sent": item.telegram_real_sent,
        "dashboard_started": item.dashboard_started,
        "passed": item.passed,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_registry_to_dict(item: FeatureRegistry) -> dict:
    return {
        "registry_id": item.registry_id,
        "created_at_utc": item.created_at_utc,
        "indicators": [indicator_definition_to_dict(i) for i in item.indicators],
        "features": [feature_definition_to_dict(f) for f in item.features],
        "factors": [factor_definition_to_dict(f) for f in item.factors],
        "total_indicators": item.total_indicators,
        "total_features": item.total_features,
        "total_factors": item.total_factors,
        "registry_valid": item.registry_valid,
        "warning_count": item.warning_count,
        "error_count": item.error_count,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_foundation_context_to_dict(item: FeatureFoundationContext) -> dict:
    return {
        "context_id": item.context_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value if item.status else None,
        "decision": item.decision.value if item.decision else None,
        "source_kickoff_gate_id": item.source_kickoff_gate_id,
        "ingestion": feature_factor_kickoff_ingestion_result_to_dict(item.ingestion),
        "input_contract": feature_input_contract_to_dict(item.input_contract),
        "output_schema": feature_output_schema_to_dict(item.output_schema),
        "registry": feature_registry_to_dict(item.registry),
        "computation_requests": [feature_computation_request_to_dict(r) for r in item.computation_requests],
        "computation_results": [feature_computation_result_to_dict(r) for r in item.computation_results],
        "feature_foundation_ready": item.feature_foundation_ready,
        "indicator_registry_ready": item.indicator_registry_ready,
        "feature_registry_ready": item.feature_registry_ready,
        "factor_registry_ready": item.factor_registry_ready,
        "input_contract_ready": item.input_contract_ready,
        "output_schema_ready": item.output_schema_ready,
        "ready_for_phase117": item.ready_for_phase117,
        "metadata_only": item.metadata_only,
        "research_data_only": item.research_data_only,
        "activation_allowed": item.activation_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "order_creation_enabled": item.order_creation_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "scraping_enabled": item.scraping_enabled,
        "html_parse_enabled": item.html_parse_enabled,
        "paid_api_enabled": item.paid_api_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "network_default_enabled": item.network_default_enabled,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "network_used": item.network_used,
        "paid_api_used": item.paid_api_used,
        "scraping_used": item.scraping_used,
        "html_parsing_used": item.html_parsing_used,
        "broker_used": item.broker_used,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "telegram_real_sent": item.telegram_real_sent,
        "dashboard_started": item.dashboard_started,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [x.value for x in item.risk_flags],
        "metadata": item.metadata
    }

def feature_foundation_full_review_to_dict(item: FeatureFoundationFullReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value if item.report_type else None,
        "ingestion": feature_factor_kickoff_ingestion_result_to_dict(item.ingestion),
        "context": feature_foundation_context_to_dict(item.context),
        "input_contract": feature_input_contract_to_dict(item.input_contract),
        "output_schema": feature_output_schema_to_dict(item.output_schema),
        "registry": feature_registry_to_dict(item.registry),
        "computation_requests": [feature_computation_request_to_dict(r) for r in item.computation_requests],
        "computation_results": [feature_computation_result_to_dict(r) for r in item.computation_results],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors
    }

def validate_feature_factor_kickoff_ingestion_result(item: FeatureFactorKickoffIngestionResult) -> None:
    if not item.ready_for_phase116:
        item.errors.append("ready_for_phase116 must be true")
    if not item.phase116_scope_allowed:
        item.errors.append("phase116_scope_allowed must be true")
    if not item.metadata_only:
        item.errors.append("metadata_only must be true")
    if not item.research_data_only:
        item.errors.append("research_data_only must be true")
    if not item.sealed:
        item.errors.append("sealed must be true")
    if not item.immutable:
        item.errors.append("immutable must be true")
    if not item.frozen:
        item.errors.append("frozen must be true")
    if item.activation_allowed:
        item.errors.append("activation_allowed must be false")
    if item.active_paper_enabled:
        item.errors.append("active_paper_enabled must be false")
    if item.broker_execution_enabled:
        item.errors.append("broker_execution_enabled must be false")
    if item.order_creation_enabled:
        item.errors.append("order_creation_enabled must be false")
    if item.paper_state_mutation_enabled:
        item.errors.append("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled:
        item.errors.append("telegram_real_send_enabled must be false")
    if item.scraping_enabled:
        item.errors.append("scraping_enabled must be false")
    if item.html_parse_enabled:
        item.errors.append("html_parse_enabled must be false")
    if item.paid_api_enabled:
        item.errors.append("paid_api_enabled must be false")
    if item.dashboard_enabled:
        item.errors.append("dashboard_enabled must be false")
    if item.network_default_enabled:
        item.errors.append("network_default_enabled must be false")
    if item.produces_trade_signal:
        item.errors.append("produces_trade_signal must be false")
    if item.produces_order_decision:
        item.errors.append("produces_order_decision must be false")
    if item.network_used:
        item.errors.append("network_used must be false")
    if item.paid_api_used:
        item.errors.append("paid_api_used must be false")
    if item.scraping_used:
        item.errors.append("scraping_used must be false")
    if item.html_parsing_used:
        item.errors.append("html_parsing_used must be false")
    if item.broker_used:
        item.errors.append("broker_used must be false")
    if item.order_created:
        item.errors.append("order_created must be false")
    if item.paper_state_mutated:
        item.errors.append("paper_state_mutated must be false")
    if item.telegram_real_sent:
        item.errors.append("telegram_real_sent must be false")
    if item.dashboard_started:
        item.errors.append("dashboard_started must be false")

def validate_indicator_definition(item: IndicatorDefinition) -> None:
    if item.produces_trade_signal:
        item.errors.append("produces_trade_signal must be false")
    if item.produces_order_decision:
        item.errors.append("produces_order_decision must be false")

def validate_feature_definition(item: FeatureDefinition) -> None:
    if item.produces_trade_signal:
        item.errors.append("produces_trade_signal must be false")
    if item.produces_order_decision:
        item.errors.append("produces_order_decision must be false")

def validate_factor_definition(item: FactorDefinition) -> None:
    if item.produces_trade_signal:
        item.errors.append("produces_trade_signal must be false")
    if item.produces_order_decision:
        item.errors.append("produces_order_decision must be false")

def validate_feature_input_contract(item: FeatureInputContract) -> None:
    pass

def validate_feature_output_schema(item: FeatureOutputSchema) -> None:
    pass

def validate_feature_computation_request(item: FeatureComputationRequest) -> None:
    if item.allow_network:
        item.errors.append("allow_network must be false")

def validate_feature_computation_result(item: FeatureComputationResult) -> None:
    if item.produced_trade_signal:
        item.errors.append("produced_trade_signal must be false")
    if item.produced_order_decision:
        item.errors.append("produced_order_decision must be false")

def validate_feature_registry(item: FeatureRegistry) -> None:
    pass

def validate_feature_foundation_context(item: FeatureFoundationContext) -> None:
    pass

def validate_feature_foundation_full_review(item: FeatureFoundationFullReview) -> None:
    pass
