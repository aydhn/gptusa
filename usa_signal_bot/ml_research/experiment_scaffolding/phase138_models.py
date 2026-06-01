import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import (
    BaselineMLScaffoldingStatus,
    BaselineMLScaffoldingDecision,
    BaselineExperimentKind,
    BaselineModelFamilyKind,
    EvaluationMetricKind,
    EvaluationHarnessKind,
    PredictionOutputBoundaryKind,
    ModelCardSectionKind,
    ExperimentRegistryStatus,
    NonActivationEvaluationRuleKind,
    BaselineScaffoldingReadinessStatus,
    BaselineScaffoldingReadinessRuleKind,
    BaselineMLScaffoldingQuality,
    BaselineMLScaffoldingRiskFlag,
    BaselineMLScaffoldingReportType
)

def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def create_ml_dataset_assembly_ingestion_id() -> str:
    return f"dai_{uuid.uuid4().hex[:8]}"

def create_baseline_model_family_spec_id() -> str:
    return f"mfs_{uuid.uuid4().hex[:8]}"

def create_baseline_experiment_spec_id() -> str:
    return f"es_{uuid.uuid4().hex[:8]}"

def create_evaluation_metric_spec_id() -> str:
    return f"ems_{uuid.uuid4().hex[:8]}"

def create_evaluation_harness_contract_id() -> str:
    return f"ehc_{uuid.uuid4().hex[:8]}"

def create_prediction_output_boundary_id() -> str:
    return f"pob_{uuid.uuid4().hex[:8]}"

def create_model_artifact_placeholder_id() -> str:
    return f"map_{uuid.uuid4().hex[:8]}"

def create_model_card_draft_section_id() -> str:
    return f"mcds_{uuid.uuid4().hex[:8]}"

def create_model_card_draft_id() -> str:
    return f"mcd_{uuid.uuid4().hex[:8]}"

def create_baseline_experiment_registry_id() -> str:
    return f"ber_{uuid.uuid4().hex[:8]}"

def create_non_activation_evaluation_boundary_rule_id() -> str:
    return f"naeb_rule_{uuid.uuid4().hex[:8]}"

def create_non_activation_evaluation_boundary_result_id() -> str:
    return f"naeb_{uuid.uuid4().hex[:8]}"

def create_baseline_experiment_readiness_rule_id() -> str:
    return f"berr_{uuid.uuid4().hex[:8]}"

def create_baseline_experiment_readiness_gate_id() -> str:
    return f"berg_{uuid.uuid4().hex[:8]}"

def create_baseline_ml_scaffolding_context_id() -> str:
    return f"bmsc_{uuid.uuid4().hex[:8]}"

def create_baseline_ml_scaffolding_full_review_id() -> str:
    return f"bmsfr_{uuid.uuid4().hex[:8]}"

@dataclass
class MLDatasetAssemblyIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    ml_foundation_ingested: bool
    foundation_artifacts_loaded: bool
    sources_resolved: bool
    feature_matrix_assembled: bool
    target_matrix_assembled: bool
    label_matrix_assembled: bool
    dataset_manifest_built: bool
    split_policy_built: bool
    split_assignment_built: bool
    leakage_audit_completed: bool
    dataset_quality_evaluated: bool
    split_quality_evaluated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase138: bool
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
    daemon_started: bool
    scheduler_enabled: bool
    training_started: bool
    prediction_started: bool
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
    valid_for_phase138: bool
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ingestion_id": self.ingestion_id,
            "created_at_utc": self.created_at_utc,
            "source_path": self.source_path,
            "source_review_id": self.source_review_id,
            "source_context_id": self.source_context_id,
            "available": self.available,
            "ml_foundation_ingested": self.ml_foundation_ingested,
            "foundation_artifacts_loaded": self.foundation_artifacts_loaded,
            "sources_resolved": self.sources_resolved,
            "feature_matrix_assembled": self.feature_matrix_assembled,
            "target_matrix_assembled": self.target_matrix_assembled,
            "label_matrix_assembled": self.label_matrix_assembled,
            "dataset_manifest_built": self.dataset_manifest_built,
            "split_policy_built": self.split_policy_built,
            "split_assignment_built": self.split_assignment_built,
            "leakage_audit_completed": self.leakage_audit_completed,
            "dataset_quality_evaluated": self.dataset_quality_evaluated,
            "split_quality_evaluated": self.split_quality_evaluated,
            "readiness_gate_built": self.readiness_gate_built,
            "readiness_gate_passed": self.readiness_gate_passed,
            "ready_for_phase138": self.ready_for_phase138,
            "metadata_only": self.metadata_only,
            "research_data_only": self.research_data_only,
            "activation_allowed": self.activation_allowed,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "active_paper_enabled": self.active_paper_enabled,
            "broker_execution_enabled": self.broker_execution_enabled,
            "order_creation_enabled": self.order_creation_enabled,
            "paper_state_mutation_enabled": self.paper_state_mutation_enabled,
            "telegram_real_send_enabled": self.telegram_real_send_enabled,
            "scraping_enabled": self.scraping_enabled,
            "html_parse_enabled": self.html_parse_enabled,
            "paid_api_enabled": self.paid_api_enabled,
            "dashboard_enabled": self.dashboard_enabled,
            "network_default_enabled": self.network_default_enabled,
            "daemon_started": self.daemon_started,
            "scheduler_enabled": self.scheduler_enabled,
            "training_started": self.training_started,
            "prediction_started": self.prediction_started,
            "model_training_used": self.model_training_used,
            "model_prediction_used": self.model_prediction_used,
            "heavy_ml_dependency_used": self.heavy_ml_dependency_used,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "investment_advice": self.investment_advice,
            "network_used": self.network_used,
            "paid_api_used": self.paid_api_used,
            "scraping_used": self.scraping_used,
            "html_parsing_used": self.html_parsing_used,
            "broker_used": self.broker_used,
            "order_created": self.order_created,
            "paper_state_mutated": self.paper_state_mutated,
            "telegram_real_sent": self.telegram_real_sent,
            "dashboard_started": self.dashboard_started,
            "valid_for_phase138": self.valid_for_phase138,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata
        }

@dataclass
class BaselineModelFamilySpec:
    family_id: str
    created_at_utc: str
    family_name: str
    family_kind: BaselineModelFamilyKind
    experiment_kind: BaselineExperimentKind
    training_allowed_in_phase138: bool
    prediction_allowed_in_phase138: bool
    implementation_deferred_to_phase139: bool
    requires_heavy_dependency: bool
    allowed_dependency_names: List[str]
    forbidden_dependency_names: List[str]
    expected_input_matrix_kind: str
    expected_target_kind: str
    expected_label_kind: Optional[str]
    output_boundary_kind: PredictionOutputBoundaryKind
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "family_id": self.family_id,
            "created_at_utc": self.created_at_utc,
            "family_name": self.family_name,
            "family_kind": self.family_kind.value,
            "experiment_kind": self.experiment_kind.value,
            "training_allowed_in_phase138": self.training_allowed_in_phase138,
            "prediction_allowed_in_phase138": self.prediction_allowed_in_phase138,
            "implementation_deferred_to_phase139": self.implementation_deferred_to_phase139,
            "requires_heavy_dependency": self.requires_heavy_dependency,
            "allowed_dependency_names": self.allowed_dependency_names,
            "forbidden_dependency_names": self.forbidden_dependency_names,
            "expected_input_matrix_kind": self.expected_input_matrix_kind,
            "expected_target_kind": self.expected_target_kind,
            "expected_label_kind": self.expected_label_kind,
            "output_boundary_kind": self.output_boundary_kind.value,
            "research_metadata_only": self.research_metadata_only,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class BaselineExperimentSpec:
    experiment_id: str
    created_at_utc: str
    experiment_name: str
    experiment_kind: BaselineExperimentKind
    model_family: BaselineModelFamilySpec
    dataset_manifest_id: Optional[str]
    split_assignment_id: Optional[str]
    target_name: Optional[str]
    label_name: Optional[str]
    feature_scope: List[str]
    metric_kinds: List[EvaluationMetricKind]
    evaluation_harness_kind: EvaluationHarnessKind
    reproducibility_seed: Optional[int]
    training_deferred_to_phase139: bool
    prediction_deferred_to_phase139: bool
    evaluation_deferred_until_artifacts_exist: bool
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
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "created_at_utc": self.created_at_utc,
            "experiment_name": self.experiment_name,
            "experiment_kind": self.experiment_kind.value,
            "model_family": self.model_family.to_dict(),
            "dataset_manifest_id": self.dataset_manifest_id,
            "split_assignment_id": self.split_assignment_id,
            "target_name": self.target_name,
            "label_name": self.label_name,
            "feature_scope": self.feature_scope,
            "metric_kinds": [mk.value for mk in self.metric_kinds],
            "evaluation_harness_kind": self.evaluation_harness_kind.value,
            "reproducibility_seed": self.reproducibility_seed,
            "training_deferred_to_phase139": self.training_deferred_to_phase139,
            "prediction_deferred_to_phase139": self.prediction_deferred_to_phase139,
            "evaluation_deferred_until_artifacts_exist": self.evaluation_deferred_until_artifacts_exist,
            "research_metadata_only": self.research_metadata_only,
            "activation_allowed": self.activation_allowed,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "model_training_used": self.model_training_used,
            "model_prediction_used": self.model_prediction_used,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "investment_advice": self.investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class EvaluationMetricSpec:
    metric_id: str
    created_at_utc: str
    metric_name: str
    metric_kind: EvaluationMetricKind
    applies_to_experiment_kinds: List[BaselineExperimentKind]
    higher_is_better: Optional[bool]
    requires_probabilities: bool
    requires_class_labels: bool
    requires_regression_values: bool
    aggregation_method: str
    threshold_free: bool
    non_trading_metric: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "created_at_utc": self.created_at_utc,
            "metric_name": self.metric_name,
            "metric_kind": self.metric_kind.value,
            "applies_to_experiment_kinds": [k.value for k in self.applies_to_experiment_kinds],
            "higher_is_better": self.higher_is_better,
            "requires_probabilities": self.requires_probabilities,
            "requires_class_labels": self.requires_class_labels,
            "requires_regression_values": self.requires_regression_values,
            "aggregation_method": self.aggregation_method,
            "threshold_free": self.threshold_free,
            "non_trading_metric": self.non_trading_metric,
            "research_metadata_only": self.research_metadata_only,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class EvaluationHarnessContract:
    harness_id: str
    created_at_utc: str
    harness_kind: EvaluationHarnessKind
    harness_version: str
    dataset_manifest_id: Optional[str]
    split_assignment_id: Optional[str]
    required_metric_specs: List[EvaluationMetricSpec]
    accepted_prediction_boundary_kinds: List[PredictionOutputBoundaryKind]
    allowed_input_artifacts: List[str]
    forbidden_output_fields: List[str]
    training_allowed_in_phase138: bool
    prediction_allowed_in_phase138: bool
    live_evaluation_allowed: bool
    broker_evaluation_allowed: bool
    paper_mutation_allowed: bool
    contract_hash: Optional[str]
    contract_valid: bool
    quality: BaselineMLScaffoldingQuality
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
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "harness_id": self.harness_id,
            "created_at_utc": self.created_at_utc,
            "harness_kind": self.harness_kind.value,
            "harness_version": self.harness_version,
            "dataset_manifest_id": self.dataset_manifest_id,
            "split_assignment_id": self.split_assignment_id,
            "required_metric_specs": [s.to_dict() for s in self.required_metric_specs],
            "accepted_prediction_boundary_kinds": [k.value for k in self.accepted_prediction_boundary_kinds],
            "allowed_input_artifacts": self.allowed_input_artifacts,
            "forbidden_output_fields": self.forbidden_output_fields,
            "training_allowed_in_phase138": self.training_allowed_in_phase138,
            "prediction_allowed_in_phase138": self.prediction_allowed_in_phase138,
            "live_evaluation_allowed": self.live_evaluation_allowed,
            "broker_evaluation_allowed": self.broker_evaluation_allowed,
            "paper_mutation_allowed": self.paper_mutation_allowed,
            "contract_hash": self.contract_hash,
            "contract_valid": self.contract_valid,
            "quality": self.quality.value,
            "research_metadata_only": self.research_metadata_only,
            "activation_allowed": self.activation_allowed,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "model_training_used": self.model_training_used,
            "model_prediction_used": self.model_prediction_used,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "investment_advice": self.investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class PredictionOutputBoundary:
    boundary_id: str
    created_at_utc: str
    allowed_output_kinds: List[PredictionOutputBoundaryKind]
    forbidden_output_fields: List[str]
    required_output_fields: List[str]
    optional_output_fields: List[str]
    forbidden_semantics: List[str]
    allows_trade_signal: bool
    allows_order_decision: bool
    allows_portfolio_weight: bool
    allows_strategy_activation: bool
    allows_broker_execution: bool
    allows_paper_mutation: bool
    boundary_hash: Optional[str]
    boundary_valid: bool
    research_metadata_only: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "created_at_utc": self.created_at_utc,
            "allowed_output_kinds": [k.value for k in self.allowed_output_kinds],
            "forbidden_output_fields": self.forbidden_output_fields,
            "required_output_fields": self.required_output_fields,
            "optional_output_fields": self.optional_output_fields,
            "forbidden_semantics": self.forbidden_semantics,
            "allows_trade_signal": self.allows_trade_signal,
            "allows_order_decision": self.allows_order_decision,
            "allows_portfolio_weight": self.allows_portfolio_weight,
            "allows_strategy_activation": self.allows_strategy_activation,
            "allows_broker_execution": self.allows_broker_execution,
            "allows_paper_mutation": self.allows_paper_mutation,
            "boundary_hash": self.boundary_hash,
            "boundary_valid": self.boundary_valid,
            "research_metadata_only": self.research_metadata_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class ModelArtifactPlaceholder:
    placeholder_id: str
    created_at_utc: str
    placeholder_name: str
    experiment_id: Optional[str]
    model_family_kind: BaselineModelFamilyKind
    artifact_path: Optional[str]
    artifact_hash: Optional[str]
    created_by_training: bool
    training_deferred_to_phase139: bool
    prediction_deferred_to_phase139: bool
    deployment_allowed: bool
    broker_allowed: bool
    strategy_activation_allowed: bool
    research_metadata_only: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "placeholder_id": self.placeholder_id,
            "created_at_utc": self.created_at_utc,
            "placeholder_name": self.placeholder_name,
            "experiment_id": self.experiment_id,
            "model_family_kind": self.model_family_kind.value,
            "artifact_path": self.artifact_path,
            "artifact_hash": self.artifact_hash,
            "created_by_training": self.created_by_training,
            "training_deferred_to_phase139": self.training_deferred_to_phase139,
            "prediction_deferred_to_phase139": self.prediction_deferred_to_phase139,
            "deployment_allowed": self.deployment_allowed,
            "broker_allowed": self.broker_allowed,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "research_metadata_only": self.research_metadata_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class ModelCardDraftSection:
    section_id: str
    created_at_utc: str
    section_kind: ModelCardSectionKind
    title: str
    body: str
    bullet_points: List[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_id": self.section_id,
            "created_at_utc": self.created_at_utc,
            "section_kind": self.section_kind.value,
            "title": self.title,
            "body": self.body,
            "bullet_points": self.bullet_points,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class ModelCardDraft:
    card_id: str
    created_at_utc: str
    card_title: str
    card_version: str
    experiment_id: Optional[str]
    model_family_kind: Optional[BaselineModelFamilyKind]
    sections: List[ModelCardDraftSection]
    rendered_markdown: Optional[str]
    rendered_text: Optional[str]
    card_hash: Optional[str]
    draft_only: bool
    training_not_started: bool
    prediction_not_started: bool
    not_investment_advice: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_id": self.card_id,
            "created_at_utc": self.created_at_utc,
            "card_title": self.card_title,
            "card_version": self.card_version,
            "experiment_id": self.experiment_id,
            "model_family_kind": self.model_family_kind.value if self.model_family_kind else None,
            "sections": [s.to_dict() for s in self.sections],
            "rendered_markdown": self.rendered_markdown,
            "rendered_text": self.rendered_text,
            "card_hash": self.card_hash,
            "draft_only": self.draft_only,
            "training_not_started": self.training_not_started,
            "prediction_not_started": self.prediction_not_started,
            "not_investment_advice": self.not_investment_advice,
            "not_trade_signal": self.not_trade_signal,
            "not_deployment_artifact": self.not_deployment_artifact,
            "research_metadata_only": self.research_metadata_only,
            "investment_advice": self.investment_advice,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class BaselineExperimentRegistry:
    registry_id: str
    created_at_utc: str
    registry_status: ExperimentRegistryStatus
    experiment_specs: List[BaselineExperimentSpec]
    model_family_specs: List[BaselineModelFamilySpec]
    metric_specs: List[EvaluationMetricSpec]
    model_placeholders: List[ModelArtifactPlaceholder]
    model_card_drafts: List[ModelCardDraft]
    experiment_count: int
    registry_hash: Optional[str]
    registry_valid: bool
    quality: BaselineMLScaffoldingQuality
    research_metadata_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    training_started: bool
    prediction_started: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry_id": self.registry_id,
            "created_at_utc": self.created_at_utc,
            "registry_status": self.registry_status.value,
            "experiment_specs": [e.to_dict() for e in self.experiment_specs],
            "model_family_specs": [m.to_dict() for m in self.model_family_specs],
            "metric_specs": [m.to_dict() for m in self.metric_specs],
            "model_placeholders": [m.to_dict() for m in self.model_placeholders],
            "model_card_drafts": [m.to_dict() for m in self.model_card_drafts],
            "experiment_count": self.experiment_count,
            "registry_hash": self.registry_hash,
            "registry_valid": self.registry_valid,
            "quality": self.quality.value,
            "research_metadata_only": self.research_metadata_only,
            "activation_allowed": self.activation_allowed,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "training_started": self.training_started,
            "prediction_started": self.prediction_started,
            "model_training_used": self.model_training_used,
            "model_prediction_used": self.model_prediction_used,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "investment_advice": self.investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class NonActivationEvaluationBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: NonActivationEvaluationRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "created_at_utc": self.created_at_utc,
            "rule_kind": self.rule_kind.value,
            "name": self.name,
            "required": self.required,
            "passed": self.passed,
            "expected_value": self.expected_value,
            "observed_value": self.observed_value,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class NonActivationEvaluationBoundaryResult:
    boundary_result_id: str
    created_at_utc: str
    rules: List[NonActivationEvaluationBoundaryRule]
    boundary_passed: bool
    no_model_training_in_phase138: bool
    no_model_prediction_in_phase138: bool
    no_trade_signal_output: bool
    no_order_decision_output: bool
    no_portfolio_weight_output: bool
    no_strategy_activation: bool
    no_broker_execution: bool
    no_paper_mutation: bool
    no_telegram_real_send: bool
    no_deployment: bool
    no_live_daemon: bool
    no_scheduler: bool
    research_metadata_only: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "boundary_result_id": self.boundary_result_id,
            "created_at_utc": self.created_at_utc,
            "rules": [r.to_dict() for r in self.rules],
            "boundary_passed": self.boundary_passed,
            "no_model_training_in_phase138": self.no_model_training_in_phase138,
            "no_model_prediction_in_phase138": self.no_model_prediction_in_phase138,
            "no_trade_signal_output": self.no_trade_signal_output,
            "no_order_decision_output": self.no_order_decision_output,
            "no_portfolio_weight_output": self.no_portfolio_weight_output,
            "no_strategy_activation": self.no_strategy_activation,
            "no_broker_execution": self.no_broker_execution,
            "no_paper_mutation": self.no_paper_mutation,
            "no_telegram_real_send": self.no_telegram_real_send,
            "no_deployment": self.no_deployment,
            "no_live_daemon": self.no_live_daemon,
            "no_scheduler": self.no_scheduler,
            "research_metadata_only": self.research_metadata_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class BaselineExperimentReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: BaselineScaffoldingReadinessRuleKind
    name: str
    status: BaselineScaffoldingReadinessStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "created_at_utc": self.created_at_utc,
            "rule_kind": self.rule_kind.value,
            "name": self.name,
            "status": self.status.value,
            "required": self.required,
            "passed": self.passed,
            "expected_value": self.expected_value,
            "observed_value": self.observed_value,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class BaselineExperimentReadinessGate:
    gate_id: str
    created_at_utc: str
    status: BaselineScaffoldingReadinessStatus
    rules: List[BaselineExperimentReadinessRule]
    experiment_registry: BaselineExperimentRegistry
    evaluation_harness_contract: EvaluationHarnessContract
    prediction_output_boundary: PredictionOutputBoundary
    non_activation_boundary: NonActivationEvaluationBoundaryResult
    ready_for_phase139: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    training_started: bool
    prediction_started: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "created_at_utc": self.created_at_utc,
            "status": self.status.value,
            "rules": [r.to_dict() for r in self.rules],
            "experiment_registry": self.experiment_registry.to_dict(),
            "evaluation_harness_contract": self.evaluation_harness_contract.to_dict(),
            "prediction_output_boundary": self.prediction_output_boundary.to_dict(),
            "non_activation_boundary": self.non_activation_boundary.to_dict(),
            "ready_for_phase139": self.ready_for_phase139,
            "research_data_only": self.research_data_only,
            "activation_allowed": self.activation_allowed,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "training_started": self.training_started,
            "prediction_started": self.prediction_started,
            "model_training_used": self.model_training_used,
            "model_prediction_used": self.model_prediction_used,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "investment_advice": self.investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class BaselineMLScaffoldingContext:
    context_id: str
    created_at_utc: str
    status: BaselineMLScaffoldingStatus
    decision: BaselineMLScaffoldingDecision
    source_dataset_assembly_review_id: Optional[str]
    ingestion: MLDatasetAssemblyIngestionResult
    model_family_specs: List[BaselineModelFamilySpec]
    experiment_specs: List[BaselineExperimentSpec]
    metric_specs: List[EvaluationMetricSpec]
    evaluation_harness_contract: EvaluationHarnessContract
    prediction_output_boundary: PredictionOutputBoundary
    model_card_drafts: List[ModelCardDraft]
    experiment_registry: BaselineExperimentRegistry
    non_activation_boundary: NonActivationEvaluationBoundaryResult
    readiness_gate: BaselineExperimentReadinessGate
    dataset_assembly_ingested: bool
    dataset_artifacts_loaded: bool
    experiment_specs_built: bool
    model_family_registry_built: bool
    metric_specs_built: bool
    evaluation_harness_contract_built: bool
    prediction_output_boundary_built: bool
    model_card_draft_built: bool
    experiment_registry_built: bool
    non_activation_boundary_validated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase139: bool
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
    daemon_started: bool
    scheduler_enabled: bool
    training_started: bool
    prediction_started: bool
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
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BaselineMLScaffoldingRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "created_at_utc": self.created_at_utc,
            "status": self.status.value,
            "decision": self.decision.value,
            "source_dataset_assembly_review_id": self.source_dataset_assembly_review_id,
            "ingestion": self.ingestion.to_dict() if self.ingestion else None,
            "model_family_specs": [s.to_dict() for s in self.model_family_specs],
            "experiment_specs": [s.to_dict() for s in self.experiment_specs],
            "metric_specs": [s.to_dict() for s in self.metric_specs],
            "evaluation_harness_contract": self.evaluation_harness_contract.to_dict() if self.evaluation_harness_contract else None,
            "prediction_output_boundary": self.prediction_output_boundary.to_dict() if self.prediction_output_boundary else None,
            "model_card_drafts": [s.to_dict() for s in self.model_card_drafts],
            "experiment_registry": self.experiment_registry.to_dict() if self.experiment_registry else None,
            "non_activation_boundary": self.non_activation_boundary.to_dict() if self.non_activation_boundary else None,
            "readiness_gate": self.readiness_gate.to_dict() if self.readiness_gate else None,
            "dataset_assembly_ingested": self.dataset_assembly_ingested,
            "dataset_artifacts_loaded": self.dataset_artifacts_loaded,
            "experiment_specs_built": self.experiment_specs_built,
            "model_family_registry_built": self.model_family_registry_built,
            "metric_specs_built": self.metric_specs_built,
            "evaluation_harness_contract_built": self.evaluation_harness_contract_built,
            "prediction_output_boundary_built": self.prediction_output_boundary_built,
            "model_card_draft_built": self.model_card_draft_built,
            "experiment_registry_built": self.experiment_registry_built,
            "non_activation_boundary_validated": self.non_activation_boundary_validated,
            "readiness_gate_built": self.readiness_gate_built,
            "readiness_gate_passed": self.readiness_gate_passed,
            "ready_for_phase139": self.ready_for_phase139,
            "metadata_only": self.metadata_only,
            "research_data_only": self.research_data_only,
            "activation_allowed": self.activation_allowed,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "active_paper_enabled": self.active_paper_enabled,
            "broker_execution_enabled": self.broker_execution_enabled,
            "order_creation_enabled": self.order_creation_enabled,
            "paper_state_mutation_enabled": self.paper_state_mutation_enabled,
            "telegram_real_send_enabled": self.telegram_real_send_enabled,
            "scraping_enabled": self.scraping_enabled,
            "html_parse_enabled": self.html_parse_enabled,
            "paid_api_enabled": self.paid_api_enabled,
            "dashboard_enabled": self.dashboard_enabled,
            "network_default_enabled": self.network_default_enabled,
            "daemon_started": self.daemon_started,
            "scheduler_enabled": self.scheduler_enabled,
            "training_started": self.training_started,
            "prediction_started": self.prediction_started,
            "model_training_used": self.model_training_used,
            "model_prediction_used": self.model_prediction_used,
            "heavy_ml_dependency_used": self.heavy_ml_dependency_used,
            "produces_trade_signal": self.produces_trade_signal,
            "produces_order_decision": self.produces_order_decision,
            "produces_portfolio_weights": self.produces_portfolio_weights,
            "investment_advice": self.investment_advice,
            "network_used": self.network_used,
            "paid_api_used": self.paid_api_used,
            "scraping_used": self.scraping_used,
            "html_parsing_used": self.html_parsing_used,
            "broker_used": self.broker_used,
            "order_created": self.order_created,
            "paper_state_mutated": self.paper_state_mutated,
            "telegram_real_sent": self.telegram_real_sent,
            "dashboard_started": self.dashboard_started,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class BaselineMLScaffoldingFullReview:
    review_id: str
    created_at_utc: str
    report_type: BaselineMLScaffoldingReportType
    ingestion: MLDatasetAssemblyIngestionResult
    context: BaselineMLScaffoldingContext
    experiment_registry: BaselineExperimentRegistry
    evaluation_harness_contract: EvaluationHarnessContract
    prediction_output_boundary: PredictionOutputBoundary
    non_activation_boundary: NonActivationEvaluationBoundaryResult
    readiness_gate: BaselineExperimentReadinessGate
    output_paths: Dict[str, str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "created_at_utc": self.created_at_utc,
            "report_type": self.report_type.value,
            "ingestion": self.ingestion.to_dict() if self.ingestion else None,
            "context": self.context.to_dict() if self.context else None,
            "experiment_registry": self.experiment_registry.to_dict() if self.experiment_registry else None,
            "evaluation_harness_contract": self.evaluation_harness_contract.to_dict() if self.evaluation_harness_contract else None,
            "prediction_output_boundary": self.prediction_output_boundary.to_dict() if self.prediction_output_boundary else None,
            "non_activation_boundary": self.non_activation_boundary.to_dict() if self.non_activation_boundary else None,
            "readiness_gate": self.readiness_gate.to_dict() if self.readiness_gate else None,
            "output_paths": self.output_paths,
            "warnings": self.warnings,
            "errors": self.errors
        }
