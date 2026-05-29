from dataclasses import dataclass, field
from typing import Any
import datetime
import uuid
from usa_signal_bot.core.enums import (
    RegimeFeatureEngineeringStatus,
    RegimeFeatureEngineeringDecision,
    MarketStateMetricKind,
    RegimeFeatureKind,
    RegimeCandidateKind,
    RegimeCandidatePreparationMethod,
    RegimeCandidateReadinessStatus,
    RegimeCandidateReadinessRuleKind,
    RegimeFeatureQuality,
    RegimeFeatureEngineeringRiskFlag,
    RegimeFeatureEngineeringReportType
)

def create_regime_foundation_ingestion_id() -> str: return f"rfi_{uuid.uuid4().hex[:12]}"
def create_market_state_metric_spec_id() -> str: return f"msms_{uuid.uuid4().hex[:12]}"
def create_market_state_metric_result_id() -> str: return f"msmr_{uuid.uuid4().hex[:12]}"
def create_regime_feature_spec_id() -> str: return f"rfs_{uuid.uuid4().hex[:12]}"
def create_regime_feature_table_id() -> str: return f"rft_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_definition_id() -> str: return f"rcd_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_score_id() -> str: return f"rcs_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_profile_id() -> str: return f"rcp_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_preparation_id() -> str: return f"rcpr_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_readiness_rule_id() -> str: return f"rcrr_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_readiness_gate_id() -> str: return f"rcrg_{uuid.uuid4().hex[:12]}"
def create_regime_feature_engineering_context_id() -> str: return f"rfec_{uuid.uuid4().hex[:12]}"
def create_regime_feature_engineering_full_review_id() -> str: return f"rfer_{uuid.uuid4().hex[:12]}"

@dataclass
class RegimeFoundationIngestionResult:
    ingestion_id: str = field(default_factory=create_regime_foundation_ingestion_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    source_path: str | None = None
    source_review_id: str | None = None
    source_context_id: str | None = None
    available: bool = False
    final_closure_ingested: bool = False
    frozen_artifacts_ready: bool = False
    input_contract_ready: bool = False
    market_state_dataset_contract_ready: bool = False
    regime_taxonomy_ready: bool = False
    non_activation_boundary_ready: bool = False
    ready_for_phase127: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    model_training_used: bool = False
    heavy_ml_dependency_used: bool = False
    valid_for_phase127: bool = False
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketStateMetricSpec:
    spec_id: str = field(default_factory=create_market_state_metric_spec_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    metric_name: str = ""
    metric_kind: MarketStateMetricKind = MarketStateMetricKind.UNKNOWN
    input_columns: list[str] = field(default_factory=list)
    output_column: str = ""
    window: int | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    local_pandas_only: bool = True
    deterministic: bool = True
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketStateMetricResult:
    result_id: str = field(default_factory=create_market_state_metric_result_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    symbol: str | None = None
    metric_name: str = ""
    metric_kind: MarketStateMetricKind = MarketStateMetricKind.UNKNOWN
    output_column: str = ""
    row_count: int = 0
    finite_count: int = 0
    null_count: int = 0
    min_value: float | None = None
    max_value: float | None = None
    mean_value: float | None = None
    latest_value: float | None = None
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureSpec:
    spec_id: str = field(default_factory=create_regime_feature_spec_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    feature_name: str = ""
    feature_kind: RegimeFeatureKind = RegimeFeatureKind.UNKNOWN
    input_columns: list[str] = field(default_factory=list)
    output_column: str = ""
    source_metric_names: list[str] = field(default_factory=list)
    transform: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    local_pandas_only: bool = True
    deterministic: bool = True
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureTableResult:
    table_id: str = field(default_factory=create_regime_feature_table_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    symbol: str | None = None
    rows: int = 0
    columns: list[str] = field(default_factory=list)
    metric_columns: list[str] = field(default_factory=list)
    regime_feature_columns: list[str] = field(default_factory=list)
    candidate_prep_columns: list[str] = field(default_factory=list)
    null_summary: dict[str, Any] = field(default_factory=dict)
    schema_valid: bool = False
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    output_path: str | None = None
    research_data_only: bool = True
    contains_trade_signal: bool = False
    contains_order_decision: bool = False
    contains_portfolio_weight: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateDefinition:
    candidate_id: str = field(default_factory=create_regime_candidate_definition_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    candidate_name: str = ""
    candidate_kind: RegimeCandidateKind = RegimeCandidateKind.UNKNOWN
    taxonomy_label_name: str = ""
    preparation_method: RegimeCandidatePreparationMethod = RegimeCandidatePreparationMethod.UNKNOWN
    input_feature_columns: list[str] = field(default_factory=list)
    positive_context_columns: list[str] = field(default_factory=list)
    negative_context_columns: list[str] = field(default_factory=list)
    neutral_context_columns: list[str] = field(default_factory=list)
    threshold_metadata: dict[str, Any] = field(default_factory=dict)
    centroid_metadata: dict[str, Any] = field(default_factory=dict)
    distance_metadata: dict[str, Any] = field(default_factory=dict)
    description: str = ""
    research_metadata_only: bool = True
    model_training_used: bool = False
    activation_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateScore:
    score_id: str = field(default_factory=create_regime_candidate_score_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    symbol: str | None = None
    timestamp: str | None = None
    candidate_name: str = ""
    candidate_kind: RegimeCandidateKind = RegimeCandidateKind.UNKNOWN
    taxonomy_label_name: str = ""
    candidate_score: float = 0.0
    normalized_candidate_score: float = 0.0
    distance_score: float | None = None
    confidence_proxy: float | None = None
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    research_metadata_only: bool = True
    model_prediction: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateProfile:
    profile_id: str = field(default_factory=create_regime_candidate_profile_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    candidate_name: str = ""
    candidate_kind: RegimeCandidateKind = RegimeCandidateKind.UNKNOWN
    taxonomy_label_name: str = ""
    score_count: int = 0
    average_score: float | None = None
    max_score: float | None = None
    min_score: float | None = None
    latest_score: float | None = None
    candidate_available: bool = False
    candidate_valid: bool = False
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidatePreparationResult:
    preparation_id: str = field(default_factory=create_regime_candidate_preparation_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    candidate_definitions: list[RegimeCandidateDefinition] = field(default_factory=list)
    candidate_profiles: list[RegimeCandidateProfile] = field(default_factory=list)
    candidate_scores: list[RegimeCandidateScore] = field(default_factory=list)
    candidate_count: int = 0
    score_count: int = 0
    taxonomy_aligned: bool = False
    candidates_valid: bool = False
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction_used: bool = False
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateReadinessRule:
    rule_id: str = field(default_factory=create_regime_candidate_readiness_rule_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    rule_kind: RegimeCandidateReadinessRuleKind = RegimeCandidateReadinessRuleKind.UNKNOWN
    name: str = ""
    status: RegimeCandidateReadinessStatus = RegimeCandidateReadinessStatus.NOT_CHECKED
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateReadinessGate:
    gate_id: str = field(default_factory=create_regime_candidate_readiness_gate_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    status: RegimeCandidateReadinessStatus = RegimeCandidateReadinessStatus.NOT_CHECKED
    rules: list[RegimeCandidateReadinessRule] = field(default_factory=list)
    preparation_result: RegimeCandidatePreparationResult | None = None
    ready_for_phase128: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureEngineeringContext:
    context_id: str = field(default_factory=create_regime_feature_engineering_context_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    status: RegimeFeatureEngineeringStatus = RegimeFeatureEngineeringStatus.UNKNOWN
    decision: RegimeFeatureEngineeringDecision = RegimeFeatureEngineeringDecision.UNKNOWN
    source_regime_foundation_review_id: str | None = None
    ingestion: RegimeFoundationIngestionResult | None = None
    metric_specs: list[MarketStateMetricSpec] = field(default_factory=list)
    metric_results: list[MarketStateMetricResult] = field(default_factory=list)
    feature_specs: list[RegimeFeatureSpec] = field(default_factory=list)
    feature_tables: list[RegimeFeatureTableResult] = field(default_factory=list)
    candidate_preparation: RegimeCandidatePreparationResult | None = None
    readiness_gate: RegimeCandidateReadinessGate | None = None
    foundation_ingested: bool = False
    inputs_loaded: bool = False
    metric_specs_ready: bool = False
    feature_specs_ready: bool = False
    metrics_computed: bool = False
    feature_table_ready: bool = False
    candidates_prepared: bool = False
    candidate_readiness_gate_ready: bool = False
    ready_for_phase128: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    model_training_used: bool = False
    heavy_ml_dependency_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureEngineeringFullReview:
    review_id: str = field(default_factory=create_regime_feature_engineering_full_review_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    report_type: RegimeFeatureEngineeringReportType = RegimeFeatureEngineeringReportType.FULL_PHASE127_REVIEW
    ingestion: RegimeFoundationIngestionResult | None = None
    context: RegimeFeatureEngineeringContext | None = None
    metric_specs: list[MarketStateMetricSpec] = field(default_factory=list)
    metric_results: list[MarketStateMetricResult] = field(default_factory=list)
    feature_specs: list[RegimeFeatureSpec] = field(default_factory=list)
    feature_tables: list[RegimeFeatureTableResult] = field(default_factory=list)
    candidate_preparation: RegimeCandidatePreparationResult | None = None
    readiness_gate: RegimeCandidateReadinessGate | None = None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def regime_foundation_ingestion_result_to_dict(item: RegimeFoundationIngestionResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def market_state_metric_spec_to_dict(item: MarketStateMetricSpec) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def market_state_metric_result_to_dict(item: MarketStateMetricResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_spec_to_dict(item: RegimeFeatureSpec) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_table_result_to_dict(item: RegimeFeatureTableResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_definition_to_dict(item: RegimeCandidateDefinition) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_score_to_dict(item: RegimeCandidateScore) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_profile_to_dict(item: RegimeCandidateProfile) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_preparation_result_to_dict(item: RegimeCandidatePreparationResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_readiness_gate_to_dict(item: RegimeCandidateReadinessGate) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_engineering_context_to_dict(item: RegimeFeatureEngineeringContext) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_engineering_full_review_to_dict(item: RegimeFeatureEngineeringFullReview) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def validate_regime_foundation_ingestion_result(item: RegimeFoundationIngestionResult) -> None:
    if item.ready_for_phase127 and not item.research_data_only:
        raise ValueError("ready_for_phase127 requires research_data_only=True")
    if item.activation_allowed or item.strategy_activation_allowed or item.deployment_allowed:
        raise ValueError("Activation/deployment not allowed")
    if item.active_paper_enabled or item.broker_execution_enabled or item.order_creation_enabled or item.paper_state_mutation_enabled:
        raise ValueError("Execution not allowed")
    if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
        raise ValueError("Trade signals not allowed")
    if item.investment_advice:
        raise ValueError("Investment advice not allowed")
    if item.model_training_used or item.heavy_ml_dependency_used:
        raise ValueError("Model training not allowed")

def validate_market_state_metric_spec(item: MarketStateMetricSpec) -> None:
    pass

def validate_market_state_metric_result(item: MarketStateMetricResult) -> None:
    pass

def validate_regime_feature_spec(item: RegimeFeatureSpec) -> None:
    pass

def validate_regime_feature_table_result(item: RegimeFeatureTableResult) -> None:
    pass

def validate_regime_candidate_definition(item: RegimeCandidateDefinition) -> None:
    pass

def validate_regime_candidate_score(item: RegimeCandidateScore) -> None:
    if item.candidate_score < 0.0 or item.candidate_score > 100.0:
        raise ValueError("Candidate score must be between 0 and 100")
    if item.normalized_candidate_score < 0.0 or item.normalized_candidate_score > 1.0:
        raise ValueError("Normalized candidate score must be between 0 and 1")
    if item.model_prediction:
        raise ValueError("Model prediction not allowed")

def validate_regime_candidate_profile(item: RegimeCandidateProfile) -> None:
    pass

def validate_regime_candidate_preparation_result(item: RegimeCandidatePreparationResult) -> None:
    pass

def validate_regime_candidate_readiness_gate(item: RegimeCandidateReadinessGate) -> None:
    if item.ready_for_phase128 and item.status != RegimeCandidateReadinessStatus.PASSED:
        raise ValueError("Cannot be ready_for_phase128 without PASSED status")

def validate_regime_feature_engineering_context(item: RegimeFeatureEngineeringContext) -> None:
    pass

def validate_regime_feature_engineering_full_review(item: RegimeFeatureEngineeringFullReview) -> None:
    pass
