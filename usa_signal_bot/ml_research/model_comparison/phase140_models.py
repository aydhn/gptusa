import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict, Optional

from usa_signal_bot.core.enums import (
    BaselineModelComparisonStatus,
    BaselineModelComparisonDecision,
    ModelComparisonInputKind,
    MetricNormalizationKind,
    ModelComparisonScoreKind,
    ModelRankingStatus,
    CandidateShortlistStatus,
    CalibrationPreparationKind,
    CalibrationPreparationStatus,
    SelectionGovernanceRuleKind,
    SelectionGovernanceStatus,
    ModelComparisonReadinessStatus,
    ModelComparisonReadinessRuleKind,
    BaselineModelComparisonQuality,
    BaselineModelComparisonRiskFlag,
    BaselineModelComparisonReportType
)


def create_baseline_training_ingestion_id() -> str:
    return f"bti_{uuid.uuid4().hex[:12]}"

def create_model_comparison_input_reference_id() -> str:
    return f"ref_{uuid.uuid4().hex[:12]}"

def create_metric_normalization_rule_id() -> str:
    return f"mnr_{uuid.uuid4().hex[:12]}"

def create_metric_normalization_result_id() -> str:
    return f"mnres_{uuid.uuid4().hex[:12]}"

def create_model_comparison_score_id() -> str:
    return f"mcs_{uuid.uuid4().hex[:12]}"

def create_split_aware_comparison_id() -> str:
    return f"sac_{uuid.uuid4().hex[:12]}"

def create_regime_aware_comparison_id() -> str:
    return f"rac_{uuid.uuid4().hex[:12]}"

def create_model_ranking_entry_id() -> str:
    return f"mre_{uuid.uuid4().hex[:12]}"

def create_model_ranking_table_id() -> str:
    return f"mrt_{uuid.uuid4().hex[:12]}"

def create_candidate_shortlist_id() -> str:
    return f"csh_{uuid.uuid4().hex[:12]}"

def create_calibration_preparation_spec_id() -> str:
    return f"cps_{uuid.uuid4().hex[:12]}"

def create_calibration_readiness_profile_id() -> str:
    return f"crp_{uuid.uuid4().hex[:12]}"

def create_selection_governance_rule_id() -> str:
    return f"sgr_{uuid.uuid4().hex[:12]}"

def create_selection_governance_result_id() -> str:
    return f"sres_{uuid.uuid4().hex[:12]}"

def create_model_card_comparison_update_id() -> str:
    return f"mcu_{uuid.uuid4().hex[:12]}"

def create_model_comparison_readiness_rule_id() -> str:
    return f"mcrr_{uuid.uuid4().hex[:12]}"

def create_model_comparison_readiness_gate_id() -> str:
    return f"mcrg_{uuid.uuid4().hex[:12]}"

def create_baseline_model_comparison_context_id() -> str:
    return f"bmc_{uuid.uuid4().hex[:12]}"

def create_baseline_model_comparison_full_review_id() -> str:
    return f"rev_{uuid.uuid4().hex[:12]}"


@dataclass
class BaselineTrainingIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    scaffolding_ingested: bool
    scaffolding_artifacts_loaded: bool
    dataset_loaded: bool
    training_jobs_built: bool
    baseline_models_trained: bool
    offline_predictions_built: bool
    evaluation_metrics_built: bool
    evaluation_report_built: bool
    model_registry_built: bool
    model_cards_updated: bool
    training_boundary_validated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase140: bool
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
    local_offline_training_used: bool
    offline_evaluation_prediction_used: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
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
    valid_for_phase140: bool
    risk_flags: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ModelComparisonInputReference:
    reference_id: str
    created_at_utc: str
    input_kind: str
    artifact_name: str
    source_path: str | None
    source_hash: str | None
    source_id: str | None
    experiment_id: str | None
    model_artifact_id: str | None
    available: bool
    read_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
    contains_trade_signal: bool
    contains_order_decision: bool
    contains_portfolio_weight: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class MetricNormalizationRule:
    rule_id: str
    created_at_utc: str
    metric_name: str
    metric_kind: str
    normalization_kind: str
    higher_is_better: bool | None
    min_value: float | None
    max_value: float | None
    weight: float
    required: bool
    non_trading_metric: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class MetricNormalizationResult:
    result_id: str
    created_at_utc: str
    metric_name: str
    metric_kind: str
    experiment_id: str | None
    model_artifact_id: str | None
    raw_value: float | int | str | dict | None
    normalized_value: float | None
    normalization_kind: str
    weight: float
    included_in_ranking: bool
    non_trading_metric: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class ModelComparisonScore:
    score_id: str
    created_at_utc: str
    experiment_id: str | None
    model_artifact_id: str | None
    model_name: str
    score_kind: str
    score_value: float | None
    component_scores: dict[str, Any]
    metric_result_ids: list[str]
    split_name: str | None
    research_only_rankable: bool
    non_trading_score: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class SplitAwareComparisonResult:
    split_comparison_id: str
    created_at_utc: str
    model_artifact_id: str | None
    experiment_id: str | None
    train_score: float | None
    validation_score: float | None
    test_score: float | None
    split_stability_score: float | None
    generalization_gap: float | None
    warning_level: str
    diagnostic_notes: list[str]
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class RegimeAwareComparisonResult:
    regime_comparison_id: str
    created_at_utc: str
    model_artifact_id: str | None
    experiment_id: str | None
    regime_bucket_scores: dict[str, Any]
    regime_consistency_score: float | None
    missing_regime_context: bool
    diagnostic_notes: list[str]
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class ModelRankingEntry:
    ranking_entry_id: str
    created_at_utc: str
    rank: int
    experiment_id: str | None
    model_artifact_id: str | None
    model_name: str
    overall_score: float | None
    validation_score: float | None
    test_score: float | None
    stability_score: float | None
    regime_consistency_score: float | None
    calibration_prep_score: float | None
    governance_score: float | None
    eligible_for_candidate_shortlist: bool
    eligible_for_live_use: bool
    eligible_for_paper_use: bool
    eligible_for_broker_use: bool
    eligible_for_deployment: bool
    eligible_for_strategy_activation: bool
    research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class ModelRankingTable:
    ranking_id: str
    created_at_utc: str
    ranking_status: str
    entries: list[ModelRankingEntry]
    entry_count: int
    rankable_entry_count: int
    ranking_hash: str | None
    ranking_valid: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class CandidateShortlist:
    shortlist_id: str
    created_at_utc: str
    shortlist_status: str
    entries: list[ModelRankingEntry]
    max_candidate_count: int
    selected_candidate_count: int
    selection_rationale: list[str]
    research_only: bool
    phase141_calibration_candidates_only: bool
    eligible_for_live_use: bool
    eligible_for_paper_use: bool
    eligible_for_broker_use: bool
    eligible_for_deployment: bool
    eligible_for_strategy_activation: bool
    shortlist_hash: str | None
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class CalibrationPreparationSpec:
    calibration_prep_id: str
    created_at_utc: str
    preparation_kind: str
    model_artifact_id: str | None
    experiment_id: str | None
    model_name: str
    probability_outputs_available: bool
    score_outputs_available: bool
    class_labels_available: bool
    required_calibration_inputs: list[str]
    missing_calibration_inputs: list[str]
    phase141_action: str
    status: str
    fitting_performed: bool
    calibration_model_created: bool
    research_data_only: bool
    activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class CalibrationReadinessProfile:
    profile_id: str
    created_at_utc: str
    model_artifact_id: str | None
    experiment_id: str | None
    model_name: str
    preparation_specs: list[CalibrationPreparationSpec]
    ready_for_phase141_calibration_review: bool
    fitting_performed: bool
    calibration_model_created: bool
    readiness_score: float | None
    diagnostic_notes: list[str]
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class SelectionGovernanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: str
    name: str
    status: str
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class SelectionGovernanceResult:
    governance_id: str
    created_at_utc: str
    rules: list[SelectionGovernanceRule]
    governance_status: str
    governance_passed: bool
    candidate_shortlist: CandidateShortlist
    ranking_table: ModelRankingTable
    calibration_profiles: list[CalibrationReadinessProfile]
    research_only_selection: bool
    live_selection_allowed: bool
    paper_selection_allowed: bool
    broker_selection_allowed: bool
    deployment_selection_allowed: bool
    strategy_activation_allowed: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class ModelCardComparisonUpdate:
    update_id: str
    created_at_utc: str
    source_model_card_update_id: str | None
    model_artifact_id: str | None
    experiment_id: str | None
    ranking_entry_id: str | None
    updated_sections: list[str]
    rendered_markdown: str | None
    rendered_text: str | None
    update_hash: str | None
    comparison_status_updated: bool
    ranking_status_updated: bool
    calibration_preparation_updated: bool
    non_activation_notice_preserved: bool
    not_investment_advice: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class ModelComparisonReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: str
    name: str
    status: str
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class ModelComparisonReadinessGate:
    gate_id: str
    created_at_utc: str
    status: str
    rules: list[ModelComparisonReadinessRule]
    ranking_table: ModelRankingTable
    candidate_shortlist: CandidateShortlist
    calibration_profiles: list[CalibrationReadinessProfile]
    selection_governance: SelectionGovernanceResult
    ready_for_phase141: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    live_inference_enabled: bool
    calibration_fitting_performed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class BaselineModelComparisonContext:
    context_id: str
    created_at_utc: str
    status: str
    decision: str
    source_baseline_training_review_id: str | None
    ingestion: BaselineTrainingIngestionResult
    input_references: list[ModelComparisonInputReference]
    normalization_rules: list[MetricNormalizationRule]
    normalization_results: list[MetricNormalizationResult]
    comparison_scores: list[ModelComparisonScore]
    split_comparisons: list[SplitAwareComparisonResult]
    regime_comparisons: list[RegimeAwareComparisonResult]
    ranking_table: ModelRankingTable
    candidate_shortlist: CandidateShortlist
    calibration_profiles: list[CalibrationReadinessProfile]
    selection_governance: SelectionGovernanceResult
    model_card_updates: list[ModelCardComparisonUpdate]
    readiness_gate: ModelComparisonReadinessGate
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
    warnings: list[str]
    errors: list[str]
    risk_flags: list[str]
    metadata: dict[str, Any]

@dataclass
class BaselineModelComparisonFullReview:
    review_id: str
    created_at_utc: str
    report_type: str
    ingestion: BaselineTrainingIngestionResult
    context: BaselineModelComparisonContext
    ranking_table: ModelRankingTable
    candidate_shortlist: CandidateShortlist
    calibration_profiles: list[CalibrationReadinessProfile]
    selection_governance: SelectionGovernanceResult
    readiness_gate: ModelComparisonReadinessGate
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]


def baseline_training_ingestion_result_to_dict(obj: BaselineTrainingIngestionResult) -> dict: return asdict(obj)
def model_comparison_input_reference_to_dict(obj: ModelComparisonInputReference) -> dict: return asdict(obj)
def metric_normalization_rule_to_dict(obj: MetricNormalizationRule) -> dict: return asdict(obj)
def metric_normalization_result_to_dict(obj: MetricNormalizationResult) -> dict: return asdict(obj)
def model_comparison_score_to_dict(obj: ModelComparisonScore) -> dict: return asdict(obj)
def split_aware_comparison_result_to_dict(obj: SplitAwareComparisonResult) -> dict: return asdict(obj)
def regime_aware_comparison_result_to_dict(obj: RegimeAwareComparisonResult) -> dict: return asdict(obj)
def model_ranking_entry_to_dict(obj: ModelRankingEntry) -> dict: return asdict(obj)
def model_ranking_table_to_dict(obj: ModelRankingTable) -> dict: return asdict(obj)
def candidate_shortlist_to_dict(obj: CandidateShortlist) -> dict: return asdict(obj)
def calibration_preparation_spec_to_dict(obj: CalibrationPreparationSpec) -> dict: return asdict(obj)
def calibration_readiness_profile_to_dict(obj: CalibrationReadinessProfile) -> dict: return asdict(obj)
def selection_governance_rule_to_dict(obj: SelectionGovernanceRule) -> dict: return asdict(obj)
def selection_governance_result_to_dict(obj: SelectionGovernanceResult) -> dict: return asdict(obj)
def model_card_comparison_update_to_dict(obj: ModelCardComparisonUpdate) -> dict: return asdict(obj)
def model_comparison_readiness_rule_to_dict(obj: ModelComparisonReadinessRule) -> dict: return asdict(obj)
def model_comparison_readiness_gate_to_dict(obj: ModelComparisonReadinessGate) -> dict: return asdict(obj)
def baseline_model_comparison_context_to_dict(obj: BaselineModelComparisonContext) -> dict: return asdict(obj)
def baseline_model_comparison_full_review_to_dict(obj: BaselineModelComparisonFullReview) -> dict: return asdict(obj)
