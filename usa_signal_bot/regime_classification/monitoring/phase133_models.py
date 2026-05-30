from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import uuid
import datetime

from usa_signal_bot.core.enums import (
    RegimeMonitoringStatus,
    RegimeMonitoringDecision,
    RegimeMonitoringBaselineKind,
    RegimeMonitoringSnapshotKind,
    RegimeDriftMetricKind,
    RegimeDriftDirection,
    RegimeDriftSeverity,
    ContextDegradationKind,
    ContextDegradationStatus,
    RegimeMonitoringReadinessStatus,
    RegimeMonitoringReadinessRuleKind,
    RegimeMonitoringQuality,
    RegimeMonitoringRiskFlag,
    RegimeMonitoringReportType
)

@dataclass
class RegimeContextValidationIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    alignment_ingested: bool
    alignment_artifacts_loaded: bool
    validation_specs_ready: bool
    compatibility_validated: bool
    conditional_diagnostics_built: bool
    acceptance_gate_built: bool
    acceptance_gate_passed: bool
    ready_for_phase133: bool
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
    valid_for_phase133: bool
    risk_flags: List[RegimeMonitoringRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class RegimeMonitoringBaseline:
    baseline_id: str
    created_at_utc: str
    baseline_kind: RegimeMonitoringBaselineKind
    source_review_id: Optional[str]
    baseline_version: str
    baseline_hash: Optional[str]
    compatibility_result_count: int
    conditional_diagnostic_count: int
    blocking_diagnostic_count: int
    warning_diagnostic_count: int
    acceptance_gate_status: Optional[str]
    low_compatibility_count: int
    uncertain_context_count: int
    conflicted_context_count: int
    data_quality_limited_count: int
    cross_symbol_summary: Dict[str, Any]
    metrics: Dict[str, Any]
    baseline_valid: bool
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeMonitoringSnapshot:
    snapshot_id: str
    created_at_utc: str
    snapshot_kind: RegimeMonitoringSnapshotKind
    source_review_id: Optional[str]
    snapshot_hash: Optional[str]
    compatibility_result_count: int
    conditional_diagnostic_count: int
    blocking_diagnostic_count: int
    warning_diagnostic_count: int
    acceptance_gate_status: Optional[str]
    low_compatibility_count: int
    uncertain_context_count: int
    conflicted_context_count: int
    data_quality_limited_count: int
    cross_symbol_summary: Dict[str, Any]
    metrics: Dict[str, Any]
    snapshot_valid: bool
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeDriftMetricSpec:
    spec_id: str
    created_at_utc: str
    metric_name: str
    metric_kind: RegimeDriftMetricKind
    baseline_field: str
    snapshot_field: str
    warning_threshold: float
    blocking_threshold: float
    higher_is_worse: bool
    deterministic: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeDriftObservation:
    observation_id: str
    created_at_utc: str
    metric_name: str
    metric_kind: RegimeDriftMetricKind
    baseline_value: Any
    snapshot_value: Any
    absolute_change: Optional[float]
    relative_change: Optional[float]
    drift_direction: RegimeDriftDirection
    drift_severity: RegimeDriftSeverity
    threshold_used: Optional[float]
    diagnostic_notes: List[str]
    research_metadata_only: bool
    investment_advice: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeDriftTrackingResult:
    drift_result_id: str
    created_at_utc: str
    baseline_id: Optional[str]
    snapshot_id: Optional[str]
    observations: List[RegimeDriftObservation]
    observation_count: int
    high_drift_count: int
    blocking_drift_count: int
    degraded_count: int
    improved_count: int
    stable_count: int
    overall_drift_direction: RegimeDriftDirection
    overall_drift_severity: RegimeDriftSeverity
    drift_valid: bool
    quality: RegimeMonitoringQuality
    research_metadata_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ContextDegradationRule:
    rule_id: str
    created_at_utc: str
    degradation_kind: ContextDegradationKind
    name: str
    warning_condition: str
    blocking_condition: str
    required: bool
    deterministic: bool
    research_metadata_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ContextDegradationDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    symbol: Optional[str]
    degradation_kind: ContextDegradationKind
    status: ContextDegradationStatus
    severity: RegimeDriftSeverity
    source_observation_id: Optional[str]
    diagnostic_text: str
    supporting_metrics: Dict[str, Any]
    recommended_action_type: str
    required_human_review: bool
    research_metadata_only: bool
    investment_advice: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ContextDegradationProfile:
    profile_id: str
    created_at_utc: str
    symbol: Optional[str]
    diagnostic_count: int
    watch_count: int
    degraded_count: int
    severely_degraded_count: int
    blocked_count: int
    profile_status: ContextDegradationStatus
    profile_summary: str
    quality: RegimeMonitoringQuality
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeMonitoringReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeMonitoringReadinessRuleKind
    name: str
    status: RegimeMonitoringReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeMonitoringReadinessGate:
    gate_id: str
    created_at_utc: str
    status: RegimeMonitoringReadinessStatus
    rules: List[RegimeMonitoringReadinessRule]
    drift_result: Optional[RegimeDriftTrackingResult]
    degradation_profiles: List[ContextDegradationProfile]
    ready_for_phase134: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeMonitoringContext:
    context_id: str
    created_at_utc: str
    status: RegimeMonitoringStatus
    decision: RegimeMonitoringDecision
    source_context_validation_review_id: Optional[str]
    ingestion: Optional[RegimeContextValidationIngestionResult]
    baseline: Optional[RegimeMonitoringBaseline]
    snapshot: Optional[RegimeMonitoringSnapshot]
    drift_specs: List[RegimeDriftMetricSpec]
    drift_result: Optional[RegimeDriftTrackingResult]
    degradation_rules: List[ContextDegradationRule]
    degradation_diagnostics: List[ContextDegradationDiagnostic]
    degradation_profiles: List[ContextDegradationProfile]
    readiness_gate: Optional[RegimeMonitoringReadinessGate]
    context_validation_ingested: bool
    artifacts_loaded: bool
    baseline_built: bool
    snapshot_built: bool
    drift_tracked: bool
    degradation_diagnostics_built: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase134: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeMonitoringRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeMonitoringFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeMonitoringReportType
    ingestion: Optional[RegimeContextValidationIngestionResult]
    context: Optional[RegimeMonitoringContext]
    baseline: Optional[RegimeMonitoringBaseline]
    snapshot: Optional[RegimeMonitoringSnapshot]
    drift_result: Optional[RegimeDriftTrackingResult]
    degradation_diagnostics: List[ContextDegradationDiagnostic]
    degradation_profiles: List[ContextDegradationProfile]
    readiness_gate: Optional[RegimeMonitoringReadinessGate]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def create_regime_context_validation_ingestion_id() -> str:
    return f"cvir_{uuid.uuid4().hex[:8]}"

def create_regime_monitoring_baseline_id() -> str:
    return f"rmbl_{uuid.uuid4().hex[:8]}"

def create_regime_monitoring_snapshot_id() -> str:
    return f"rmss_{uuid.uuid4().hex[:8]}"

def create_regime_drift_metric_spec_id() -> str:
    return f"rdms_{uuid.uuid4().hex[:8]}"

def create_regime_drift_observation_id() -> str:
    return f"rdo_{uuid.uuid4().hex[:8]}"

def create_regime_drift_tracking_result_id() -> str:
    return f"rdtr_{uuid.uuid4().hex[:8]}"

def create_context_degradation_rule_id() -> str:
    return f"cdr_{uuid.uuid4().hex[:8]}"

def create_context_degradation_diagnostic_id() -> str:
    return f"cdd_{uuid.uuid4().hex[:8]}"

def create_context_degradation_profile_id() -> str:
    return f"cdp_{uuid.uuid4().hex[:8]}"

def create_regime_monitoring_readiness_rule_id() -> str:
    return f"rmrr_{uuid.uuid4().hex[:8]}"

def create_regime_monitoring_readiness_gate_id() -> str:
    return f"rmrg_{uuid.uuid4().hex[:8]}"

def create_regime_monitoring_context_id() -> str:
    return f"rmcx_{uuid.uuid4().hex[:8]}"

def create_regime_monitoring_full_review_id() -> str:
    return f"rmfr_{uuid.uuid4().hex[:8]}"

# Dict converters
def regime_context_validation_ingestion_result_to_dict(obj: RegimeContextValidationIngestionResult) -> Dict[str, Any]:
    return asdict(obj)

def regime_monitoring_baseline_to_dict(obj: RegimeMonitoringBaseline) -> Dict[str, Any]:
    return asdict(obj)

def regime_monitoring_snapshot_to_dict(obj: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return asdict(obj)

def regime_drift_metric_spec_to_dict(obj: RegimeDriftMetricSpec) -> Dict[str, Any]:
    return asdict(obj)

def regime_drift_observation_to_dict(obj: RegimeDriftObservation) -> Dict[str, Any]:
    return asdict(obj)

def regime_drift_tracking_result_to_dict(obj: RegimeDriftTrackingResult) -> Dict[str, Any]:
    return asdict(obj)

def context_degradation_rule_to_dict(obj: ContextDegradationRule) -> Dict[str, Any]:
    return asdict(obj)

def context_degradation_diagnostic_to_dict(obj: ContextDegradationDiagnostic) -> Dict[str, Any]:
    return asdict(obj)

def context_degradation_profile_to_dict(obj: ContextDegradationProfile) -> Dict[str, Any]:
    return asdict(obj)

def regime_monitoring_readiness_rule_to_dict(obj: RegimeMonitoringReadinessRule) -> Dict[str, Any]:
    return asdict(obj)

def regime_monitoring_readiness_gate_to_dict(obj: RegimeMonitoringReadinessGate) -> Dict[str, Any]:
    return asdict(obj)

def regime_monitoring_context_to_dict(obj: RegimeMonitoringContext) -> Dict[str, Any]:
    return asdict(obj)

def regime_monitoring_full_review_to_dict(obj: RegimeMonitoringFullReview) -> Dict[str, Any]:
    return asdict(obj)
