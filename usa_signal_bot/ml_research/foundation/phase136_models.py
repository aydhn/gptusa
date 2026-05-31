from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from ...core.enums import (
    MLFoundationStatus, MLFoundationDecision, MLSourceArtifactKind, MLDatasetContractKind,
    MLFeatureRole, MLTargetKind, MLLabelKind, MLLeakageGuardKind, MLNonActivationRuleKind,
    MLResearchGovernanceRuleKind, MLFoundationReadinessStatus, MLFoundationReadinessRuleKind,
    MLFoundationQuality, MLFoundationRiskFlag, MLFoundationReportType
)
import uuid

@dataclass
class RegimeFinalClosureIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    research_freeze_ingested: bool
    artifact_chain_loaded: bool
    artifact_chain_validated: bool
    final_closure_validated: bool
    freeze_seal_created: bool
    final_safety_audit_passed: bool
    ml_input_contract_built: bool
    ml_kickoff_gate_built: bool
    ml_kickoff_gate_passed: bool
    ready_for_phase136: bool
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
    valid_for_phase136: bool
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLSourceArtifactReference:
    reference_id: str
    created_at_utc: str
    artifact_kind: MLSourceArtifactKind
    artifact_name: str
    source_phase: int
    source_path: Optional[str]
    source_hash: Optional[str]
    schema_signature: Optional[str]
    lineage_reference: Optional[str]
    required: bool
    available: bool
    read_only: bool
    frozen: bool
    allowed_for_ml_research: bool
    contains_features: bool
    contains_targets: bool
    contains_labels: bool
    contains_trade_signals: bool
    contains_order_decisions: bool
    contains_portfolio_weights: bool
    research_metadata_only: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLSourceRegistry:
    registry_id: str
    created_at_utc: str
    source_references: List[MLSourceArtifactReference]
    required_source_count: int
    available_required_source_count: int
    missing_required_source_count: int
    registry_hash: Optional[str]
    registry_valid: bool
    quality: MLFoundationQuality
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
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLFeatureContract:
    contract_id: str
    created_at_utc: str
    feature_name: str
    feature_role: MLFeatureRole
    source_artifact_kind: MLSourceArtifactKind
    source_column: Optional[str]
    dtype_hint: Optional[str]
    nullable_allowed: bool
    missing_value_policy: str
    scaling_allowed_later: bool
    feature_selection_allowed_later: bool
    read_only_source: bool
    leakage_sensitive: bool
    allowed_for_phase137_dataset_assembly: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLTargetContract:
    contract_id: str
    created_at_utc: str
    target_name: str
    target_kind: MLTargetKind
    horizon_bars: Optional[int]
    horizon_calendar_days: Optional[int]
    source_column: Optional[str]
    target_formula_description: str
    target_directional_language_allowed: bool
    trade_signal_semantics_allowed: bool
    order_semantics_allowed: bool
    portfolio_semantics_allowed: bool
    leakage_sensitive: bool
    allowed_for_phase137_dataset_assembly: bool
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLLabelContract:
    contract_id: str
    created_at_utc: str
    label_name: str
    label_kind: MLLabelKind
    source_column: Optional[str]
    label_description: str
    class_values: List[str]
    trade_signal_semantics_allowed: bool
    order_semantics_allowed: bool
    portfolio_semantics_allowed: bool
    leakage_sensitive: bool
    allowed_for_phase137_dataset_assembly: bool
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetContract:
    dataset_contract_id: str
    created_at_utc: str
    contract_kind: MLDatasetContractKind
    contract_version: str
    source_registry: MLSourceRegistry
    feature_contracts: List[MLFeatureContract]
    target_contracts: List[MLTargetContract]
    label_contracts: List[MLLabelContract]
    forbidden_output_fields: List[str]
    required_identifier_columns: List[str]
    required_time_columns: List[str]
    allowed_join_keys: List[str]
    split_design_deferred_to_phase137: bool
    dataset_assembly_deferred_to_phase137: bool
    model_training_deferred: bool
    model_prediction_deferred: bool
    contract_hash: Optional[str]
    contract_valid: bool
    quality: MLFoundationQuality
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
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLLeakageGuardRule:
    rule_id: str
    created_at_utc: str
    guard_kind: MLLeakageGuardKind
    name: str
    required: bool
    passed: bool
    severity: str
    description: str
    phase137_check_required: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLLeakageGuardResult:
    result_id: str
    created_at_utc: str
    rules: List[MLLeakageGuardRule]
    total_rules: int
    passed_rules: int
    warning_rules: int
    failed_rules: int
    blocked_rules: int
    leakage_guard_passed: bool
    phase137_audit_required: bool
    research_metadata_only: bool
    activation_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLNonActivationBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MLNonActivationRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLNonActivationBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[MLNonActivationBoundaryRule]
    boundary_passed: bool
    no_trade_signal_output: bool
    no_order_decision_output: bool
    no_portfolio_weight_output: bool
    no_strategy_activation: bool
    no_broker_execution: bool
    no_paper_mutation: bool
    no_telegram_real_send: bool
    no_deployment: bool
    no_model_training_in_phase136: bool
    no_model_prediction_in_phase136: bool
    no_live_daemon: bool
    no_scheduler: bool
    research_metadata_only: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLResearchGovernanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MLResearchGovernanceRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLResearchGovernanceResult:
    governance_id: str
    created_at_utc: str
    rules: List[MLResearchGovernanceRule]
    governance_passed: bool
    local_only: bool
    free_data_only: bool
    frozen_inputs_read_only: bool
    dataset_contract_required: bool
    leakage_guard_required: bool
    reproducible_artifacts_required: bool
    deterministic_hashing_required: bool
    safety_boundary_required: bool
    no_secret_required: bool
    no_network_by_default: bool
    no_heavy_ml_dependency_in_phase136: bool
    research_metadata_only: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLFoundationReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MLFoundationReadinessRuleKind
    name: str
    status: MLFoundationReadinessStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLFoundationReadinessGate:
    gate_id: str
    created_at_utc: str
    status: MLFoundationReadinessStatus
    rules: List[MLFoundationReadinessRule]
    dataset_contract: MLDatasetContract
    leakage_guard: MLLeakageGuardResult
    non_activation_boundary: MLNonActivationBoundaryResult
    governance: MLResearchGovernanceResult
    ready_for_phase137: bool
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
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLFoundationContext:
    context_id: str
    created_at_utc: str
    status: MLFoundationStatus
    decision: MLFoundationDecision
    source_final_closure_review_id: Optional[str]
    ingestion: RegimeFinalClosureIngestionResult
    source_registry: MLSourceRegistry
    feature_contracts: List[MLFeatureContract]
    target_contracts: List[MLTargetContract]
    label_contracts: List[MLLabelContract]
    dataset_contract: MLDatasetContract
    leakage_guard: MLLeakageGuardResult
    non_activation_boundary: MLNonActivationBoundaryResult
    governance: MLResearchGovernanceResult
    readiness_gate: MLFoundationReadinessGate
    final_closure_ingested: bool
    final_closure_artifacts_loaded: bool
    source_registry_built: bool
    feature_contract_built: bool
    target_contract_built: bool
    label_contract_built: bool
    dataset_contract_built: bool
    leakage_guard_built: bool
    non_activation_boundary_validated: bool
    governance_built: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase137: bool
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
    risk_flags: List[MLFoundationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLFoundationFullReview:
    review_id: str
    created_at_utc: str
    report_type: MLFoundationReportType
    ingestion: RegimeFinalClosureIngestionResult
    context: MLFoundationContext
    source_registry: MLSourceRegistry
    dataset_contract: MLDatasetContract
    leakage_guard: MLLeakageGuardResult
    non_activation_boundary: MLNonActivationBoundaryResult
    governance: MLResearchGovernanceResult
    readiness_gate: MLFoundationReadinessGate
    output_paths: Dict[str, str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_regime_final_closure_ingestion_id() -> str:
    return f"ingest-{uuid.uuid4()}"
def create_ml_source_artifact_reference_id() -> str:
    return f"ref-{uuid.uuid4()}"
def create_ml_source_registry_id() -> str:
    return f"reg-{uuid.uuid4()}"
def create_ml_feature_contract_id() -> str:
    return f"feat-{uuid.uuid4()}"
def create_ml_target_contract_id() -> str:
    return f"target-{uuid.uuid4()}"
def create_ml_label_contract_id() -> str:
    return f"label-{uuid.uuid4()}"
def create_ml_dataset_contract_id() -> str:
    return f"ds-{uuid.uuid4()}"
def create_ml_leakage_guard_rule_id() -> str:
    return f"lg-rule-{uuid.uuid4()}"
def create_ml_leakage_guard_result_id() -> str:
    return f"lg-res-{uuid.uuid4()}"
def create_ml_non_activation_boundary_rule_id() -> str:
    return f"nab-rule-{uuid.uuid4()}"
def create_ml_non_activation_boundary_result_id() -> str:
    return f"nab-res-{uuid.uuid4()}"
def create_ml_research_governance_rule_id() -> str:
    return f"gov-rule-{uuid.uuid4()}"
def create_ml_research_governance_result_id() -> str:
    return f"gov-res-{uuid.uuid4()}"
def create_ml_foundation_readiness_rule_id() -> str:
    return f"gate-rule-{uuid.uuid4()}"
def create_ml_foundation_readiness_gate_id() -> str:
    return f"gate-{uuid.uuid4()}"
def create_ml_foundation_context_id() -> str:
    return f"ctx-{uuid.uuid4()}"
def create_ml_foundation_full_review_id() -> str:
    return f"rev-{uuid.uuid4()}"
