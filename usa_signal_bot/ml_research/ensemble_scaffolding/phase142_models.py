from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid

from ...core.enums import (
    EnsembleScaffoldingStatus,
    EnsembleScaffoldingDecision,
    EnsembleCandidateKind,
    EnsembleFamilyKind,
    CandidateGroupKind,
    BlendPolicyKind,
    BlendCoefficientStatus,
    PredictionCorrelationKind,
    DiversityMetricKind,
    ComplementarityKind,
    CalibrationAwareEligibilityStatus,
    EnsembleGovernanceRuleKind,
    EnsembleGovernanceStatus,
    NonActivationEnsembleRuleKind,
    EnsembleReadinessStatus,
    EnsembleReadinessRuleKind,
    EnsembleScaffoldingQuality,
    EnsembleScaffoldingRiskFlag,
    EnsembleScaffoldingReportType
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _uuid() -> str:
    return str(uuid.uuid4())

@dataclass
class CalibrationDiagnosticsIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
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
    valid_for_phase142: bool
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class EnsembleCandidateReference:
    candidate_ref_id: str
    created_at_utc: str
    candidate_kind: EnsembleCandidateKind
    source_candidate_id: Optional[str]
    model_artifact_id: Optional[str]
    experiment_id: Optional[str]
    model_name: str
    rank: Optional[int]
    diagnostics_report_id: Optional[str]
    prediction_artifact_id: Optional[str]
    evaluation_report_id: Optional[str]
    reliability_score: Optional[float]
    calibration_warning_count: int
    post_training_validation_passed: bool
    eligible_for_ensemble_research: bool
    eligible_for_live_use: bool
    eligible_for_paper_use: bool
    eligible_for_broker_use: bool
    eligible_for_deployment: bool
    eligible_for_strategy_activation: bool
    research_data_only: bool
    offline_ml_research_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleFamilySpec:
    family_id: str
    created_at_utc: str
    family_name: str
    family_kind: EnsembleFamilyKind
    description: str
    supported_candidate_kinds: List[EnsembleCandidateKind]
    supported_blend_policies: List[BlendPolicyKind]
    fitting_allowed_in_phase142: bool
    final_prediction_allowed_in_phase142: bool
    implementation_deferred_to_phase143: bool
    requires_heavy_dependency: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CandidateGroupSpec:
    group_id: str
    created_at_utc: str
    group_name: str
    group_kind: CandidateGroupKind
    candidate_refs: List[EnsembleCandidateReference]
    min_candidate_count: int
    max_candidate_count: int
    actual_candidate_count: int
    group_valid: bool
    calibration_aware: bool
    diversity_aware: bool
    regime_aware: bool
    research_only: bool
    eligible_for_phase143_offline_ensemble_eval: bool
    eligible_for_live_use: bool
    eligible_for_paper_use: bool
    eligible_for_broker_use: bool
    eligible_for_deployment: bool
    eligible_for_strategy_activation: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BlendPolicySpec:
    policy_id: str
    created_at_utc: str
    policy_name: str
    policy_kind: BlendPolicyKind
    candidate_group_id: Optional[str]
    ensemble_family_kind: EnsembleFamilyKind
    coefficient_sum_required: float
    coefficient_non_negative_required: bool
    coefficient_cap: Optional[float]
    uses_calibration_metrics: bool
    uses_diversity_metrics: bool
    uses_ranking_metrics: bool
    fitting_allowed_in_phase142: bool
    final_prediction_allowed_in_phase142: bool
    threshold_optimization_allowed: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BlendCoefficientPlan:
    plan_id: str
    created_at_utc: str
    policy_id: str
    candidate_group_id: str
    status: BlendCoefficientStatus
    coefficient_by_candidate_ref_id: Dict[str, float]
    coefficient_sum: float
    coefficient_valid: bool
    coefficient_label: str
    not_portfolio_weight: bool
    not_allocation: bool
    not_target_weight: bool
    fitting_performed: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class PredictionCorrelationDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    candidate_a_ref_id: str
    candidate_b_ref_id: str
    correlation_kind: PredictionCorrelationKind
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
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CandidateDiversityProfile:
    profile_id: str
    created_at_utc: str
    candidate_ref_id: str
    group_id: Optional[str]
    metric_kind: DiversityMetricKind
    diversity_score: Optional[float]
    correlation_penalty: Optional[float]
    stability_bonus: Optional[float]
    calibration_bonus: Optional[float]
    diagnostic_notes: List[str]
    profile_valid: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ComplementarityProfile:
    profile_id: str
    created_at_utc: str
    candidate_ref_id: str
    group_id: Optional[str]
    complementarity_kind: ComplementarityKind
    complementarity_score: Optional[float]
    coverage_notes: List[str]
    regime_notes: List[str]
    split_notes: List[str]
    calibration_notes: List[str]
    profile_valid: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CalibrationAwareEligibilityProfile:
    profile_id: str
    created_at_utc: str
    candidate_ref_id: str
    status: CalibrationAwareEligibilityStatus
    reliability_score: Optional[float]
    ece_value: Optional[float]
    mce_value: Optional[float]
    brier_score: Optional[float]
    calibration_warning_count: int
    eligible_for_phase143_research: bool
    live_use_allowed: bool
    paper_use_allowed: bool
    broker_use_allowed: bool
    deployment_allowed: bool
    strategy_activation_allowed: bool
    diagnostic_notes: List[str]
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsemblePreparationReport:
    report_id: str
    created_at_utc: str
    candidate_group: CandidateGroupSpec
    family_spec: EnsembleFamilySpec
    blend_policy: BlendPolicySpec
    blend_plan: BlendCoefficientPlan
    correlation_diagnostics: List[PredictionCorrelationDiagnostic]
    diversity_profiles: List[CandidateDiversityProfile]
    complementarity_profiles: List[ComplementarityProfile]
    eligibility_profiles: List[CalibrationAwareEligibilityProfile]
    report_hash: Optional[str]
    report_valid: bool
    quality: EnsembleScaffoldingQuality
    fitting_performed: bool
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
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleGovernanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: EnsembleGovernanceRuleKind
    name: str
    status: EnsembleGovernanceStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleGovernanceResult:
    governance_id: str
    created_at_utc: str
    rules: List[EnsembleGovernanceRule]
    governance_status: EnsembleGovernanceStatus
    governance_passed: bool
    preparation_reports: List[EnsemblePreparationReport]
    candidate_groups: List[CandidateGroupSpec]
    blend_plans: List[BlendCoefficientPlan]
    research_only_ensemble_preparation: bool
    live_use_allowed: bool
    paper_use_allowed: bool
    broker_use_allowed: bool
    deployment_allowed: bool
    strategy_activation_allowed: bool
    fitting_performed: bool
    threshold_optimization_performed: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NonActivationEnsembleBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: NonActivationEnsembleRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NonActivationEnsembleBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[NonActivationEnsembleBoundaryRule]
    boundary_passed: bool
    no_ensemble_fitting: bool
    no_final_ensemble_prediction: bool
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
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ModelCardEnsembleUpdate:
    update_id: str
    created_at_utc: str
    source_model_card_update_id: Optional[str]
    candidate_group_id: Optional[str]
    ensemble_report_id: Optional[str]
    updated_sections: List[str]
    rendered_markdown: Optional[str]
    rendered_text: Optional[str]
    update_hash: Optional[str]
    ensemble_preparation_updated: bool
    blend_policy_updated: bool
    calibration_aware_governance_updated: bool
    non_activation_notice_preserved: bool
    not_investment_advice: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    no_ensemble_fitting_performed: bool
    no_final_ensemble_prediction_created: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: EnsembleReadinessRuleKind
    name: str
    status: EnsembleReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleReadinessGate:
    gate_id: str
    created_at_utc: str
    status: EnsembleReadinessStatus
    rules: List[EnsembleReadinessRule]
    preparation_reports: List[EnsemblePreparationReport]
    ensemble_governance: EnsembleGovernanceResult
    non_activation_boundary: NonActivationEnsembleBoundaryResult
    ready_for_phase143: bool
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
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleScaffoldingContext:
    context_id: str
    created_at_utc: str
    status: EnsembleScaffoldingStatus
    decision: EnsembleScaffoldingDecision
    source_calibration_diagnostics_review_id: Optional[str]
    ingestion: CalibrationDiagnosticsIngestionResult
    candidates: List[EnsembleCandidateReference]
    family_specs: List[EnsembleFamilySpec]
    candidate_groups: List[CandidateGroupSpec]
    blend_policies: List[BlendPolicySpec]
    blend_plans: List[BlendCoefficientPlan]
    correlation_diagnostics: List[PredictionCorrelationDiagnostic]
    diversity_profiles: List[CandidateDiversityProfile]
    complementarity_profiles: List[ComplementarityProfile]
    eligibility_profiles: List[CalibrationAwareEligibilityProfile]
    preparation_reports: List[EnsemblePreparationReport]
    ensemble_governance: EnsembleGovernanceResult
    non_activation_boundary: NonActivationEnsembleBoundaryResult
    model_card_updates: List[ModelCardEnsembleUpdate]
    readiness_gate: EnsembleReadinessGate
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
    risk_flags: List[EnsembleScaffoldingRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EnsembleScaffoldingFullReview:
    review_id: str
    created_at_utc: str
    report_type: EnsembleScaffoldingReportType
    ingestion: CalibrationDiagnosticsIngestionResult
    context: EnsembleScaffoldingContext
    preparation_reports: List[EnsemblePreparationReport]
    ensemble_governance: EnsembleGovernanceResult
    non_activation_boundary: NonActivationEnsembleBoundaryResult
    readiness_gate: EnsembleReadinessGate
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def create_calibration_diagnostics_ingestion_id() -> str:
    return f"cd_ingest_{_uuid()}"

def create_ensemble_candidate_reference_id() -> str:
    return f"ens_cand_{_uuid()}"

def create_ensemble_family_spec_id() -> str:
    return f"ens_fam_{_uuid()}"

def create_candidate_group_spec_id() -> str:
    return f"cand_grp_{_uuid()}"

def create_blend_policy_spec_id() -> str:
    return f"blend_pol_{_uuid()}"

def create_blend_coefficient_plan_id() -> str:
    return f"blend_plan_{_uuid()}"

def create_prediction_correlation_diagnostic_id() -> str:
    return f"pred_corr_{_uuid()}"

def create_candidate_diversity_profile_id() -> str:
    return f"div_prof_{_uuid()}"

def create_complementarity_profile_id() -> str:
    return f"comp_prof_{_uuid()}"

def create_calibration_aware_eligibility_profile_id() -> str:
    return f"cal_elig_{_uuid()}"

def create_ensemble_preparation_report_id() -> str:
    return f"ens_prep_{_uuid()}"

def create_ensemble_governance_rule_id() -> str:
    return f"ens_gov_rule_{_uuid()}"

def create_ensemble_governance_result_id() -> str:
    return f"ens_gov_res_{_uuid()}"

def create_non_activation_ensemble_boundary_rule_id() -> str:
    return f"na_ens_rule_{_uuid()}"

def create_non_activation_ensemble_boundary_result_id() -> str:
    return f"na_ens_res_{_uuid()}"

def create_model_card_ensemble_update_id() -> str:
    return f"mc_ens_upd_{_uuid()}"

def create_ensemble_readiness_rule_id() -> str:
    return f"ens_read_rule_{_uuid()}"

def create_ensemble_readiness_gate_id() -> str:
    return f"ens_read_gate_{_uuid()}"

def create_ensemble_scaffolding_context_id() -> str:
    return f"ens_ctx_{_uuid()}"

def create_ensemble_scaffolding_full_review_id() -> str:
    return f"ens_rev_{_uuid()}"

import dataclasses

def _to_dict(obj: Any) -> Dict[str, Any]:
    return dataclasses.asdict(obj)

def calibration_diagnostics_ingestion_result_to_dict(item: CalibrationDiagnosticsIngestionResult) -> Dict[str, Any]: return _to_dict(item)
def ensemble_candidate_reference_to_dict(item: EnsembleCandidateReference) -> Dict[str, Any]: return _to_dict(item)
def ensemble_family_spec_to_dict(item: EnsembleFamilySpec) -> Dict[str, Any]: return _to_dict(item)
def candidate_group_spec_to_dict(item: CandidateGroupSpec) -> Dict[str, Any]: return _to_dict(item)
def blend_policy_spec_to_dict(item: BlendPolicySpec) -> Dict[str, Any]: return _to_dict(item)
def blend_coefficient_plan_to_dict(item: BlendCoefficientPlan) -> Dict[str, Any]: return _to_dict(item)
def prediction_correlation_diagnostic_to_dict(item: PredictionCorrelationDiagnostic) -> Dict[str, Any]: return _to_dict(item)
def candidate_diversity_profile_to_dict(item: CandidateDiversityProfile) -> Dict[str, Any]: return _to_dict(item)
def complementarity_profile_to_dict(item: ComplementarityProfile) -> Dict[str, Any]: return _to_dict(item)
def calibration_aware_eligibility_profile_to_dict(item: CalibrationAwareEligibilityProfile) -> Dict[str, Any]: return _to_dict(item)
def ensemble_preparation_report_to_dict(item: EnsemblePreparationReport) -> Dict[str, Any]: return _to_dict(item)
def ensemble_governance_rule_to_dict(item: EnsembleGovernanceRule) -> Dict[str, Any]: return _to_dict(item)
def ensemble_governance_result_to_dict(item: EnsembleGovernanceResult) -> Dict[str, Any]: return _to_dict(item)
def non_activation_ensemble_boundary_rule_to_dict(item: NonActivationEnsembleBoundaryRule) -> Dict[str, Any]: return _to_dict(item)
def non_activation_ensemble_boundary_result_to_dict(item: NonActivationEnsembleBoundaryResult) -> Dict[str, Any]: return _to_dict(item)
def model_card_ensemble_update_to_dict(item: ModelCardEnsembleUpdate) -> Dict[str, Any]: return _to_dict(item)
def ensemble_readiness_rule_to_dict(item: EnsembleReadinessRule) -> Dict[str, Any]: return _to_dict(item)
def ensemble_readiness_gate_to_dict(item: EnsembleReadinessGate) -> Dict[str, Any]: return _to_dict(item)
def ensemble_scaffolding_context_to_dict(item: EnsembleScaffoldingContext) -> Dict[str, Any]: return _to_dict(item)
def ensemble_scaffolding_full_review_to_dict(item: EnsembleScaffoldingFullReview) -> Dict[str, Any]: return _to_dict(item)

def validate_calibration_diagnostics_ingestion_result(item: CalibrationDiagnosticsIngestionResult) -> List[str]:
    errors = []
    if not item.ready_for_phase142: errors.append("Not ready for phase 142")
    if not item.research_data_only: errors.append("research_data_only must be true")
    if not item.offline_ml_research_only: errors.append("offline_ml_research_only must be true")
    if item.activation_allowed: errors.append("activation_allowed must be false")
    if item.strategy_activation_allowed: errors.append("strategy_activation_allowed must be false")
    if item.deployment_allowed: errors.append("deployment_allowed must be false")
    if item.active_paper_enabled: errors.append("active_paper_enabled must be false")
    if item.broker_execution_enabled: errors.append("broker_execution_enabled must be false")
    if item.order_creation_enabled: errors.append("order_creation_enabled must be false")
    if item.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled: errors.append("telegram_real_send_enabled must be false")
    if item.scraping_enabled: errors.append("scraping_enabled must be false")
    if item.html_parse_enabled: errors.append("html_parse_enabled must be false")
    if item.paid_api_enabled: errors.append("paid_api_enabled must be false")
    if item.dashboard_enabled: errors.append("dashboard_enabled must be false")
    if item.network_default_enabled: errors.append("network_default_enabled must be false")
    if item.daemon_started: errors.append("daemon_started must be false")
    if item.scheduler_enabled: errors.append("scheduler_enabled must be false")
    if item.live_inference_enabled: errors.append("live_inference_enabled must be false")
    if item.online_inference_enabled: errors.append("online_inference_enabled must be false")


    if item.calibration_fitting_performed: errors.append("calibration_fitting_performed must be false")
    if item.calibrated_model_created: errors.append("calibrated_model_created must be false")
    if item.threshold_optimization_performed: errors.append("threshold_optimization_performed must be false")
    if item.heavy_ml_dependency_used: errors.append("heavy_ml_dependency_used must be false")
    if item.produces_trade_signal: errors.append("produces_trade_signal must be false")
    if item.produces_order_decision: errors.append("produces_order_decision must be false")
    if item.produces_portfolio_weights: errors.append("produces_portfolio_weights must be false")
    if item.investment_advice: errors.append("investment_advice must be false")
    return errors

def validate_ensemble_candidate_reference(item: EnsembleCandidateReference) -> List[str]:
    errors = []
    if item.eligible_for_live_use: errors.append("eligible_for_live_use must be false")
    if item.eligible_for_paper_use: errors.append("eligible_for_paper_use must be false")
    if item.eligible_for_broker_use: errors.append("eligible_for_broker_use must be false")
    if item.eligible_for_deployment: errors.append("eligible_for_deployment must be false")
    if item.eligible_for_strategy_activation: errors.append("eligible_for_strategy_activation must be false")
    return errors

def validate_ensemble_family_spec(item: EnsembleFamilySpec) -> List[str]: return []
def validate_candidate_group_spec(item: CandidateGroupSpec) -> List[str]: return []
def validate_blend_policy_spec(item: BlendPolicySpec) -> List[str]: return []

def validate_blend_coefficient_plan(item: BlendCoefficientPlan) -> List[str]:
    errors = []
    if not item.not_portfolio_weight: errors.append("not_portfolio_weight must be true")
    if not item.not_allocation: errors.append("not_allocation must be true")
    if not item.not_target_weight: errors.append("not_target_weight must be true")
    return errors

def validate_prediction_correlation_diagnostic(item: PredictionCorrelationDiagnostic) -> List[str]: return []
def validate_candidate_diversity_profile(item: CandidateDiversityProfile) -> List[str]: return []
def validate_complementarity_profile(item: ComplementarityProfile) -> List[str]: return []
def validate_calibration_aware_eligibility_profile(item: CalibrationAwareEligibilityProfile) -> List[str]: return []
def validate_ensemble_preparation_report(item: EnsemblePreparationReport) -> List[str]: return []
def validate_ensemble_governance_rule(item: EnsembleGovernanceRule) -> List[str]: return []
def validate_ensemble_governance_result(item: EnsembleGovernanceResult) -> List[str]: return []
def validate_non_activation_ensemble_boundary_rule(item: NonActivationEnsembleBoundaryRule) -> List[str]: return []
def validate_non_activation_ensemble_boundary_result(item: NonActivationEnsembleBoundaryResult) -> List[str]: return []
def validate_model_card_ensemble_update(item: ModelCardEnsembleUpdate) -> List[str]: return []
def validate_ensemble_readiness_rule(item: EnsembleReadinessRule) -> List[str]: return []

def validate_ensemble_readiness_gate(item: EnsembleReadinessGate) -> List[str]:
    errors = []
    if item.ready_for_phase143:
        if not item.ensemble_governance.governance_passed:
            errors.append("Ensemble governance must pass to be ready for phase 143")
        if not item.non_activation_boundary.boundary_passed:
            errors.append("Non-activation boundary must pass to be ready for phase 143")
    return errors

def validate_ensemble_scaffolding_context(item: EnsembleScaffoldingContext) -> List[str]: return []
def validate_ensemble_scaffolding_full_review(item: EnsembleScaffoldingFullReview) -> List[str]: return []
