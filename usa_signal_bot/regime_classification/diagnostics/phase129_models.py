import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, Optional

from usa_signal_bot.core.enums import (
    RegimeTransitionAnalyticsStatus,
    RegimeTransitionAnalyticsDecision,
    RegimeTransitionMetricKind,
    RegimePersistenceMetricKind,
    RegimeStabilityDiagnosticKind,
    RegimeChurnLevel,
    RegimeDiagnosticsReadinessStatus,
    RegimeDiagnosticsReadinessRuleKind,
    RegimeDiagnosticsQuality,
    RegimeTransitionRiskFlag,
    RegimeTransitionReportType,
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class RegimeLabelingIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    feature_engineering_ingested: bool
    inputs_loaded: bool
    labeling_specs_ready: bool
    heuristic_labels_ready: bool
    rolling_windows_ready: bool
    candidates_validated: bool
    label_stability_profiled: bool
    readiness_gate_ready: bool
    ready_for_phase129: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
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
    model_training_used: bool
    model_prediction_used: bool
    heavy_ml_dependency_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase129: bool
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeTransitionObservation:
    observation_id: str
    created_at_utc: str
    symbol: Optional[str]
    from_label: str
    to_label: str
    transition_count: int
    transition_probability: float
    self_transition: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeTransitionMatrix:
    matrix_id: str
    created_at_utc: str
    symbol: Optional[str]
    labels: list[str]
    observations: list[RegimeTransitionObservation]
    transition_counts: dict[str, dict[str, int]]
    transition_probabilities: dict[str, dict[str, float]]
    total_transitions: int
    self_transition_count: int
    switch_count: int
    self_transition_rate: float
    switch_rate: float
    dominant_transition: Optional[str]
    transition_entropy_proxy: Optional[float]
    transition_concentration: Optional[float]
    matrix_valid: bool
    quality: RegimeDiagnosticsQuality
    research_metadata_only: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimePersistenceProfile:
    persistence_id: str
    created_at_utc: str
    symbol: Optional[str]
    label_name: str
    run_count: int
    total_periods: int
    average_run_length: Optional[float]
    median_run_length: Optional[float]
    max_run_length: Optional[int]
    persistence_ratio: Optional[float]
    self_transition_rate: Optional[float]
    average_confidence: Optional[float]
    quality: RegimeDiagnosticsQuality
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeDurationProfile:
    duration_id: str
    created_at_utc: str
    symbol: Optional[str]
    label_name: str
    run_lengths: list[int]
    run_count: int
    min_duration: Optional[int]
    max_duration: Optional[int]
    average_duration: Optional[float]
    median_duration: Optional[float]
    latest_duration: Optional[int]
    duration_profile_valid: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeChurnDiagnostic:
    churn_id: str
    created_at_utc: str
    symbol: Optional[str]
    label_column: str
    row_count: int
    switch_count: int
    switch_rate: float
    churn_level: RegimeChurnLevel
    low_confidence_count: int
    conflict_count: int
    window_disagreement_count: int
    notes: list[str]
    quality: RegimeDiagnosticsQuality
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeStabilityDiagnostic:
    stability_diag_id: str
    created_at_utc: str
    symbol: Optional[str]
    diagnostic_kind: RegimeStabilityDiagnosticKind
    diagnostic_name: str
    diagnostic_score: float
    diagnostic_value: Optional[float]
    quality: RegimeDiagnosticsQuality
    notes: list[str]
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeTransitionAnalyticsResult:
    analytics_id: str
    created_at_utc: str
    transition_matrices: list[RegimeTransitionMatrix]
    persistence_profiles: list[RegimePersistenceProfile]
    duration_profiles: list[RegimeDurationProfile]
    churn_diagnostics: list[RegimeChurnDiagnostic]
    stability_diagnostics: list[RegimeStabilityDiagnostic]
    matrix_count: int
    persistence_profile_count: int
    duration_profile_count: int
    churn_diagnostic_count: int
    stability_diagnostic_count: int
    analytics_valid: bool
    quality: RegimeDiagnosticsQuality
    research_metadata_only: bool
    model_training_used: bool
    model_prediction_used: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeDiagnosticsReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeDiagnosticsReadinessRuleKind
    name: str
    status: RegimeDiagnosticsReadinessStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeDiagnosticsReadinessGate:
    gate_id: str
    created_at_utc: str
    status: RegimeDiagnosticsReadinessStatus
    rules: list[RegimeDiagnosticsReadinessRule]
    analytics_result: RegimeTransitionAnalyticsResult
    ready_for_phase130: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeTransitionContext:
    context_id: str
    created_at_utc: str
    status: RegimeTransitionAnalyticsStatus
    decision: RegimeTransitionAnalyticsDecision
    source_regime_labeling_review_id: Optional[str]
    ingestion: RegimeLabelingIngestionResult
    analytics_result: RegimeTransitionAnalyticsResult
    readiness_gate: RegimeDiagnosticsReadinessGate
    labeling_ingested: bool
    sequences_loaded: bool
    transition_matrix_built: bool
    persistence_analytics_built: bool
    duration_analytics_built: bool
    churn_diagnostics_built: bool
    stability_diagnostics_built: bool
    readiness_gate_ready: bool
    ready_for_phase130: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
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
    model_training_used: bool
    model_prediction_used: bool
    heavy_ml_dependency_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeTransitionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeTransitionFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeTransitionReportType
    ingestion: RegimeLabelingIngestionResult
    context: RegimeTransitionContext
    analytics_result: RegimeTransitionAnalyticsResult
    readiness_gate: RegimeDiagnosticsReadinessGate
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_regime_labeling_ingestion_id() -> str:
    return f"rli_{uuid.uuid4().hex[:8]}"

def create_regime_transition_observation_id() -> str:
    return f"rto_{uuid.uuid4().hex[:8]}"

def create_regime_transition_matrix_id() -> str:
    return f"rtm_{uuid.uuid4().hex[:8]}"

def create_regime_persistence_profile_id() -> str:
    return f"rpp_{uuid.uuid4().hex[:8]}"

def create_regime_duration_profile_id() -> str:
    return f"rdp_{uuid.uuid4().hex[:8]}"

def create_regime_churn_diagnostic_id() -> str:
    return f"rcd_{uuid.uuid4().hex[:8]}"

def create_regime_stability_diagnostic_id() -> str:
    return f"rsd_{uuid.uuid4().hex[:8]}"

def create_regime_transition_analytics_id() -> str:
    return f"rta_{uuid.uuid4().hex[:8]}"

def create_regime_diagnostics_readiness_rule_id() -> str:
    return f"rdrr_{uuid.uuid4().hex[:8]}"

def create_regime_diagnostics_readiness_gate_id() -> str:
    return f"rdrg_{uuid.uuid4().hex[:8]}"

def create_regime_transition_context_id() -> str:
    return f"rtc_{uuid.uuid4().hex[:8]}"

def create_regime_transition_full_review_id() -> str:
    return f"rtfr_{uuid.uuid4().hex[:8]}"


# _to_dict and validate_* wrappers can be added below,
# but we will rely on standard JSON serialization wrappers in our store.
