
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
import uuid
import datetime

from usa_signal_bot.core.enums import (
    EnsemblePrototypeStatus,
    EnsemblePrototypeDecision,
    EnsemblePrototypeKind,
    OfflineEnsemblePredictionKind,
    BlendDiagnosticKind,
    CandidateAgreementKind,
    EnsembleCandidateComparisonKind,
    OfflineEnsembleEvaluationMetricKind,
    OfflineEnsembleEvaluationStatus,
    NonActivationEnsembleRegistryStatus,
    EnsembleRegistryEntryStatus,
    EnsemblePrototypeBoundaryRuleKind,
    EnsemblePrototypeReadinessStatus,
    EnsemblePrototypeReadinessRuleKind,
    EnsemblePrototypeQuality,
    EnsemblePrototypeRiskFlag,
    EnsemblePrototypeReportType
)

@dataclass
class EnsembleScaffoldingIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    calibration_diagnostics_ingested: bool
    calibration_artifacts_loaded: bool
    ensemble_candidates_resolved: bool
    ensemble_family_specs_built: bool
    candidate_groups_built: bool
    blend_policy_built: bool
    blend_coefficient_plan_built: bool
    prediction_correlation_built: bool
    diversity_profiles_built: bool
    complementarity_profiles_built: bool
    calibration_aware_eligibility_built: bool
    ensemble_preparation_report_built: bool
    ensemble_governance_built: bool
    non_activation_boundary_validated: bool
    model_cards_updated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase143: bool
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
    ensemble_fitting_performed: bool
    final_ensemble_prediction_created: bool
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
    valid_for_phase143: bool
    risk_flags: List[EnsemblePrototypeRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeInputReference:
    input_ref_id: str
    created_at_utc: str
    source_artifact_name: str
    source_artifact_kind: str
    source_path: Optional[str]
    source_hash: Optional[str]
    candidate_ref_id: Optional[str]
    candidate_group_id: Optional[str]
    blend_plan_id: Optional[str]
    prediction_artifact_id: Optional[str]
    available: bool
    read_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
    contains_forbidden_outputs: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeSpec:
    prototype_id: str
    created_at_utc: str
    prototype_name: str
    prototype_kind: EnsemblePrototypeKind
    candidate_group_id: str
    blend_plan_id: str
    candidate_ref_ids: List[str]
    coefficient_by_candidate_ref_id: Dict[str, float]
    coefficient_sum: float
    coefficient_valid: bool
    output_kind: OfflineEnsemblePredictionKind
    offline_evaluation_only: bool
    live_inference_allowed: bool
    online_inference_allowed: bool
    threshold_optimization_allowed: bool
    deployment_allowed: bool
    broker_allowed: bool
    paper_mutation_allowed: bool
    strategy_activation_allowed: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class OfflineEnsemblePredictionArtifact:
    prediction_id: str
    created_at_utc: str
    prototype_id: str
    candidate_group_id: str
    blend_plan_id: str
    prediction_kind: OfflineEnsemblePredictionKind
    split_name: Optional[str]
    row_count: int
    output_path: Optional[str]
    output_hash: Optional[str]
    output_columns: List[str]
    required_columns: List[str]
    forbidden_columns_detected: List[str]
    offline_evaluation_only: bool
    live_inference_output: bool
    online_inference_output: bool
    threshold_optimization_output: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BlendContributionDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    prototype_id: str
    candidate_ref_id: str
    blend_plan_id: str
    diagnostic_kind: BlendDiagnosticKind
    coefficient_value: Optional[float]
    contribution_share: Optional[float]
    contribution_valid: bool
    dominant_candidate_warning: bool
    not_portfolio_weight: bool
    not_allocation: bool
    not_target_weight: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CandidateAgreementDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    prototype_id: str
    candidate_a_ref_id: Optional[str]
    candidate_b_ref_id: Optional[str]
    candidate_ref_id: Optional[str]
    agreement_kind: CandidateAgreementKind
    split_name: Optional[str]
    sample_count: int
    value: Optional[float]
    diagnostic_valid: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleCandidateComparisonResult:
    comparison_id: str
    created_at_utc: str
    prototype_id: str
    candidate_ref_id: Optional[str]
    comparison_kind: EnsembleCandidateComparisonKind
    split_name: Optional[str]
    ensemble_metric_value: Optional[float]
    candidate_metric_value: Optional[float]
    delta_value: Optional[float]
    comparison_notes: List[str]
    comparison_valid: bool
    non_trading_comparison: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class OfflineEnsembleEvaluationMetricResult:
    metric_result_id: str
    created_at_utc: str
    prototype_id: str
    prediction_id: Optional[str]
    metric_kind: OfflineEnsembleEvaluationMetricKind
    metric_name: str
    split_name: Optional[str]
    value: Any
    higher_is_better: Optional[bool]
    status: OfflineEnsembleEvaluationStatus
    sample_count: int
    diagnostic_notes: List[str]
    non_trading_metric: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class OfflineEnsembleEvaluationReport:
    report_id: str
    created_at_utc: str
    prototype_id: str
    prediction_ids: List[str]
    metric_results: List[OfflineEnsembleEvaluationMetricResult]
    blend_diagnostics: List[BlendContributionDiagnostic]
    agreement_diagnostics: List[CandidateAgreementDiagnostic]
    candidate_comparisons: List[EnsembleCandidateComparisonResult]
    train_metric_count: int
    validation_metric_count: int
    test_metric_count: int
    report_hash: Optional[str]
    report_valid: bool
    quality: EnsemblePrototypeQuality
    offline_evaluation_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    threshold_optimization_performed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NonActivationEnsembleRegistryEntry:
    entry_id: str
    created_at_utc: str
    prototype_id: str
    candidate_group_id: str
    blend_plan_id: str
    prototype_name: str
    prototype_kind: EnsemblePrototypeKind
    registry_status: EnsembleRegistryEntryStatus
    prediction_artifact_id: Optional[str]
    evaluation_report_id: Optional[str]
    model_card_update_id: Optional[str]
    eligible_for_phase144_drift_baseline: bool
    eligible_for_live_use: bool
    eligible_for_paper_use: bool
    eligible_for_broker_use: bool
    eligible_for_deployment: bool
    eligible_for_strategy_activation: bool
    offline_research_only: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NonActivationEnsembleRegistry:
    registry_id: str
    created_at_utc: str
    registry_status: NonActivationEnsembleRegistryStatus
    registry_version: str
    entries: List[NonActivationEnsembleRegistryEntry]
    entry_count: int
    valid_entry_count: int
    blocked_entry_count: int
    registry_hash: Optional[str]
    registry_valid: bool
    offline_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    broker_allowed: bool
    paper_mutation_allowed: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleModelCardUpdate:
    update_id: str
    created_at_utc: str
    source_model_card_update_id: Optional[str]
    prototype_id: Optional[str]
    evaluation_report_id: Optional[str]
    registry_entry_id: Optional[str]
    updated_sections: List[str]
    rendered_markdown: Optional[str]
    rendered_text: Optional[str]
    update_hash: Optional[str]
    prototype_evaluation_updated: bool
    blend_diagnostics_updated: bool
    non_activation_registry_updated: bool
    non_activation_notice_preserved: bool
    not_investment_advice: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    no_live_inference: bool
    no_strategy_activation: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: EnsemblePrototypeBoundaryRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[EnsemblePrototypeBoundaryRule]
    boundary_passed: bool
    offline_prototype_only: bool
    offline_evaluation_only: bool
    no_live_inference: bool
    no_online_inference: bool
    no_trade_signal_output: bool
    no_order_decision_output: bool
    no_portfolio_weight_output: bool
    no_strategy_activation: bool
    no_broker_execution: bool
    no_paper_mutation: bool
    no_telegram_real_send: bool
    no_deployment: bool
    no_dashboard: bool
    no_live_daemon: bool
    no_scheduler: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: EnsemblePrototypeReadinessRuleKind
    name: str
    status: EnsemblePrototypeReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeReadinessGate:
    gate_id: str
    created_at_utc: str
    status: EnsemblePrototypeReadinessStatus
    rules: List[EnsemblePrototypeReadinessRule]
    prototype_specs: List[EnsemblePrototypeSpec]
    prediction_artifacts: List[OfflineEnsemblePredictionArtifact]
    evaluation_reports: List[OfflineEnsembleEvaluationReport]
    ensemble_registry: NonActivationEnsembleRegistry
    boundary: EnsemblePrototypeBoundaryResult
    ready_for_phase144: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    threshold_optimization_performed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeContext:
    context_id: str
    created_at_utc: str
    status: EnsemblePrototypeStatus
    decision: EnsemblePrototypeDecision
    source_ensemble_scaffolding_review_id: Optional[str]
    ingestion: EnsembleScaffoldingIngestionResult
    input_references: List[EnsemblePrototypeInputReference]
    prototype_specs: List[EnsemblePrototypeSpec]
    prediction_artifacts: List[OfflineEnsemblePredictionArtifact]
    blend_diagnostics: List[BlendContributionDiagnostic]
    agreement_diagnostics: List[CandidateAgreementDiagnostic]
    candidate_comparisons: List[EnsembleCandidateComparisonResult]
    evaluation_reports: List[OfflineEnsembleEvaluationReport]
    ensemble_registry: NonActivationEnsembleRegistry
    model_card_updates: List[EnsembleModelCardUpdate]
    boundary: EnsemblePrototypeBoundaryResult
    readiness_gate: EnsemblePrototypeReadinessGate
    ensemble_scaffolding_ingested: bool
    scaffolding_artifacts_loaded: bool
    ensemble_inputs_resolved: bool
    prototype_specs_built: bool
    offline_ensemble_predictions_built: bool
    blend_diagnostics_built: bool
    candidate_agreement_built: bool
    ensemble_candidate_comparison_built: bool
    ensemble_evaluation_metrics_built: bool
    ensemble_evaluation_report_built: bool
    ensemble_registry_built: bool
    model_cards_updated: bool
    prototype_boundary_validated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase144: bool
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
    risk_flags: List[EnsemblePrototypeRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePrototypeFullReview:
    review_id: str
    created_at_utc: str
    report_type: EnsemblePrototypeReportType
    ingestion: EnsembleScaffoldingIngestionResult
    context: EnsemblePrototypeContext
    prototype_specs: List[EnsemblePrototypeSpec]
    prediction_artifacts: List[OfflineEnsemblePredictionArtifact]
    evaluation_reports: List[OfflineEnsembleEvaluationReport]
    ensemble_registry: NonActivationEnsembleRegistry
    boundary: EnsemblePrototypeBoundaryResult
    readiness_gate: EnsemblePrototypeReadinessGate
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Helpers
def create_ensemble_scaffolding_ingestion_id() -> str:
    return f"esi_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_input_reference_id() -> str:
    return f"ep_inref_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_spec_id() -> str:
    return f"eps_{uuid.uuid4().hex[:12]}"

def create_offline_ensemble_prediction_artifact_id() -> str:
    return f"oepa_{uuid.uuid4().hex[:12]}"

def create_blend_contribution_diagnostic_id() -> str:
    return f"bcd_{uuid.uuid4().hex[:12]}"

def create_candidate_agreement_diagnostic_id() -> str:
    return f"cad_{uuid.uuid4().hex[:12]}"

def create_ensemble_candidate_comparison_id() -> str:
    return f"ecc_{uuid.uuid4().hex[:12]}"

def create_offline_ensemble_evaluation_metric_result_id() -> str:
    return f"oeemr_{uuid.uuid4().hex[:12]}"

def create_offline_ensemble_evaluation_report_id() -> str:
    return f"oeer_{uuid.uuid4().hex[:12]}"

def create_non_activation_ensemble_registry_entry_id() -> str:
    return f"naere_{uuid.uuid4().hex[:12]}"

def create_non_activation_ensemble_registry_id() -> str:
    return f"naer_{uuid.uuid4().hex[:12]}"

def create_ensemble_model_card_update_id() -> str:
    return f"emcu_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_boundary_rule_id() -> str:
    return f"epbr_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_boundary_result_id() -> str:
    return f"epbres_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_readiness_rule_id() -> str:
    return f"eprr_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_readiness_gate_id() -> str:
    return f"eprg_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_context_id() -> str:
    return f"epc_{uuid.uuid4().hex[:12]}"

def create_ensemble_prototype_full_review_id() -> str:
    return f"epfr_{uuid.uuid4().hex[:12]}"
