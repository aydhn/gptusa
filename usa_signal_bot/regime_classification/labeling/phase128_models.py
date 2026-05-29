from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
import datetime

from usa_signal_bot.core.enums import (
    RegimeLabelingStatus,
    RegimeLabelingDecision,
    RegimeLabelingMethod,
    RegimeWindowKind,
    RegimeLabelConfidenceKind,
    RegimeLabelConflictKind,
    RegimeCandidateValidationStatus,
    RegimeCandidateValidationRuleKind,
    RegimeLabelingReadinessStatus,
    RegimeLabelingReadinessRuleKind,
    RegimeLabelingQuality,
    RegimeLabelingRiskFlag,
    RegimeLabelingReportType
)

def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class RegimeFeatureEngineeringIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    foundation_ingested: bool
    inputs_loaded: bool
    metric_specs_ready: bool
    feature_specs_ready: bool
    metrics_computed: bool
    feature_table_ready: bool
    candidates_prepared: bool
    candidate_readiness_gate_ready: bool
    ready_for_phase128: bool
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
    valid_for_phase128: bool
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelingSpec:
    spec_id: str
    created_at_utc: str
    spec_name: str
    method: RegimeLabelingMethod
    taxonomy_labels: list[str]
    candidate_score_columns: list[str]
    minimum_score_threshold: float
    minimum_score_gap: float
    fallback_label: str
    mixed_label: str
    unknown_label: str
    conflict_policy: str
    deterministic: bool
    research_metadata_only: bool
    model_training_used: bool
    model_prediction_used: bool
    activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelingRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    method: RegimeLabelingMethod
    label_name: str
    candidate_name: str | None
    threshold: float | None
    priority: int
    required_columns: list[str]
    description: str
    deterministic: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class HeuristicRegimeLabelResult:
    label_result_id: str
    created_at_utc: str
    symbol: str | None
    timestamp: str | None
    assigned_label: str
    assigned_label_kind: str
    method: RegimeLabelingMethod
    top_candidate_name: str | None
    top_candidate_score: float | None
    second_candidate_name: str | None
    second_candidate_score: float | None
    score_gap: float | None
    confidence_score: float
    confidence_kind: RegimeLabelConfidenceKind
    conflict_kinds: list[RegimeLabelConflictKind]
    fallback_used: bool
    mixed_label_used: bool
    unknown_label_used: bool
    validation_status: RegimeCandidateValidationStatus
    research_metadata_only: bool
    model_prediction: bool
    model_training_used: bool
    activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RollingRegimeWindowSpec:
    window_spec_id: str
    created_at_utc: str
    window_name: str
    window_kind: RegimeWindowKind
    window_size: int
    min_periods: int
    label_column: str
    confidence_column: str
    output_label_column: str
    output_confidence_column: str
    method: RegimeLabelingMethod
    deterministic: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RollingRegimeWindowResult:
    window_result_id: str
    created_at_utc: str
    symbol: str | None
    window_name: str
    window_kind: RegimeWindowKind
    window_size: int
    row_count: int
    output_label_column: str
    output_confidence_column: str
    dominant_label: str | None
    dominant_label_ratio: float | None
    average_confidence: float | None
    label_switch_count: int
    stability_score: float
    research_metadata_only: bool
    model_prediction: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelSequence:
    sequence_id: str
    created_at_utc: str
    symbol: str | None
    rows: int
    label_column: str
    confidence_column: str
    labels: list[str]
    label_counts: dict[str, int]
    label_switch_count: int
    dominant_label: str | None
    dominant_label_ratio: float | None
    average_confidence: float | None
    sequence_valid: bool
    research_metadata_only: bool
    model_prediction: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelStabilityProfile:
    stability_id: str
    created_at_utc: str
    symbol: str | None
    label_column: str
    row_count: int
    label_switch_count: int
    average_run_length: float | None
    dominant_label: str | None
    dominant_label_ratio: float | None
    average_confidence: float | None
    low_confidence_count: int
    conflict_count: int
    stability_score: float
    quality: RegimeLabelingQuality
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateValidationRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeCandidateValidationRuleKind
    name: str
    status: RegimeCandidateValidationStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateValidationResult:
    validation_id: str
    created_at_utc: str
    rules: list[RegimeCandidateValidationRule]
    total_rules: int
    passed_rules: int
    warning_rules: int
    failed_rules: int
    blocked_rules: int
    validation_passed: bool
    candidate_count: int
    score_count: int
    taxonomy_aligned: bool
    no_model_training: bool
    no_model_prediction: bool
    research_metadata_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    quality: RegimeLabelingQuality
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelingReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeLabelingReadinessRuleKind
    name: str
    status: RegimeLabelingReadinessStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelingReadinessGate:
    gate_id: str
    created_at_utc: str
    status: RegimeLabelingReadinessStatus
    rules: list[RegimeLabelingReadinessRule]
    candidate_validation: RegimeCandidateValidationResult | None
    stability_profiles: list[RegimeLabelStabilityProfile]
    ready_for_phase129: bool
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
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelingContext:
    context_id: str
    created_at_utc: str
    status: RegimeLabelingStatus
    decision: RegimeLabelingDecision
    source_regime_feature_engineering_review_id: str | None
    ingestion: RegimeFeatureEngineeringIngestionResult | None = None
    labeling_specs: list[RegimeLabelingSpec] = field(default_factory=list)
    labeling_rules: list[RegimeLabelingRule] = field(default_factory=list)
    label_results: list[HeuristicRegimeLabelResult] = field(default_factory=list)
    window_specs: list[RollingRegimeWindowSpec] = field(default_factory=list)
    window_results: list[RollingRegimeWindowResult] = field(default_factory=list)
    label_sequences: list[RegimeLabelSequence] = field(default_factory=list)
    stability_profiles: list[RegimeLabelStabilityProfile] = field(default_factory=list)
    candidate_validation: RegimeCandidateValidationResult | None = None
    readiness_gate: RegimeLabelingReadinessGate | None = None
    feature_engineering_ingested: bool = False
    inputs_loaded: bool = False
    labeling_specs_ready: bool = False
    heuristic_labels_ready: bool = False
    rolling_windows_ready: bool = False
    candidates_validated: bool = False
    label_stability_profiled: bool = False
    readiness_gate_ready: bool = False
    ready_for_phase129: bool = False
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
    model_prediction_used: bool = False
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
    risk_flags: list[RegimeLabelingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelingFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeLabelingReportType
    ingestion: RegimeFeatureEngineeringIngestionResult | None
    context: RegimeLabelingContext
    labeling_specs: list[RegimeLabelingSpec]
    label_results: list[HeuristicRegimeLabelResult]
    window_results: list[RollingRegimeWindowResult]
    label_sequences: list[RegimeLabelSequence]
    stability_profiles: list[RegimeLabelStabilityProfile]
    candidate_validation: RegimeCandidateValidationResult | None
    readiness_gate: RegimeLabelingReadinessGate | None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_regime_feature_engineering_ingestion_id() -> str:
    return f"rfe_ingest_{uuid.uuid4().hex[:8]}"

def create_regime_labeling_spec_id() -> str:
    return f"rl_spec_{uuid.uuid4().hex[:8]}"

def create_regime_labeling_rule_id() -> str:
    return f"rl_rule_{uuid.uuid4().hex[:8]}"

def create_heuristic_regime_label_result_id() -> str:
    return f"hl_res_{uuid.uuid4().hex[:8]}"

def create_rolling_regime_window_spec_id() -> str:
    return f"rrw_spec_{uuid.uuid4().hex[:8]}"

def create_rolling_regime_window_result_id() -> str:
    return f"rrw_res_{uuid.uuid4().hex[:8]}"

def create_regime_label_sequence_id() -> str:
    return f"rl_seq_{uuid.uuid4().hex[:8]}"

def create_regime_label_stability_profile_id() -> str:
    return f"rl_stab_{uuid.uuid4().hex[:8]}"

def create_regime_candidate_validation_rule_id() -> str:
    return f"rcv_rule_{uuid.uuid4().hex[:8]}"

def create_regime_candidate_validation_result_id() -> str:
    return f"rcv_res_{uuid.uuid4().hex[:8]}"

def create_regime_labeling_readiness_rule_id() -> str:
    return f"rlr_rule_{uuid.uuid4().hex[:8]}"

def create_regime_labeling_readiness_gate_id() -> str:
    return f"rlr_gate_{uuid.uuid4().hex[:8]}"

def create_regime_labeling_context_id() -> str:
    return f"rl_ctx_{uuid.uuid4().hex[:8]}"

def create_regime_labeling_full_review_id() -> str:
    return f"rl_rev_{uuid.uuid4().hex[:8]}"

def regime_feature_engineering_ingestion_result_to_dict(item: RegimeFeatureEngineeringIngestionResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_labeling_spec_to_dict(item: RegimeLabelingSpec) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_labeling_rule_to_dict(item: RegimeLabelingRule) -> dict:
    from dataclasses import asdict
    return asdict(item)

def heuristic_regime_label_result_to_dict(item: HeuristicRegimeLabelResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def rolling_regime_window_spec_to_dict(item: RollingRegimeWindowSpec) -> dict:
    from dataclasses import asdict
    return asdict(item)

def rolling_regime_window_result_to_dict(item: RollingRegimeWindowResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_label_sequence_to_dict(item: RegimeLabelSequence) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_label_stability_profile_to_dict(item: RegimeLabelStabilityProfile) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_validation_result_to_dict(item: RegimeCandidateValidationResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_labeling_readiness_gate_to_dict(item: RegimeLabelingReadinessGate) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_labeling_context_to_dict(item: RegimeLabelingContext) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_labeling_full_review_to_dict(item: RegimeLabelingFullReview) -> dict:
    from dataclasses import asdict
    return asdict(item)

def validate_regime_feature_engineering_ingestion_result(item: RegimeFeatureEngineeringIngestionResult) -> None:
    pass

def validate_regime_labeling_spec(item: RegimeLabelingSpec) -> None:
    pass

def validate_regime_labeling_rule(item: RegimeLabelingRule) -> None:
    pass

def validate_heuristic_regime_label_result(item: HeuristicRegimeLabelResult) -> None:
    pass

def validate_rolling_regime_window_result(item: RollingRegimeWindowResult) -> None:
    pass

def validate_regime_label_sequence(item: RegimeLabelSequence) -> None:
    pass

def validate_regime_label_stability_profile(item: RegimeLabelStabilityProfile) -> None:
    pass

def validate_regime_candidate_validation_result(item: RegimeCandidateValidationResult) -> None:
    pass

def validate_regime_labeling_readiness_gate(item: RegimeLabelingReadinessGate) -> None:
    pass

def validate_regime_labeling_context(item: RegimeLabelingContext) -> None:
    pass

def validate_regime_labeling_full_review(item: RegimeLabelingFullReview) -> None:
    pass
