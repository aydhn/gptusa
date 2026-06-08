from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    PortfolioConstructionStatus,
    PortfolioConstructionDecision,
    PortfolioConstructionInputKind,
    SandboxAllocationMethodKind,
    PortfolioConstructionPolicyKind,
    ConstraintAwareScoreKind,
    PortfolioSandboxDiagnosticKind,
    AllocationSandboxSafetyRuleKind,
    Phase156ReadinessStatus,
    Phase156ReadinessRuleKind,
    PortfolioConstructionRiskFlag,
    PortfolioConstructionReportType
)

def _now_str() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class SizingPrototypeIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    portfolio_foundation_ingested: bool
    inputs_resolved: bool
    sizing_policy_built: bool
    method_contracts_built: bool
    fixed_fractional_sizing_built: bool
    volatility_adjusted_sizing_built: bool
    drawdown_adjusted_sizing_built: bool
    cost_aware_sizing_built: bool
    liquidity_aware_sizing_built: bool
    robustness_adjusted_sizing_built: bool
    comparison_matrix_built: bool
    sizing_diagnostics_built: bool
    sensitivity_report_built: bool
    risk_budget_adherence_built: bool
    safety_boundary_validated: bool
    phase155_readiness_gate_built: bool
    phase155_readiness_gate_passed: bool
    ready_for_phase155: bool
    research_data_only: bool
    sizing_research_prototype_only: bool
    deterministic: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    real_order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    strategy_activation_allowed: bool
    actual_portfolio_construction_executed: bool
    actual_position_sizing_executed: bool
    portfolio_optimization_enabled: bool
    rebalancing_enabled: bool
    target_weights_produced: bool
    allocation_output_produced: bool
    order_size_produced: bool
    capital_deployment_allowed: bool
    deployment_allowed: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    dashboard_started: bool
    daemon_started: bool
    scheduler_enabled: bool
    produces_live_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    valid_for_phase155: bool
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: PortfolioConstructionInputKind
    source_artifact_name: str
    source_path: Optional[str]
    source_hash: Optional[str]
    available: bool
    read_only: bool
    row_count: Optional[int]
    columns: List[str] = field(default_factory=list)
    forbidden_columns_detected: List[str] = field(default_factory=list)
    research_data_only: bool = True
    allocation_sandbox_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioSandboxCandidate:
    candidate_id: str
    created_at_utc: str
    symbol: str
    candidate_valid: bool
    eligible_for_sandbox: bool
    sizing_score: Optional[float]
    risk_budget_score: Optional[float]
    robustness_score: Optional[float]
    liquidity_score: Optional[float]
    cost_score: Optional[float]
    diversification_group: Optional[str]
    sandbox_notes: List[str] = field(default_factory=list)
    live_signal: bool = False
    order_decision: bool = False
    actual_target_weight: Optional[float] = None
    actual_portfolio_weight: Optional[float] = None
    actual_allocation: Optional[float] = None
    actual_position_size: Optional[float] = None
    order_size: Optional[float] = None
    capital_allocation: Optional[float] = None
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionPolicy:
    policy_id: str
    created_at_utc: str
    policy_kind: PortfolioConstructionPolicyKind
    policy_name: str
    max_sandbox_weight_fraction: float
    min_sandbox_weight_fraction: float
    max_group_sandbox_weight_fraction: float
    max_turnover_sandbox_fraction: float
    risk_budget_weight: float
    robustness_weight: float
    sizing_weight: float
    liquidity_weight: float
    cost_weight: float
    diversification_weight: float
    deterministic: bool = True
    policy_valid: bool = True
    research_data_only: bool = True
    allocation_sandbox_only: bool = True
    actual_target_weights_allowed: bool = False
    actual_allocation_allowed: bool = False
    capital_deployment_allowed: bool = False
    portfolio_optimization_allowed: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxAllocationMethodContract:
    contract_id: str
    created_at_utc: str
    method_kind: SandboxAllocationMethodKind
    method_name: str
    enabled: bool
    deterministic: bool = True
    contract_only: bool = True
    produces_sandbox_prototype_weight: bool = True
    produces_actual_target_weight: bool = False
    produces_actual_portfolio_weight: bool = False
    produces_actual_allocation: bool = False
    produces_order_size: bool = False
    produces_capital_allocation: bool = False
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConstraintAwareScore:
    score_id: str
    created_at_utc: str
    symbol: str
    score_kind: ConstraintAwareScoreKind
    raw_score: Optional[float]
    normalized_score: Optional[float]
    penalty_applied: Optional[float]
    score_valid: bool = True
    research_data_only: bool = True
    allocation_sandbox_only: bool = True
    not_investment_advice: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxAllocationResult:
    result_id: str
    created_at_utc: str
    symbol: str
    method_kind: SandboxAllocationMethodKind
    method_name: str
    raw_sandbox_score: Optional[float]
    sandbox_prototype_weight: Optional[float]
    normalized_sandbox_weight: Optional[float]
    group_sandbox_weight: Optional[float]
    constraint_penalty: Optional[float]
    cap_applied: bool
    floor_applied: bool
    zeroed_by_constraint: bool
    result_valid: bool = True
    research_allocation_sandbox: bool = True
    actual_target_weight: Optional[float] = None
    actual_portfolio_weight: Optional[float] = None
    actual_allocation: Optional[float] = None
    actual_position_size: Optional[float] = None
    order_size: Optional[float] = None
    capital_allocation: Optional[float] = None
    live_signal: bool = False
    order_decision: bool = False
    not_investment_advice: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrototypeExposureRecord:
    exposure_id: str
    created_at_utc: str
    symbol: str
    method_kind: SandboxAllocationMethodKind
    sandbox_prototype_weight: Optional[float]
    normalized_sandbox_weight: Optional[float]
    diversification_group: Optional[str]
    group_sandbox_weight: Optional[float]
    exposure_valid: bool = True
    research_exposure_only: bool = True
    actual_exposure: Optional[float] = None
    actual_position_size: Optional[float] = None
    actual_allocation: Optional[float] = None
    order_size: Optional[float] = None
    capital_allocation: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrototypeExposureTable:
    table_id: str
    created_at_utc: str
    records: List[PrototypeExposureRecord]
    symbol_count: int
    method_count: int
    table_hash: Optional[str]
    table_valid: bool = True
    research_exposure_only: bool = True
    no_actual_target_weights: bool = True
    no_actual_portfolio_weights: bool = True
    no_actual_allocation: bool = True
    no_actual_position_size: bool = True
    no_order_size: bool = True
    no_capital_allocation: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioSandboxDiagnosticRecord:
    diagnostic_id: str
    created_at_utc: str
    diagnostic_kind: PortfolioSandboxDiagnosticKind
    value: Any
    diagnostic_notes: List[str] = field(default_factory=list)
    diagnostic_valid: bool = True
    research_sandbox_only: bool = True
    not_investment_advice: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AllocationSandboxComparisonReport:
    report_id: str
    created_at_utc: str
    allocation_results: List[SandboxAllocationResult]
    exposure_table: PrototypeExposureTable
    diagnostics: List[PortfolioSandboxDiagnosticRecord]
    method_count: int
    symbol_count: int
    report_hash: Optional[str]
    report_valid: bool = True
    research_allocation_sandbox: bool = True
    actual_target_weight_detected: bool = False
    actual_portfolio_weight_detected: bool = False
    actual_allocation_detected: bool = False
    actual_position_size_detected: bool = False
    order_size_detected: bool = False
    capital_allocation_detected: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionValidationReport:
    report_id: str
    created_at_utc: str
    policy: PortfolioConstructionPolicy
    method_contracts: List[SandboxAllocationMethodContract]
    comparison_report: AllocationSandboxComparisonReport
    report_valid: bool = True
    construction_sandbox_valid: bool = True
    constraint_compliance_valid: bool = True
    risk_budget_sandbox_valid: bool = True
    diversification_diagnostics_valid: bool = True
    no_actual_target_weights: bool = True
    no_actual_allocation: bool = True
    no_capital_deployment: bool = True
    no_order_output: bool = True
    no_broker_execution: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AllocationSandboxSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: AllocationSandboxSafetyRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AllocationSandboxSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[AllocationSandboxSafetyBoundaryRule]
    boundary_passed: bool
    research_allocation_sandbox_only: bool = True
    read_only_sizing_artifacts: bool = True
    no_actual_target_weights: bool = True
    no_actual_portfolio_weights: bool = True
    no_actual_allocation: bool = True
    no_actual_position_size: bool = True
    no_order_size: bool = True
    no_capital_deployment: bool = True
    no_portfolio_optimization: bool = True
    no_rebalancing_execution: bool = True
    no_live_trading: bool = True
    no_paper_trading: bool = True
    no_broker_execution: bool = True
    no_real_order_creation: bool = True
    no_paper_state_mutation: bool = True
    no_telegram_real_send: bool = True
    no_strategy_activation: bool = True
    no_deployment: bool = True
    no_network: bool = True
    no_dashboard: bool = True
    no_daemon: bool = True
    no_scheduler: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase156ReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: Phase156ReadinessRuleKind
    name: str
    status: Phase156ReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase156ReadinessGate:
    gate_id: str
    created_at_utc: str
    status: Phase156ReadinessStatus
    rules: List[Phase156ReadinessRule]
    policy: PortfolioConstructionPolicy
    method_contracts: List[SandboxAllocationMethodContract]
    comparison_report: AllocationSandboxComparisonReport
    validation_report: PortfolioConstructionValidationReport
    safety_boundary: AllocationSandboxSafetyBoundaryResult
    ready_for_phase156: bool = False
    research_data_only: bool = True
    allocation_sandbox_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    actual_target_weights_produced: bool = False
    actual_allocation_produced: bool = False
    actual_position_size_produced: bool = False
    order_size_produced: bool = False
    capital_deployment_allowed: bool = False
    portfolio_optimization_enabled: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionContext:
    context_id: str
    created_at_utc: str
    status: PortfolioConstructionStatus
    decision: PortfolioConstructionDecision
    source_sizing_prototype_review_id: Optional[str]
    ingestion: SizingPrototypeIngestionResult
    input_references: List[PortfolioConstructionInputReference] = field(default_factory=list)
    candidates: List[PortfolioSandboxCandidate] = field(default_factory=list)
    policy: Optional[PortfolioConstructionPolicy] = None
    method_contracts: List[SandboxAllocationMethodContract] = field(default_factory=list)
    scores: List[ConstraintAwareScore] = field(default_factory=list)
    allocation_results: List[SandboxAllocationResult] = field(default_factory=list)
    exposure_table: Optional[PrototypeExposureTable] = None
    diagnostics: List[PortfolioSandboxDiagnosticRecord] = field(default_factory=list)
    comparison_report: Optional[AllocationSandboxComparisonReport] = None
    validation_report: Optional[PortfolioConstructionValidationReport] = None
    safety_boundary: Optional[AllocationSandboxSafetyBoundaryResult] = None
    phase156_readiness_gate: Optional[Phase156ReadinessGate] = None
    sizing_prototype_ingested: bool = False
    artifacts_loaded: bool = False
    inputs_resolved: bool = False
    sandbox_candidates_built: bool = False
    construction_policy_built: bool = False
    method_contracts_built: bool = False
    constraint_aware_scores_built: bool = False
    equal_sandbox_allocation_built: bool = False
    sizing_score_sandbox_allocation_built: bool = False
    risk_budget_sandbox_allocation_built: bool = False
    robustness_sandbox_allocation_built: bool = False
    constraint_normalization_built: bool = False
    prototype_exposure_table_built: bool = False
    diversification_diagnostics_built: bool = False
    concentration_diagnostics_built: bool = False
    turnover_diagnostics_built: bool = False
    constraint_breach_diagnostics_built: bool = False
    risk_budget_sandbox_diagnostics_built: bool = False
    allocation_comparison_report_built: bool = False
    construction_validation_report_built: bool = False
    safety_boundary_validated: bool = False
    phase156_readiness_gate_built: bool = False
    phase156_readiness_gate_passed: bool = False
    ready_for_phase156: bool = False
    research_data_only: bool = True
    allocation_sandbox_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    actual_target_weights_produced: bool = False
    actual_portfolio_weights_produced: bool = False
    actual_allocation_produced: bool = False
    actual_position_size_produced: bool = False
    order_size_produced: bool = False
    capital_deployment_allowed: bool = False
    portfolio_optimization_enabled: bool = False
    rebalancing_execution_enabled: bool = False
    deployment_allowed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    produces_live_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[PortfolioConstructionRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionFullReview:
    review_id: str
    created_at_utc: str
    report_type: PortfolioConstructionReportType
    ingestion: SizingPrototypeIngestionResult
    context: PortfolioConstructionContext
    policy: PortfolioConstructionPolicy
    comparison_report: AllocationSandboxComparisonReport
    validation_report: PortfolioConstructionValidationReport
    safety_boundary: AllocationSandboxSafetyBoundaryResult
    phase156_readiness_gate: Phase156ReadinessGate
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_sizing_prototype_ingestion_id() -> str:
    return f"spi_{uuid.uuid4().hex[:8]}"

def create_portfolio_construction_input_reference_id() -> str:
    return f"pcinp_{uuid.uuid4().hex[:8]}"

def create_portfolio_sandbox_candidate_id() -> str:
    return f"cand_{uuid.uuid4().hex[:8]}"

def create_portfolio_construction_policy_id() -> str:
    return f"pcp_{uuid.uuid4().hex[:8]}"

def create_sandbox_allocation_method_contract_id() -> str:
    return f"samc_{uuid.uuid4().hex[:8]}"

def create_constraint_aware_score_id() -> str:
    return f"cas_{uuid.uuid4().hex[:8]}"

def create_sandbox_allocation_result_id() -> str:
    return f"sar_{uuid.uuid4().hex[:8]}"

def create_prototype_exposure_record_id() -> str:
    return f"per_{uuid.uuid4().hex[:8]}"

def create_prototype_exposure_table_id() -> str:
    return f"pet_{uuid.uuid4().hex[:8]}"

def create_portfolio_sandbox_diagnostic_id() -> str:
    return f"psd_{uuid.uuid4().hex[:8]}"

def create_allocation_sandbox_comparison_report_id() -> str:
    return f"ascr_{uuid.uuid4().hex[:8]}"

def create_portfolio_construction_validation_report_id() -> str:
    return f"pcvr_{uuid.uuid4().hex[:8]}"

def create_allocation_sandbox_safety_boundary_rule_id() -> str:
    return f"sbr_{uuid.uuid4().hex[:8]}"

def create_allocation_sandbox_safety_boundary_result_id() -> str:
    return f"assb_{uuid.uuid4().hex[:8]}"

def create_phase156_readiness_rule_id() -> str:
    return f"p156rr_{uuid.uuid4().hex[:8]}"

def create_phase156_readiness_gate_id() -> str:
    return f"p156g_{uuid.uuid4().hex[:8]}"

def create_portfolio_construction_context_id() -> str:
    return f"pcc_{uuid.uuid4().hex[:8]}"

def create_portfolio_construction_full_review_id() -> str:
    return f"pcfr_{uuid.uuid4().hex[:8]}"
