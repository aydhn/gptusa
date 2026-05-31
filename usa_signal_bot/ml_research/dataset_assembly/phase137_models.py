import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import (
    MLDatasetAssemblyStatus,
    MLDatasetAssemblyDecision,
    MLDatasetSourceResolutionStatus,
    MLMatrixKind,
    MLAssemblyMode,
    MLSplitPolicyKind,
    MLSplitName,
    MLLeakageAuditStatus,
    MLLeakageAuditRuleKind,
    MLDatasetQualityKind,
    MLDatasetQualityStatus,
    MLDatasetAssemblyReadinessStatus,
    MLDatasetAssemblyReadinessRuleKind,
    MLDatasetAssemblyQuality,
    MLDatasetAssemblyRiskFlag,
    MLDatasetAssemblyReportType
)
import datetime

@dataclass
class MLFoundationIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
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
    valid_for_phase137: bool
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetSourceReference:
    source_ref_id: str
    created_at_utc: str
    source_name: str
    source_kind: str
    source_path: Optional[str]
    source_hash: Optional[str]
    source_resolution_status: MLDatasetSourceResolutionStatus
    source_artifact_kind: Optional[str]
    row_count: Optional[int]
    column_count: Optional[int]
    available_columns: List[str] = field(default_factory=list)
    required_columns: List[str] = field(default_factory=list)
    missing_columns: List[str] = field(default_factory=list)
    read_only: bool = True
    local_only: bool = True
    research_metadata_only: bool = True
    contains_forbidden_outputs: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLMatrixAssemblySpec:
    spec_id: str
    created_at_utc: str
    matrix_kind: MLMatrixKind
    assembly_mode: MLAssemblyMode
    source_refs: List[MLDatasetSourceReference] = field(default_factory=list)
    required_columns: List[str] = field(default_factory=list)
    excluded_columns: List[str] = field(default_factory=list)
    join_keys: List[str] = field(default_factory=list)
    time_column: str = "timestamp"
    identifier_columns: List[str] = field(default_factory=list)
    output_path: Optional[str] = None
    output_hash_required: bool = True
    deterministic: bool = True
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLMatrixAssemblyResult:
    result_id: str
    created_at_utc: str
    matrix_kind: MLMatrixKind
    assembly_mode: MLAssemblyMode
    row_count: int
    column_count: int
    columns: List[str] = field(default_factory=list)
    identifier_columns: List[str] = field(default_factory=list)
    time_column: Optional[str] = None
    source_ref_ids: List[str] = field(default_factory=list)
    output_path: Optional[str] = None
    output_hash: Optional[str] = None
    missing_value_summary: Dict[str, Any] = field(default_factory=dict)
    duplicate_row_count: int = 0
    assembly_valid: bool = False
    quality: MLDatasetAssemblyQuality = MLDatasetAssemblyQuality.UNKNOWN
    research_metadata_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLAssembledDatasetManifest:
    manifest_id: str
    created_at_utc: str
    manifest_version: str
    feature_matrix: MLMatrixAssemblyResult
    target_matrix: MLMatrixAssemblyResult
    label_matrix: MLMatrixAssemblyResult
    source_refs: List[MLDatasetSourceReference] = field(default_factory=list)
    dataset_contract_hash: Optional[str] = None
    feature_contract_count: int = 0
    target_contract_count: int = 0
    label_contract_count: int = 0
    total_row_count: int = 0
    feature_count: int = 0
    target_count: int = 0
    label_count: int = 0
    common_symbol_count: int = 0
    common_time_range: Dict[str, Any] = field(default_factory=dict)
    manifest_hash: Optional[str] = None
    manifest_valid: bool = False
    quality: MLDatasetAssemblyQuality = MLDatasetAssemblyQuality.UNKNOWN
    research_metadata_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLSplitPolicy:
    policy_id: str
    created_at_utc: str
    policy_kind: MLSplitPolicyKind
    policy_name: str
    train_ratio: Optional[float] = None
    validation_ratio: Optional[float] = None
    test_ratio: Optional[float] = None
    embargo_bars: int = 5
    purge_bars: int = 5
    walk_forward_window_bars: Optional[int] = None
    walk_forward_step_bars: Optional[int] = None
    min_train_bars: Optional[int] = None
    symbol_aware: bool = True
    time_ordered: bool = True
    leakage_safe_required: bool = True
    deterministic: bool = True
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLSplitAssignment:
    assignment_id: str
    created_at_utc: str
    policy_id: str
    split_name_counts: Dict[str, int] = field(default_factory=dict)
    symbol_split_counts: Dict[str, Dict[str, int]] = field(default_factory=dict)
    time_ranges_by_split: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    assignment_path: Optional[str] = None
    assignment_hash: Optional[str] = None
    split_assignment_valid: bool = False
    leakage_safe: bool = False
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLLeakageAuditRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MLLeakageAuditRuleKind
    name: str
    status: MLLeakageAuditStatus
    required: bool
    passed: bool
    severity: str
    expected_value: Optional[Any] = None
    observed_value: Optional[Any] = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLLeakageAuditResult:
    audit_id: str
    created_at_utc: str
    rules: List[MLLeakageAuditRule] = field(default_factory=list)
    total_rules: int = 0
    passed_rules: int = 0
    warning_rules: int = 0
    failed_rules: int = 0
    blocked_rules: int = 0
    leakage_audit_passed: bool = False
    future_data_leakage_detected: bool = False
    target_leakage_detected: bool = False
    label_overlap_detected: bool = False
    timestamp_alignment_issue_detected: bool = False
    train_test_overlap_detected: bool = False
    forward_window_overlap_detected: bool = False
    forbidden_output_detected: bool = False
    research_metadata_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetQualityProfile:
    profile_id: str
    created_at_utc: str
    quality_kind: MLDatasetQualityKind
    status: MLDatasetQualityStatus
    score: float
    metric_snapshot: Dict[str, Any] = field(default_factory=dict)
    diagnostic_notes: List[str] = field(default_factory=list)
    required_human_review: bool = False
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLSplitQualityProfile:
    profile_id: str
    created_at_utc: str
    policy_id: str
    status: MLDatasetQualityStatus
    score: float
    train_count: int = 0
    validation_count: int = 0
    test_count: int = 0
    embargo_count: int = 0
    purged_count: int = 0
    split_balance_notes: List[str] = field(default_factory=list)
    leakage_safety_notes: List[str] = field(default_factory=list)
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetAssemblyReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MLDatasetAssemblyReadinessRuleKind
    name: str
    status: MLDatasetAssemblyReadinessStatus
    required: bool
    passed: bool
    expected_value: Optional[Any] = None
    observed_value: Optional[Any] = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetAssemblyReadinessGate:
    gate_id: str
    created_at_utc: str
    status: MLDatasetAssemblyReadinessStatus
    rules: List[MLDatasetAssemblyReadinessRule] = field(default_factory=list)
    dataset_manifest: Optional[MLAssembledDatasetManifest] = None
    split_policy: Optional[MLSplitPolicy] = None
    split_assignment: Optional[MLSplitAssignment] = None
    leakage_audit: Optional[MLLeakageAuditResult] = None
    dataset_quality_profiles: List[MLDatasetQualityProfile] = field(default_factory=list)
    split_quality_profile: Optional[MLSplitQualityProfile] = None
    ready_for_phase138: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    training_started: bool = False
    prediction_started: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetAssemblyContext:
    context_id: str
    created_at_utc: str
    status: MLDatasetAssemblyStatus
    decision: MLDatasetAssemblyDecision
    source_ml_foundation_review_id: Optional[str] = None
    ingestion: Optional[MLFoundationIngestionResult] = None
    source_refs: List[MLDatasetSourceReference] = field(default_factory=list)
    feature_matrix: Optional[MLMatrixAssemblyResult] = None
    target_matrix: Optional[MLMatrixAssemblyResult] = None
    label_matrix: Optional[MLMatrixAssemblyResult] = None
    dataset_manifest: Optional[MLAssembledDatasetManifest] = None
    split_policy: Optional[MLSplitPolicy] = None
    split_assignment: Optional[MLSplitAssignment] = None
    leakage_audit: Optional[MLLeakageAuditResult] = None
    dataset_quality_profiles: List[MLDatasetQualityProfile] = field(default_factory=list)
    split_quality_profile: Optional[MLSplitQualityProfile] = None
    readiness_gate: Optional[MLDatasetAssemblyReadinessGate] = None
    ml_foundation_ingested: bool = False
    foundation_artifacts_loaded: bool = False
    sources_resolved: bool = False
    feature_matrix_assembled: bool = False
    target_matrix_assembled: bool = False
    label_matrix_assembled: bool = False
    dataset_manifest_built: bool = False
    split_policy_built: bool = False
    split_assignment_built: bool = False
    leakage_audit_completed: bool = False
    dataset_quality_evaluated: bool = False
    split_quality_evaluated: bool = False
    readiness_gate_built: bool = False
    readiness_gate_passed: bool = False
    ready_for_phase138: bool = False
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
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[MLDatasetAssemblyRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetAssemblyFullReview:
    review_id: str
    created_at_utc: str
    report_type: MLDatasetAssemblyReportType
    ingestion: Optional[MLFoundationIngestionResult] = None
    context: Optional[MLDatasetAssemblyContext] = None
    dataset_manifest: Optional[MLAssembledDatasetManifest] = None
    split_policy: Optional[MLSplitPolicy] = None
    split_assignment: Optional[MLSplitAssignment] = None
    leakage_audit: Optional[MLLeakageAuditResult] = None
    dataset_quality_profiles: List[MLDatasetQualityProfile] = field(default_factory=list)
    split_quality_profile: Optional[MLSplitQualityProfile] = None
    readiness_gate: Optional[MLDatasetAssemblyReadinessGate] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_ml_foundation_ingestion_id() -> str:
    return f"mlf_ing_{uuid.uuid4().hex[:12]}"

def create_ml_dataset_source_reference_id() -> str:
    return f"ml_src_{uuid.uuid4().hex[:12]}"

def create_ml_matrix_assembly_spec_id() -> str:
    return f"ml_spec_{uuid.uuid4().hex[:12]}"

def create_ml_matrix_assembly_result_id() -> str:
    return f"ml_res_{uuid.uuid4().hex[:12]}"

def create_ml_assembled_dataset_manifest_id() -> str:
    return f"ml_man_{uuid.uuid4().hex[:12]}"

def create_ml_split_policy_id() -> str:
    return f"ml_pol_{uuid.uuid4().hex[:12]}"

def create_ml_split_assignment_id() -> str:
    return f"ml_asg_{uuid.uuid4().hex[:12]}"

def create_ml_leakage_audit_rule_id() -> str:
    return f"ml_lar_{uuid.uuid4().hex[:12]}"

def create_ml_leakage_audit_result_id() -> str:
    return f"ml_aud_{uuid.uuid4().hex[:12]}"

def create_ml_dataset_quality_profile_id() -> str:
    return f"ml_dqp_{uuid.uuid4().hex[:12]}"

def create_ml_split_quality_profile_id() -> str:
    return f"ml_sqp_{uuid.uuid4().hex[:12]}"

def create_ml_dataset_assembly_readiness_rule_id() -> str:
    return f"ml_rr_{uuid.uuid4().hex[:12]}"

def create_ml_dataset_assembly_readiness_gate_id() -> str:
    return f"ml_gate_{uuid.uuid4().hex[:12]}"

def create_ml_dataset_assembly_context_id() -> str:
    return f"ml_ctx_{uuid.uuid4().hex[:12]}"

def create_ml_dataset_assembly_full_review_id() -> str:
    return f"ml_rev_{uuid.uuid4().hex[:12]}"

from dataclasses import asdict

def ml_foundation_ingestion_result_to_dict(obj: MLFoundationIngestionResult) -> dict:
    return asdict(obj)

def ml_dataset_source_reference_to_dict(obj: MLDatasetSourceReference) -> dict:
    d = asdict(obj)
    d['source_resolution_status'] = obj.source_resolution_status.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_matrix_assembly_spec_to_dict(obj: MLMatrixAssemblySpec) -> dict:
    d = asdict(obj)
    d['matrix_kind'] = obj.matrix_kind.value
    d['assembly_mode'] = obj.assembly_mode.value
    d['source_refs'] = [ml_dataset_source_reference_to_dict(r) for r in obj.source_refs]
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_matrix_assembly_result_to_dict(obj: MLMatrixAssemblyResult) -> dict:
    d = asdict(obj)
    d['matrix_kind'] = obj.matrix_kind.value
    d['assembly_mode'] = obj.assembly_mode.value
    d['quality'] = obj.quality.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_assembled_dataset_manifest_to_dict(obj: MLAssembledDatasetManifest) -> dict:
    d = asdict(obj)
    d['feature_matrix'] = ml_matrix_assembly_result_to_dict(obj.feature_matrix)
    d['target_matrix'] = ml_matrix_assembly_result_to_dict(obj.target_matrix)
    d['label_matrix'] = ml_matrix_assembly_result_to_dict(obj.label_matrix)
    d['source_refs'] = [ml_dataset_source_reference_to_dict(r) for r in obj.source_refs]
    d['quality'] = obj.quality.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_split_policy_to_dict(obj: MLSplitPolicy) -> dict:
    d = asdict(obj)
    d['policy_kind'] = obj.policy_kind.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_split_assignment_to_dict(obj: MLSplitAssignment) -> dict:
    d = asdict(obj)
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_leakage_audit_rule_to_dict(obj: MLLeakageAuditRule) -> dict:
    d = asdict(obj)
    d['rule_kind'] = obj.rule_kind.value
    d['status'] = obj.status.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_leakage_audit_result_to_dict(obj: MLLeakageAuditResult) -> dict:
    d = asdict(obj)
    d['rules'] = [ml_leakage_audit_rule_to_dict(r) for r in obj.rules]
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_dataset_quality_profile_to_dict(obj: MLDatasetQualityProfile) -> dict:
    d = asdict(obj)
    d['quality_kind'] = obj.quality_kind.value
    d['status'] = obj.status.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_split_quality_profile_to_dict(obj: MLSplitQualityProfile) -> dict:
    d = asdict(obj)
    d['status'] = obj.status.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_dataset_assembly_readiness_rule_to_dict(obj: MLDatasetAssemblyReadinessRule) -> dict:
    d = asdict(obj)
    d['rule_kind'] = obj.rule_kind.value
    d['status'] = obj.status.value
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_dataset_assembly_readiness_gate_to_dict(obj: MLDatasetAssemblyReadinessGate) -> dict:
    d = asdict(obj)
    d['status'] = obj.status.value
    d['rules'] = [ml_dataset_assembly_readiness_rule_to_dict(r) for r in obj.rules]
    if obj.dataset_manifest:
        d['dataset_manifest'] = ml_assembled_dataset_manifest_to_dict(obj.dataset_manifest)
    if obj.split_policy:
        d['split_policy'] = ml_split_policy_to_dict(obj.split_policy)
    if obj.split_assignment:
        d['split_assignment'] = ml_split_assignment_to_dict(obj.split_assignment)
    if obj.leakage_audit:
        d['leakage_audit'] = ml_leakage_audit_result_to_dict(obj.leakage_audit)
    d['dataset_quality_profiles'] = [ml_dataset_quality_profile_to_dict(p) for p in obj.dataset_quality_profiles]
    if obj.split_quality_profile:
        d['split_quality_profile'] = ml_split_quality_profile_to_dict(obj.split_quality_profile)
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_dataset_assembly_context_to_dict(obj: MLDatasetAssemblyContext) -> dict:
    d = asdict(obj)
    d['status'] = obj.status.value
    d['decision'] = obj.decision.value
    if obj.ingestion:
        d['ingestion'] = ml_foundation_ingestion_result_to_dict(obj.ingestion)
    d['source_refs'] = [ml_dataset_source_reference_to_dict(r) for r in obj.source_refs]
    if obj.feature_matrix:
        d['feature_matrix'] = ml_matrix_assembly_result_to_dict(obj.feature_matrix)
    if obj.target_matrix:
        d['target_matrix'] = ml_matrix_assembly_result_to_dict(obj.target_matrix)
    if obj.label_matrix:
        d['label_matrix'] = ml_matrix_assembly_result_to_dict(obj.label_matrix)
    if obj.dataset_manifest:
        d['dataset_manifest'] = ml_assembled_dataset_manifest_to_dict(obj.dataset_manifest)
    if obj.split_policy:
        d['split_policy'] = ml_split_policy_to_dict(obj.split_policy)
    if obj.split_assignment:
        d['split_assignment'] = ml_split_assignment_to_dict(obj.split_assignment)
    if obj.leakage_audit:
        d['leakage_audit'] = ml_leakage_audit_result_to_dict(obj.leakage_audit)
    d['dataset_quality_profiles'] = [ml_dataset_quality_profile_to_dict(p) for p in obj.dataset_quality_profiles]
    if obj.split_quality_profile:
        d['split_quality_profile'] = ml_split_quality_profile_to_dict(obj.split_quality_profile)
    if obj.readiness_gate:
        d['readiness_gate'] = ml_dataset_assembly_readiness_gate_to_dict(obj.readiness_gate)
    d['risk_flags'] = [f.value for f in obj.risk_flags]
    return d

def ml_dataset_assembly_full_review_to_dict(obj: MLDatasetAssemblyFullReview) -> dict:
    d = asdict(obj)
    d['report_type'] = obj.report_type.value
    if obj.ingestion:
        d['ingestion'] = ml_foundation_ingestion_result_to_dict(obj.ingestion)
    if obj.context:
        d['context'] = ml_dataset_assembly_context_to_dict(obj.context)
    if obj.dataset_manifest:
        d['dataset_manifest'] = ml_assembled_dataset_manifest_to_dict(obj.dataset_manifest)
    if obj.split_policy:
        d['split_policy'] = ml_split_policy_to_dict(obj.split_policy)
    if obj.split_assignment:
        d['split_assignment'] = ml_split_assignment_to_dict(obj.split_assignment)
    if obj.leakage_audit:
        d['leakage_audit'] = ml_leakage_audit_result_to_dict(obj.leakage_audit)
    d['dataset_quality_profiles'] = [ml_dataset_quality_profile_to_dict(p) for p in obj.dataset_quality_profiles]
    if obj.split_quality_profile:
        d['split_quality_profile'] = ml_split_quality_profile_to_dict(obj.split_quality_profile)
    if obj.readiness_gate:
        d['readiness_gate'] = ml_dataset_assembly_readiness_gate_to_dict(obj.readiness_gate)
    return d
