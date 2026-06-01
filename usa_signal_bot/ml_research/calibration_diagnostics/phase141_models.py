from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import uuid
import datetime

from usa_signal_bot.core.enums import (
    CalibrationDiagnosticsStatus,
    CalibrationDiagnosticsDecision,
    CalibrationInputKind,
    ProbabilityReliabilityKind,
    ReliabilityBinStrategy,
    CalibrationMetricKind,
    CalibrationDiagnosticSeverity,
    CalibrationDiagnosticStatus,
    PostTrainingValidationRuleKind,
    CalibrationGovernanceRuleKind,
    CalibrationGovernanceStatus,
    CalibrationReadinessStatus,
    CalibrationReadinessRuleKind,
    CalibrationDiagnosticsQuality,
    CalibrationDiagnosticsRiskFlag,
    CalibrationDiagnosticsReportType
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class ModelComparisonIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    baseline_training_ingested: bool
    training_artifacts_loaded: bool
    evaluation_reports_normalized: bool
    metrics_normalized: bool
    model_comparison_built: bool
    split_aware_comparison_built: bool
    regime_aware_comparison_built: bool
    model_ranking_built: bool
    candidate_shortlist_built: bool
    calibration_preparation_built: bool
    selection_governance_built: bool
    model_cards_updated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase141: bool
    metadata_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
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
    daemon_started: bool
    scheduler_enabled: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    calibration_fitting_performed: bool
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
    valid_for_phase141: bool
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class CalibrationCandidateReference:
    candidate_id: str
    created_at_utc: str
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    model_name: str
    ranking_entry_id: Optional[str]
    rank: Optional[int]
    source_shortlist_id: Optional[str]
    prediction_artifact_id: Optional[str]
    evaluation_report_id: Optional[str]
    eligible_for_calibration_diagnostics: bool
    eligible_for_live_use: bool
    eligible_for_paper_use: bool
    eligible_for_broker_use: bool
    eligible_for_deployment: bool
    eligible_for_strategy_activation: bool
    research_data_only: bool
    offline_ml_research_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationInputProfile:
    profile_id: str
    created_at_utc: str
    candidate_id: str
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    input_kinds_available: List[CalibrationInputKind]
    probability_output_available: bool
    score_output_available: bool
    class_label_output_available: bool
    regression_output_available: bool
    true_label_available: bool
    true_target_available: bool
    split_assignment_available: bool
    row_count: int
    split_counts: Dict[str, int]
    output_columns: List[str]
    forbidden_columns_detected: List[str]
    input_profile_valid: bool
    quality: CalibrationDiagnosticsQuality
    research_data_only: bool
    offline_ml_research_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ReliabilityBinSpec:
    bin_spec_id: str
    created_at_utc: str
    candidate_id: str
    reliability_kind: ProbabilityReliabilityKind
    strategy: ReliabilityBinStrategy
    bin_count: int
    min_probability: float
    max_probability: float
    split_name: Optional[str]
    class_name: Optional[str]
    deterministic: bool
    fitting_performed: bool
    threshold_optimization_performed: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ReliabilityBinResult:
    bin_result_id: str
    created_at_utc: str
    bin_spec_id: str
    candidate_id: str
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    split_name: Optional[str]
    class_name: Optional[str]
    bin_index: int
    bin_lower: float
    bin_upper: float
    sample_count: int
    average_confidence: Optional[float]
    empirical_accuracy: Optional[float]
    calibration_gap: Optional[float]
    positive_count: Optional[int]
    negative_count: Optional[int]
    reliability_valid: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationMetricResult:
    metric_id: str
    created_at_utc: str
    candidate_id: str
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    split_name: Optional[str]
    metric_kind: CalibrationMetricKind
    metric_name: str
    value: Any
    sample_count: int
    status: CalibrationDiagnosticStatus
    severity: CalibrationDiagnosticSeverity
    diagnostic_notes: List[str]
    non_trading_metric: bool
    fitting_performed: bool
    threshold_optimization_performed: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BrierDecompositionResult:
    decomposition_id: str
    created_at_utc: str
    candidate_id: str
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    split_name: Optional[str]
    brier_score: Optional[float]
    reliability: Optional[float]
    resolution: Optional[float]
    uncertainty: Optional[float]
    bin_count: int
    sample_count: int
    decomposition_valid: bool
    fitting_performed: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ScoreDistributionDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    candidate_id: str
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    split_name: Optional[str]
    score_column: Optional[str]
    row_count: int
    min_score: Optional[float]
    max_score: Optional[float]
    mean_score: Optional[float]
    median_score: Optional[float]
    std_score: Optional[float]
    quantiles: Dict[str, float]
    extreme_low_count: int
    extreme_high_count: int
    missing_score_count: int
    diagnostic_valid: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ClassBalanceDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    candidate_id: str
    experiment_id: Optional[str]
    split_name: Optional[str]
    label_column: Optional[str]
    class_counts: Dict[str, int]
    class_ratios: Dict[str, float]
    majority_class: Optional[str]
    minority_class: Optional[str]
    imbalance_ratio: Optional[float]
    sample_count: int
    diagnostic_valid: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationDiagnosticsReport:
    report_id: str
    created_at_utc: str
    candidate_id: str
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    input_profile: CalibrationInputProfile
    reliability_bins: List[ReliabilityBinResult]
    calibration_metrics: List[CalibrationMetricResult]
    brier_decomposition: Optional[BrierDecompositionResult]
    score_distribution: Optional[ScoreDistributionDiagnostic]
    class_balance: Optional[ClassBalanceDiagnostic]
    report_hash: Optional[str]
    report_valid: bool
    quality: CalibrationDiagnosticsQuality
    fitting_performed: bool
    calibrated_model_created: bool
    threshold_optimization_performed: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    live_inference_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class PostTrainingValidationRule:
    rule_id: str
    created_at_utc: str
    rule_kind: PostTrainingValidationRuleKind
    name: str
    status: CalibrationDiagnosticStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    severity: CalibrationDiagnosticSeverity
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class PostTrainingValidationResult:
    validation_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    rules: List[PostTrainingValidationRule]
    total_rules: int
    passed_rules: int
    warning_rules: int
    failed_rules: int
    blocked_rules: int
    validation_passed: bool
    probability_outputs_valid: bool
    score_outputs_valid: bool
    true_labels_available: bool
    no_forbidden_output_fields: bool
    no_trade_metric_used: bool
    no_signal_output: bool
    no_order_output: bool
    no_portfolio_output: bool
    no_live_inference: bool
    no_calibration_fitting: bool
    no_deployment: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationGovernanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: CalibrationGovernanceRuleKind
    name: str
    status: CalibrationGovernanceStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationGovernanceResult:
    governance_id: str
    created_at_utc: str
    rules: List[CalibrationGovernanceRule]
    governance_status: CalibrationGovernanceStatus
    governance_passed: bool
    diagnostics_reports: List[CalibrationDiagnosticsReport]
    post_training_validations: List[PostTrainingValidationResult]
    research_only_diagnostics: bool
    live_use_allowed: bool
    paper_use_allowed: bool
    broker_use_allowed: bool
    deployment_allowed: bool
    strategy_activation_allowed: bool
    calibration_fitting_performed: bool
    calibrated_model_created: bool
    threshold_optimization_performed: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ModelCardCalibrationUpdate:
    update_id: str
    created_at_utc: str
    source_model_card_update_id: Optional[str]
    candidate_id: Optional[str]
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    diagnostics_report_id: Optional[str]
    updated_sections: List[str]
    rendered_markdown: Optional[str]
    rendered_text: Optional[str]
    update_hash: Optional[str]
    calibration_diagnostics_updated: bool
    reliability_review_updated: bool
    post_training_validation_updated: bool
    non_activation_notice_preserved: bool
    not_investment_advice: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    no_calibrated_model_created: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: CalibrationReadinessRuleKind
    name: str
    status: CalibrationReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationReadinessGate:
    gate_id: str
    created_at_utc: str
    status: CalibrationReadinessStatus
    rules: List[CalibrationReadinessRule]
    diagnostics_reports: List[CalibrationDiagnosticsReport]
    post_training_validations: List[PostTrainingValidationResult]
    calibration_governance: CalibrationGovernanceResult
    ready_for_phase142: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    calibration_fitting_performed: bool
    calibrated_model_created: bool
    threshold_optimization_performed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationDiagnosticsContext:
    context_id: str
    created_at_utc: str
    status: CalibrationDiagnosticsStatus
    decision: CalibrationDiagnosticsDecision
    source_model_comparison_review_id: Optional[str]
    ingestion: ModelComparisonIngestionResult
    candidate_references: List[CalibrationCandidateReference]
    input_profiles: List[CalibrationInputProfile]
    diagnostics_reports: List[CalibrationDiagnosticsReport]
    post_training_validations: List[PostTrainingValidationResult]
    calibration_governance: CalibrationGovernanceResult
    model_card_updates: List[ModelCardCalibrationUpdate]
    readiness_gate: CalibrationReadinessGate
    model_comparison_ingested: bool
    comparison_artifacts_loaded: bool
    calibration_inputs_resolved: bool
    reliability_bins_built: bool
    calibration_metrics_built: bool
    brier_decomposition_built: bool
    score_distribution_built: bool
    class_balance_built: bool
    post_training_validation_built: bool
    calibration_governance_built: bool
    model_cards_updated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase142: bool
    metadata_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
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
    daemon_started: bool
    scheduler_enabled: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    calibration_fitting_performed: bool
    calibrated_model_created: bool
    threshold_optimization_performed: bool
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
    risk_flags: List[CalibrationDiagnosticsRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationDiagnosticsFullReview:
    review_id: str
    created_at_utc: str
    report_type: CalibrationDiagnosticsReportType
    ingestion: ModelComparisonIngestionResult
    context: CalibrationDiagnosticsContext
    diagnostics_reports: List[CalibrationDiagnosticsReport]
    post_training_validations: List[PostTrainingValidationResult]
    calibration_governance: CalibrationGovernanceResult
    readiness_gate: CalibrationReadinessGate
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Factory Functions
def create_model_comparison_ingestion_id() -> str:
    return f"mci_{uuid.uuid4().hex}"

def create_calibration_candidate_reference_id() -> str:
    return f"ccref_{uuid.uuid4().hex}"

def create_calibration_input_profile_id() -> str:
    return f"cip_{uuid.uuid4().hex}"

def create_reliability_bin_spec_id() -> str:
    return f"rbs_{uuid.uuid4().hex}"

def create_reliability_bin_result_id() -> str:
    return f"rbr_{uuid.uuid4().hex}"

def create_calibration_metric_result_id() -> str:
    return f"cmr_{uuid.uuid4().hex}"

def create_brier_decomposition_result_id() -> str:
    return f"bdr_{uuid.uuid4().hex}"

def create_score_distribution_diagnostic_id() -> str:
    return f"sdd_{uuid.uuid4().hex}"

def create_class_balance_diagnostic_id() -> str:
    return f"cbd_{uuid.uuid4().hex}"

def create_calibration_diagnostics_report_id() -> str:
    return f"cdr_{uuid.uuid4().hex}"

def create_post_training_validation_rule_id() -> str:
    return f"ptvr_{uuid.uuid4().hex}"

def create_post_training_validation_result_id() -> str:
    return f"ptvres_{uuid.uuid4().hex}"

def create_calibration_governance_rule_id() -> str:
    return f"cgr_{uuid.uuid4().hex}"

def create_calibration_governance_result_id() -> str:
    return f"cgres_{uuid.uuid4().hex}"

def create_model_card_calibration_update_id() -> str:
    return f"mccu_{uuid.uuid4().hex}"

def create_calibration_readiness_rule_id() -> str:
    return f"crr_{uuid.uuid4().hex}"

def create_calibration_readiness_gate_id() -> str:
    return f"crg_{uuid.uuid4().hex}"

def create_calibration_diagnostics_context_id() -> str:
    return f"cdc_{uuid.uuid4().hex}"

def create_calibration_diagnostics_full_review_id() -> str:
    return f"cdfr_{uuid.uuid4().hex}"

def model_comparison_ingestion_result_to_dict(item: ModelComparisonIngestionResult) -> Dict[str, Any]: return asdict(item)
def calibration_candidate_reference_to_dict(item: CalibrationCandidateReference) -> Dict[str, Any]: return asdict(item)
def calibration_input_profile_to_dict(item: CalibrationInputProfile) -> Dict[str, Any]: return asdict(item)
def reliability_bin_spec_to_dict(item: ReliabilityBinSpec) -> Dict[str, Any]: return asdict(item)
def reliability_bin_result_to_dict(item: ReliabilityBinResult) -> Dict[str, Any]: return asdict(item)
def calibration_metric_result_to_dict(item: CalibrationMetricResult) -> Dict[str, Any]: return asdict(item)
def brier_decomposition_result_to_dict(item: BrierDecompositionResult) -> Dict[str, Any]: return asdict(item)
def score_distribution_diagnostic_to_dict(item: ScoreDistributionDiagnostic) -> Dict[str, Any]: return asdict(item)
def class_balance_diagnostic_to_dict(item: ClassBalanceDiagnostic) -> Dict[str, Any]: return asdict(item)
def calibration_diagnostics_report_to_dict(item: CalibrationDiagnosticsReport) -> Dict[str, Any]: return asdict(item)
def post_training_validation_rule_to_dict(item: PostTrainingValidationRule) -> Dict[str, Any]: return asdict(item)
def post_training_validation_result_to_dict(item: PostTrainingValidationResult) -> Dict[str, Any]: return asdict(item)
def calibration_governance_rule_to_dict(item: CalibrationGovernanceRule) -> Dict[str, Any]: return asdict(item)
def calibration_governance_result_to_dict(item: CalibrationGovernanceResult) -> Dict[str, Any]: return asdict(item)
def model_card_calibration_update_to_dict(item: ModelCardCalibrationUpdate) -> Dict[str, Any]: return asdict(item)
def calibration_readiness_rule_to_dict(item: CalibrationReadinessRule) -> Dict[str, Any]: return asdict(item)
def calibration_readiness_gate_to_dict(item: CalibrationReadinessGate) -> Dict[str, Any]: return asdict(item)
def calibration_diagnostics_context_to_dict(item: CalibrationDiagnosticsContext) -> Dict[str, Any]: return asdict(item)
def calibration_diagnostics_full_review_to_dict(item: CalibrationDiagnosticsFullReview) -> Dict[str, Any]: return asdict(item)

# Validate dummy functions
def validate_model_comparison_ingestion_result(item: ModelComparisonIngestionResult) -> List[str]: return []
def validate_calibration_candidate_reference(item: CalibrationCandidateReference) -> List[str]: return []
def validate_calibration_input_profile(item: CalibrationInputProfile) -> List[str]: return []
def validate_reliability_bin_spec(item: ReliabilityBinSpec) -> List[str]: return []
def validate_reliability_bin_result(item: ReliabilityBinResult) -> List[str]: return []
def validate_calibration_metric_result(item: CalibrationMetricResult) -> List[str]: return []
def validate_brier_decomposition_result(item: BrierDecompositionResult) -> List[str]: return []
def validate_score_distribution_diagnostic(item: ScoreDistributionDiagnostic) -> List[str]: return []
def validate_class_balance_diagnostic(item: ClassBalanceDiagnostic) -> List[str]: return []
def validate_calibration_diagnostics_report(item: CalibrationDiagnosticsReport) -> List[str]: return []
def validate_post_training_validation_rule(item: PostTrainingValidationRule) -> List[str]: return []
def validate_post_training_validation_result(item: PostTrainingValidationResult) -> List[str]: return []
def validate_calibration_governance_rule(item: CalibrationGovernanceRule) -> List[str]: return []
def validate_calibration_governance_result(item: CalibrationGovernanceResult) -> List[str]: return []
def validate_model_card_calibration_update(item: ModelCardCalibrationUpdate) -> List[str]: return []
def validate_calibration_readiness_rule(item: CalibrationReadinessRule) -> List[str]: return []
def validate_calibration_readiness_gate(item: CalibrationReadinessGate) -> List[str]: return []
def validate_calibration_diagnostics_context(item: CalibrationDiagnosticsContext) -> List[str]: return []
def validate_calibration_diagnostics_full_review(item: CalibrationDiagnosticsFullReview) -> List[str]: return []
