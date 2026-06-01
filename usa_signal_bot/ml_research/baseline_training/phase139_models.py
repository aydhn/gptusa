"""Phase 139 Dataclass Models"""
import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.enums import (
    BaselineTrainingStatus,
    BaselineTrainingDecision,
    BaselineTrainingJobKind,
    BaselineFittedModelKind,
    OfflinePredictionKind,
    OfflineEvaluationStatus,
    OfflineEvaluationMetricKind,
    NonActivationModelRegistryStatus,
    ModelRegistryEntryStatus,
    BaselineTrainingBoundaryRuleKind,
    BaselineTrainingReadinessStatus,
    BaselineTrainingReadinessRuleKind,
    BaselineTrainingQuality,
    BaselineTrainingRiskFlag,
    BaselineTrainingReportType
)

def _uuid() -> str:
    return str(uuid.uuid4())

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def create_baseline_scaffolding_ingestion_id() -> str:
    return f"bsi-{_uuid()}"

def create_baseline_training_job_id() -> str:
    return f"btj-{_uuid()}"

def create_baseline_fitted_model_artifact_id() -> str:
    return f"bma-{_uuid()}"

def create_offline_prediction_artifact_id() -> str:
    return f"opa-{_uuid()}"

def create_offline_evaluation_metric_result_id() -> str:
    return f"oem-{_uuid()}"

def create_offline_evaluation_report_id() -> str:
    return f"oer-{_uuid()}"

def create_non_activation_model_registry_entry_id() -> str:
    return f"nme-{_uuid()}"

def create_non_activation_model_registry_id() -> str:
    return f"nmr-{_uuid()}"

def create_baseline_model_card_update_id() -> str:
    return f"mcu-{_uuid()}"

def create_baseline_training_boundary_rule_id() -> str:
    return f"tbr-{_uuid()}"

def create_baseline_training_boundary_result_id() -> str:
    return f"tb-{_uuid()}"

def create_baseline_training_readiness_rule_id() -> str:
    return f"trr-{_uuid()}"

def create_baseline_training_readiness_gate_id() -> str:
    return f"trg-{_uuid()}"

def create_baseline_training_context_id() -> str:
    return f"btc-{_uuid()}"

def create_baseline_training_full_review_id() -> str:
    return f"btr-{_uuid()}"

@dataclass
class BaselineScaffoldingIngestionResult:
    ingestion_id: str = field(default_factory=create_baseline_scaffolding_ingestion_id)
    created_at_utc: str = field(default_factory=_now)
    source_path: str | None = None
    source_review_id: str | None = None
    source_context_id: str | None = None
    available: bool = False
    dataset_assembly_ingested: bool = False
    dataset_artifacts_loaded: bool = False
    experiment_specs_built: bool = False
    model_family_registry_built: bool = False
    metric_specs_built: bool = False
    evaluation_harness_contract_built: bool = False
    prediction_output_boundary_built: bool = False
    model_card_draft_built: bool = False
    experiment_registry_built: bool = False
    non_activation_boundary_validated: bool = False
    readiness_gate_built: bool = False
    readiness_gate_passed: bool = False
    ready_for_phase139: bool = False
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
    daemon_started: bool = False
    scheduler_enabled: bool = False
    training_started: bool = False
    prediction_started: bool = False
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
    valid_for_phase139: bool = False
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineTrainingJobSpec:
    job_id: str = field(default_factory=create_baseline_training_job_id)
    created_at_utc: str = field(default_factory=_now)
    job_name: str = "Unknown"
    job_kind: BaselineTrainingJobKind = BaselineTrainingJobKind.UNKNOWN
    experiment_id: str | None = None
    model_family_kind: str = "Unknown"
    feature_matrix_path: str | None = None
    target_matrix_path: str | None = None
    label_matrix_path: str | None = None
    split_assignment_path: str | None = None
    train_split_name: str = "train"
    validation_split_name: str = "validation"
    test_split_name: str = "test"
    target_name: str | None = None
    label_name: str | None = None
    allowed_feature_columns: list[str] = field(default_factory=list)
    excluded_columns: list[str] = field(default_factory=list)
    deterministic_seed: int | None = None
    local_offline_training_allowed: bool = True
    online_training_allowed: bool = False
    live_inference_allowed: bool = False
    implementation_uses_heavy_dependency: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineFittedModelArtifact:
    artifact_id: str = field(default_factory=create_baseline_fitted_model_artifact_id)
    created_at_utc: str = field(default_factory=_now)
    job_id: str = "Unknown"
    experiment_id: str | None = None
    model_name: str = "Unknown"
    fitted_model_kind: BaselineFittedModelKind = BaselineFittedModelKind.UNKNOWN
    model_parameters: dict[str, Any] = field(default_factory=dict)
    training_row_count: int = 0
    validation_row_count: int = 0
    feature_count: int = 0
    target_name: str | None = None
    label_name: str | None = None
    artifact_path: str | None = None
    artifact_hash: str | None = None
    trained_locally: bool = True
    offline_training_only: bool = True
    online_inference_enabled: bool = False
    live_inference_enabled: bool = False
    deployment_allowed: bool = False
    broker_allowed: bool = False
    paper_mutation_allowed: bool = False
    strategy_activation_allowed: bool = False
    research_data_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class OfflinePredictionArtifact:
    prediction_id: str = field(default_factory=create_offline_prediction_artifact_id)
    created_at_utc: str = field(default_factory=_now)
    artifact_id: str = "Unknown"
    job_id: str = "Unknown"
    experiment_id: str | None = None
    prediction_kind: OfflinePredictionKind = OfflinePredictionKind.UNKNOWN
    split_name: str = "Unknown"
    row_count: int = 0
    output_path: str | None = None
    output_hash: str | None = None
    output_columns: list[str] = field(default_factory=list)
    required_columns: list[str] = field(default_factory=list)
    forbidden_columns_detected: list[str] = field(default_factory=list)
    offline_evaluation_only: bool = True
    live_inference_output: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class OfflineEvaluationMetricResult:
    metric_result_id: str = field(default_factory=create_offline_evaluation_metric_result_id)
    created_at_utc: str = field(default_factory=_now)
    artifact_id: str = "Unknown"
    prediction_id: str = "Unknown"
    experiment_id: str | None = None
    metric_kind: OfflineEvaluationMetricKind = OfflineEvaluationMetricKind.UNKNOWN
    metric_name: str = "Unknown"
    split_name: str = "Unknown"
    value: float | int | str | dict[str, Any] | None = None
    higher_is_better: bool | None = None
    status: OfflineEvaluationStatus = OfflineEvaluationStatus.UNKNOWN
    sample_count: int = 0
    diagnostic_notes: list[str] = field(default_factory=list)
    non_trading_metric: bool = True
    research_data_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class OfflineEvaluationReport:
    report_id: str = field(default_factory=create_offline_evaluation_report_id)
    created_at_utc: str = field(default_factory=_now)
    experiment_id: str | None = None
    artifact_id: str = "Unknown"
    prediction_ids: list[str] = field(default_factory=list)
    metric_results: list[OfflineEvaluationMetricResult] = field(default_factory=list)
    train_metric_count: int = 0
    validation_metric_count: int = 0
    test_metric_count: int = 0
    report_hash: str | None = None
    report_valid: bool = False
    quality: BaselineTrainingQuality = BaselineTrainingQuality.UNKNOWN
    offline_evaluation_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NonActivationModelRegistryEntry:
    entry_id: str = field(default_factory=create_non_activation_model_registry_entry_id)
    created_at_utc: str = field(default_factory=_now)
    artifact_id: str = "Unknown"
    experiment_id: str | None = None
    model_name: str = "Unknown"
    fitted_model_kind: BaselineFittedModelKind = BaselineFittedModelKind.UNKNOWN
    registry_status: ModelRegistryEntryStatus = ModelRegistryEntryStatus.UNKNOWN
    artifact_path: str | None = None
    artifact_hash: str | None = None
    evaluation_report_id: str | None = None
    model_card_id: str | None = None
    eligible_for_phase140_comparison: bool = False
    eligible_for_live_use: bool = False
    eligible_for_paper_use: bool = False
    eligible_for_broker_use: bool = False
    eligible_for_deployment: bool = False
    eligible_for_strategy_activation: bool = False
    offline_research_only: bool = True
    research_data_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NonActivationModelRegistry:
    registry_id: str = field(default_factory=create_non_activation_model_registry_id)
    created_at_utc: str = field(default_factory=_now)
    registry_status: NonActivationModelRegistryStatus = NonActivationModelRegistryStatus.UNKNOWN
    registry_version: str = "phase139.v1"
    entries: list[NonActivationModelRegistryEntry] = field(default_factory=list)
    entry_count: int = 0
    valid_entry_count: int = 0
    blocked_entry_count: int = 0
    registry_hash: str | None = None
    registry_valid: bool = False
    offline_research_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    broker_allowed: bool = False
    paper_mutation_allowed: bool = False
    live_inference_enabled: bool = False
    research_data_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineModelCardUpdate:
    update_id: str = field(default_factory=create_baseline_model_card_update_id)
    created_at_utc: str = field(default_factory=_now)
    source_card_id: str | None = None
    experiment_id: str | None = None
    artifact_id: str | None = None
    evaluation_report_id: str | None = None
    updated_sections: list[str] = field(default_factory=list)
    rendered_markdown: str | None = None
    rendered_text: str | None = None
    update_hash: str | None = None
    training_status_updated: bool = False
    evaluation_status_updated: bool = False
    non_activation_notice_preserved: bool = True
    not_investment_advice: bool = True
    not_trade_signal: bool = True
    not_deployment_artifact: bool = True
    research_data_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineTrainingBoundaryRule:
    rule_id: str = field(default_factory=create_baseline_training_boundary_rule_id)
    created_at_utc: str = field(default_factory=_now)
    rule_kind: BaselineTrainingBoundaryRuleKind = BaselineTrainingBoundaryRuleKind.UNKNOWN
    name: str = "Unknown"
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineTrainingBoundaryResult:
    boundary_id: str = field(default_factory=create_baseline_training_boundary_result_id)
    created_at_utc: str = field(default_factory=_now)
    rules: list[BaselineTrainingBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    offline_training_only: bool = True
    offline_evaluation_only: bool = True
    no_live_inference: bool = True
    no_trade_signal_output: bool = True
    no_order_decision_output: bool = True
    no_portfolio_weight_output: bool = True
    no_strategy_activation: bool = True
    no_broker_execution: bool = True
    no_paper_mutation: bool = True
    no_telegram_real_send: bool = True
    no_deployment: bool = True
    no_dashboard: bool = True
    no_live_daemon: bool = True
    no_scheduler: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineTrainingReadinessRule:
    rule_id: str = field(default_factory=create_baseline_training_readiness_rule_id)
    created_at_utc: str = field(default_factory=_now)
    rule_kind: BaselineTrainingReadinessRuleKind = BaselineTrainingReadinessRuleKind.UNKNOWN
    name: str = "Unknown"
    status: BaselineTrainingReadinessStatus = BaselineTrainingReadinessStatus.UNKNOWN
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineTrainingReadinessGate:
    gate_id: str = field(default_factory=create_baseline_training_readiness_gate_id)
    created_at_utc: str = field(default_factory=_now)
    status: BaselineTrainingReadinessStatus = BaselineTrainingReadinessStatus.UNKNOWN
    rules: list[BaselineTrainingReadinessRule] = field(default_factory=list)
    training_jobs: list[BaselineTrainingJobSpec] = field(default_factory=list)
    fitted_models: list[BaselineFittedModelArtifact] = field(default_factory=list)
    prediction_artifacts: list[OfflinePredictionArtifact] = field(default_factory=list)
    evaluation_reports: list[OfflineEvaluationReport] = field(default_factory=list)
    model_registry: NonActivationModelRegistry = field(default_factory=NonActivationModelRegistry)
    boundary: BaselineTrainingBoundaryResult = field(default_factory=BaselineTrainingBoundaryResult)
    ready_for_phase140: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    live_inference_enabled: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineTrainingContext:
    context_id: str = field(default_factory=create_baseline_training_context_id)
    created_at_utc: str = field(default_factory=_now)
    status: BaselineTrainingStatus = BaselineTrainingStatus.UNKNOWN
    decision: BaselineTrainingDecision = BaselineTrainingDecision.UNKNOWN
    source_baseline_scaffolding_review_id: str | None = None
    ingestion: BaselineScaffoldingIngestionResult = field(default_factory=BaselineScaffoldingIngestionResult)
    training_jobs: list[BaselineTrainingJobSpec] = field(default_factory=list)
    fitted_models: list[BaselineFittedModelArtifact] = field(default_factory=list)
    prediction_artifacts: list[OfflinePredictionArtifact] = field(default_factory=list)
    evaluation_reports: list[OfflineEvaluationReport] = field(default_factory=list)
    model_registry: NonActivationModelRegistry = field(default_factory=NonActivationModelRegistry)
    model_card_updates: list[BaselineModelCardUpdate] = field(default_factory=list)
    boundary: BaselineTrainingBoundaryResult = field(default_factory=BaselineTrainingBoundaryResult)
    readiness_gate: BaselineTrainingReadinessGate = field(default_factory=BaselineTrainingReadinessGate)
    scaffolding_ingested: bool = False
    scaffolding_artifacts_loaded: bool = False
    dataset_loaded: bool = False
    training_jobs_built: bool = False
    baseline_models_trained: bool = False
    offline_predictions_built: bool = False
    evaluation_metrics_built: bool = False
    evaluation_report_built: bool = False
    model_registry_built: bool = False
    model_cards_updated: bool = False
    training_boundary_validated: bool = False
    readiness_gate_built: bool = False
    readiness_gate_passed: bool = False
    ready_for_phase140: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
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
    daemon_started: bool = False
    scheduler_enabled: bool = False
    local_offline_training_used: bool = False
    offline_evaluation_prediction_used: bool = False
    live_inference_enabled: bool = False
    online_inference_enabled: bool = False
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
    risk_flags: list[BaselineTrainingRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineTrainingFullReview:
    review_id: str = field(default_factory=create_baseline_training_full_review_id)
    created_at_utc: str = field(default_factory=_now)
    report_type: BaselineTrainingReportType = BaselineTrainingReportType.FULL_PHASE139_REVIEW
    ingestion: BaselineScaffoldingIngestionResult = field(default_factory=BaselineScaffoldingIngestionResult)
    context: BaselineTrainingContext = field(default_factory=BaselineTrainingContext)
    training_jobs: list[BaselineTrainingJobSpec] = field(default_factory=list)
    fitted_models: list[BaselineFittedModelArtifact] = field(default_factory=list)
    prediction_artifacts: list[OfflinePredictionArtifact] = field(default_factory=list)
    evaluation_reports: list[OfflineEvaluationReport] = field(default_factory=list)
    model_registry: NonActivationModelRegistry = field(default_factory=NonActivationModelRegistry)
    boundary: BaselineTrainingBoundaryResult = field(default_factory=BaselineTrainingBoundaryResult)
    readiness_gate: BaselineTrainingReadinessGate = field(default_factory=BaselineTrainingReadinessGate)
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
