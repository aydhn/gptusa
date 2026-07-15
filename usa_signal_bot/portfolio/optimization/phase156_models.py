import uuid
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Dict, List, Tuple
from usa_signal_bot.core.enums import (
    OptimizerPrototypeStatus, OptimizerPrototypeDecision, OptimizerInputKind, OptimizerMethodKind,
    OptimizerPolicyKind, OptimizerObjectiveKind, OptimizerConstraintKind, OptimizerDiagnosticKind,
    OptimizerSafetyRuleKind, Phase157ReadinessStatus, Phase157ReadinessRuleKind,
    OptimizerPrototypeQuality, OptimizerPrototypeRiskFlag, OptimizerPrototypeReportType
)


def _gen_uuid() -> str:
    return str(uuid.uuid4())

def _now_utc() -> str:
    return datetime.utcnow().isoformat() + "Z"


@dataclass
class PortfolioConstructionIngestionResult:
    ingestion_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    source_path: Optional[str] = None
    source_review_id: Optional[str] = None
    source_context_id: Optional[str] = None
    available: bool = False
    sizing_prototype_ingested: bool = False
    inputs_resolved: bool = False
    sandbox_candidates_built: bool = False
    construction_policy_built: bool = False
    method_contracts_built: bool = False
    constraint_aware_scores_built: bool = False
    equal_sandbox_allocation_built: bool = False
    sizing_score_sandbox_allocation_built: bool = False
    risk_budget_sandbox_allocation_built: bool = False
    robustness_sandbox_allocation_built: bool = False
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
    research_data_only: bool = False
    allocation_sandbox_only: bool = False
    deterministic: bool = False
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
    valid_for_phase156: bool = False
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerInputReference:
    input_ref_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    input_kind: OptimizerInputKind = OptimizerInputKind.UNKNOWN
    source_artifact_name: str = ""
    source_path: Optional[str] = None
    source_hash: Optional[str] = None
    available: bool = False
    read_only: bool = False
    row_count: Optional[int] = None
    columns: List[str] = field(default_factory=list)
    forbidden_columns_detected: List[str] = field(default_factory=list)
    research_data_only: bool = False
    optimizer_sandbox_only: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerSandboxCandidate:
    candidate_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    symbol: str = ""
    candidate_valid: bool = False
    eligible_for_optimizer_sandbox: bool = False
    sandbox_score: Optional[float] = None
    risk_budget_score: Optional[float] = None
    robustness_score: Optional[float] = None
    liquidity_score: Optional[float] = None
    cost_score: Optional[float] = None
    concentration_group: Optional[str] = None
    previous_sandbox_weight: Optional[float] = None
    live_signal: bool = False
    order_decision: bool = False
    actual_target_weight: Optional[float] = None
    actual_portfolio_weight: Optional[float] = None
    actual_allocation: Optional[float] = None
    actual_position_size: Optional[float] = None
    order_size: Optional[float] = None
    capital_allocation: Optional[float] = None
    research_data_only: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerPolicy:
    policy_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    policy_kind: OptimizerPolicyKind = OptimizerPolicyKind.UNKNOWN
    policy_name: str = ""
    max_sandbox_optimizer_weight: float = 0.0
    min_sandbox_optimizer_weight: float = 0.0
    max_group_sandbox_optimizer_weight: float = 0.0
    max_turnover_sandbox: float = 0.0
    max_risk_budget_usage: float = 0.0
    score_objective_weight: float = 0.0
    concentration_objective_weight: float = 0.0
    risk_budget_objective_weight: float = 0.0
    robustness_objective_weight: float = 0.0
    turnover_objective_weight: float = 0.0
    deterministic: bool = False
    policy_valid: bool = False
    research_data_only: bool = False
    optimizer_sandbox_only: bool = False
    actual_target_weights_allowed: bool = False
    actual_allocation_allowed: bool = False
    capital_deployment_allowed: bool = False
    actual_portfolio_optimization_allowed: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerObjectiveContract:
    contract_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    objective_kind: OptimizerObjectiveKind = OptimizerObjectiveKind.UNKNOWN
    objective_name: str = ""
    enabled: bool = False
    deterministic: bool = False
    contract_only: bool = False
    weight_in_composite: float = 0.0
    produces_objective_score: bool = False
    produces_actual_target_weight: bool = False
    produces_actual_allocation: bool = False
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerConstraintContract:
    contract_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    constraint_kind: OptimizerConstraintKind = OptimizerConstraintKind.UNKNOWN
    constraint_name: str = ""
    enabled: bool = False
    deterministic: bool = False
    contract_only: bool = False
    limit_value: Optional[Any] = None
    produces_actual_target_weight: bool = False
    produces_actual_allocation: bool = False
    produces_order_size: bool = False
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerSandboxResult:
    result_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    symbol: str = ""
    method_kind: OptimizerMethodKind = OptimizerMethodKind.UNKNOWN
    method_name: str = ""
    raw_optimizer_score: Optional[float] = None
    sandbox_optimizer_weight: Optional[float] = None
    normalized_sandbox_optimizer_weight: Optional[float] = None
    group_sandbox_optimizer_weight: Optional[float] = None
    objective_score: Optional[float] = None
    constraint_penalty: Optional[float] = None
    cap_applied: bool = False
    floor_applied: bool = False
    zeroed_by_constraint: bool = False
    result_valid: bool = False
    optimization_research_sandbox: bool = False
    actual_target_weight: Optional[float] = None
    actual_portfolio_weight: Optional[float] = None
    actual_allocation: Optional[float] = None
    actual_position_size: Optional[float] = None
    order_size: Optional[float] = None
    capital_allocation: Optional[float] = None
    live_signal: bool = False
    order_decision: bool = False
    not_investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerObjectiveScore:
    score_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    method_kind: OptimizerMethodKind = OptimizerMethodKind.UNKNOWN
    objective_kind: OptimizerObjectiveKind = OptimizerObjectiveKind.UNKNOWN
    value: Optional[Any] = None
    score_valid: bool = False
    research_sandbox_only: bool = False
    not_investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class ObjectiveComparisonReport:
    report_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    optimizer_results: List[OptimizerSandboxResult] = field(default_factory=list)
    objective_scores: List[OptimizerObjectiveScore] = field(default_factory=list)
    method_count: int = 0
    symbol_count: int = 0
    best_method_by_objective: Dict[str, str] = field(default_factory=dict)
    report_hash: Optional[str] = None
    report_valid: bool = False
    optimization_research_sandbox: bool = False
    actual_target_weight_detected: bool = False
    actual_portfolio_weight_detected: bool = False
    actual_allocation_detected: bool = False
    actual_position_size_detected: bool = False
    order_size_detected: bool = False
    capital_allocation_detected: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerDiagnosticRecord:
    diagnostic_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    diagnostic_kind: OptimizerDiagnosticKind = OptimizerDiagnosticKind.UNKNOWN
    method_kind: Optional[OptimizerMethodKind] = None
    value: Optional[Any] = None
    diagnostic_notes: List[str] = field(default_factory=list)
    diagnostic_valid: bool = False
    research_sandbox_only: bool = False
    not_investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerValidationReport:
    report_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    policy: OptimizerPolicy = field(default_factory=OptimizerPolicy)
    objective_contracts: List[OptimizerObjectiveContract] = field(default_factory=list)
    constraint_contracts: List[OptimizerConstraintContract] = field(default_factory=list)
    comparison_report: ObjectiveComparisonReport = field(default_factory=ObjectiveComparisonReport)
    diagnostics: List[OptimizerDiagnosticRecord] = field(default_factory=list)
    report_valid: bool = False
    optimizer_sandbox_valid: bool = False
    objective_comparison_valid: bool = False
    constraint_compliance_valid: bool = False
    no_actual_target_weights: bool = False
    no_actual_allocation: bool = False
    no_capital_deployment: bool = False
    no_order_output: bool = False
    no_broker_execution: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerSafetyBoundaryRule:
    rule_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    rule_kind: OptimizerSafetyRuleKind = OptimizerSafetyRuleKind.UNKNOWN
    name: str = ""
    required: bool = False
    passed: bool = False
    expected_value: Optional[Any] = None
    observed_value: Optional[Any] = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerSafetyBoundaryResult:
    boundary_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    rules: List[OptimizerSafetyBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    optimizer_sandbox_only: bool = False
    read_only_construction_artifacts: bool = False
    no_actual_target_weights: bool = False
    no_actual_portfolio_weights: bool = False
    no_actual_allocation: bool = False
    no_actual_position_size: bool = False
    no_order_size: bool = False
    no_capital_deployment: bool = False
    no_actual_portfolio_optimization: bool = False
    no_rebalancing_execution: bool = False
    no_live_trading: bool = False
    no_paper_trading: bool = False
    no_broker_execution: bool = False
    no_real_order_creation: bool = False
    no_paper_state_mutation: bool = False
    no_telegram_real_send: bool = False
    no_strategy_activation: bool = False
    no_deployment: bool = False
    no_network: bool = False
    no_dashboard: bool = False
    no_daemon: bool = False
    no_scheduler: bool = False
    research_data_only: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class Phase157ReadinessRule:
    rule_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    rule_kind: Phase157ReadinessRuleKind = Phase157ReadinessRuleKind.UNKNOWN
    name: str = ""
    status: Phase157ReadinessStatus = Phase157ReadinessStatus.UNKNOWN
    required: bool = False
    passed: bool = False
    expected_value: Optional[Any] = None
    observed_value: Optional[Any] = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class Phase157ReadinessGate:
    gate_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    status: Phase157ReadinessStatus = Phase157ReadinessStatus.UNKNOWN
    rules: List[Phase157ReadinessRule] = field(default_factory=list)
    policy: OptimizerPolicy = field(default_factory=OptimizerPolicy)
    comparison_report: ObjectiveComparisonReport = field(default_factory=ObjectiveComparisonReport)
    validation_report: OptimizerValidationReport = field(default_factory=OptimizerValidationReport)
    safety_boundary: OptimizerSafetyBoundaryResult = field(default_factory=OptimizerSafetyBoundaryResult)
    ready_for_phase157: bool = False
    research_data_only: bool = False
    optimizer_sandbox_only: bool = False
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
    actual_portfolio_optimization_enabled: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerPrototypeContext:
    context_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    status: OptimizerPrototypeStatus = OptimizerPrototypeStatus.UNKNOWN
    decision: OptimizerPrototypeDecision = OptimizerPrototypeDecision.UNKNOWN
    source_portfolio_construction_review_id: Optional[str] = None
    ingestion: PortfolioConstructionIngestionResult = field(default_factory=PortfolioConstructionIngestionResult)
    input_references: List[OptimizerInputReference] = field(default_factory=list)
    candidates: List[OptimizerSandboxCandidate] = field(default_factory=list)
    policy: OptimizerPolicy = field(default_factory=OptimizerPolicy)
    objective_contracts: List[OptimizerObjectiveContract] = field(default_factory=list)
    constraint_contracts: List[OptimizerConstraintContract] = field(default_factory=list)
    optimizer_results: List[OptimizerSandboxResult] = field(default_factory=list)
    objective_scores: List[OptimizerObjectiveScore] = field(default_factory=list)
    comparison_report: ObjectiveComparisonReport = field(default_factory=ObjectiveComparisonReport)
    diagnostics: List[OptimizerDiagnosticRecord] = field(default_factory=list)
    validation_report: OptimizerValidationReport = field(default_factory=OptimizerValidationReport)
    safety_boundary: OptimizerSafetyBoundaryResult = field(default_factory=OptimizerSafetyBoundaryResult)
    phase157_readiness_gate: Phase157ReadinessGate = field(default_factory=Phase157ReadinessGate)
    portfolio_construction_ingested: bool = False
    artifacts_loaded: bool = False
    inputs_resolved: bool = False
    optimizer_candidates_built: bool = False
    optimizer_policy_built: bool = False
    objective_contracts_built: bool = False
    constraint_contracts_built: bool = False
    equal_baseline_optimizer_built: bool = False
    score_maximizing_optimizer_built: bool = False
    risk_budget_optimizer_built: bool = False
    concentration_minimizing_optimizer_built: bool = False
    robustness_first_optimizer_built: bool = False
    turnover_aware_optimizer_built: bool = False
    sandbox_weight_normalization_built: bool = False
    objective_scores_built: bool = False
    objective_comparison_report_built: bool = False
    optimizer_diagnostics_built: bool = False
    optimizer_validation_report_built: bool = False
    safety_boundary_validated: bool = False
    phase157_readiness_gate_built: bool = False
    phase157_readiness_gate_passed: bool = False
    ready_for_phase157: bool = False
    research_data_only: bool = False
    optimizer_sandbox_only: bool = False
    deterministic: bool = False
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
    actual_portfolio_optimization_enabled: bool = False
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
    risk_flags: List[OptimizerPrototypeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


@dataclass
class OptimizerPrototypeFullReview:
    review_id: str = field(default_factory=_gen_uuid)
    created_at_utc: str = field(default_factory=_now_utc)
    report_type: OptimizerPrototypeReportType = OptimizerPrototypeReportType.FULL_PHASE156_REVIEW
    ingestion: PortfolioConstructionIngestionResult = field(default_factory=PortfolioConstructionIngestionResult)
    context: OptimizerPrototypeContext = field(default_factory=OptimizerPrototypeContext)
    policy: OptimizerPolicy = field(default_factory=OptimizerPolicy)
    comparison_report: ObjectiveComparisonReport = field(default_factory=ObjectiveComparisonReport)
    validation_report: OptimizerValidationReport = field(default_factory=OptimizerValidationReport)
    safety_boundary: OptimizerSafetyBoundaryResult = field(default_factory=OptimizerSafetyBoundaryResult)
    phase157_readiness_gate: Phase157ReadinessGate = field(default_factory=Phase157ReadinessGate)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict: return asdict(self)

# ID generators
def create_portfolio_construction_ingestion_id() -> str: return _gen_uuid()
def create_optimizer_input_reference_id() -> str: return _gen_uuid()
def create_optimizer_sandbox_candidate_id() -> str: return _gen_uuid()
def create_optimizer_policy_id() -> str: return _gen_uuid()
def create_optimizer_objective_contract_id() -> str: return _gen_uuid()
def create_optimizer_constraint_contract_id() -> str: return _gen_uuid()
def create_optimizer_sandbox_result_id() -> str: return _gen_uuid()
def create_optimizer_objective_score_id() -> str: return _gen_uuid()
def create_objective_comparison_report_id() -> str: return _gen_uuid()
def create_optimizer_diagnostic_id() -> str: return _gen_uuid()
def create_optimizer_validation_report_id() -> str: return _gen_uuid()
def create_optimizer_safety_boundary_rule_id() -> str: return _gen_uuid()
def create_optimizer_safety_boundary_result_id() -> str: return _gen_uuid()
def create_phase157_readiness_rule_id() -> str: return _gen_uuid()
def create_phase157_readiness_gate_id() -> str: return _gen_uuid()
def create_optimizer_prototype_context_id() -> str: return _gen_uuid()
def create_optimizer_prototype_full_review_id() -> str: return _gen_uuid()


# Validation functions (stubs enforcing no-execution constraints)
def validate_portfolio_construction_ingestion(r: PortfolioConstructionIngestionResult) -> List[str]:
    checks = [
        (not r.ready_for_phase156, "Ingestion not ready for Phase 156"),
        (not r.research_data_only, "Not strictly research_data_only"),
        (not r.allocation_sandbox_only, "Not strictly sandbox_only"),
        (not r.deterministic, "Not deterministic"),
        (r.live_trading_enabled, "Live trading enabled"),
        (r.paper_trading_enabled, "Paper trading enabled"),
        (r.broker_execution_enabled, "Broker execution enabled"),
        (r.real_order_creation_enabled, "Real order creation enabled"),
        (r.paper_state_mutation_enabled, "Paper state mutation enabled"),
        (r.telegram_real_send_enabled, "Telegram real send enabled"),
        (r.strategy_activation_allowed, "Strategy activation allowed"),
        (r.actual_target_weights_produced, "Actual target weights produced"),
        (r.actual_portfolio_weights_produced, "Actual portfolio weights produced"),
        (r.actual_allocation_produced, "Actual allocation produced"),
        (r.actual_position_size_produced, "Actual position size produced"),
        (r.order_size_produced, "Order size produced"),
        (r.capital_deployment_allowed, "Capital deployment allowed"),
        (r.portfolio_optimization_enabled, "Actual portfolio optimization enabled"),
        (r.rebalancing_execution_enabled, "Rebalancing execution enabled"),
        (r.deployment_allowed, "Deployment allowed"),
        (r.network_used, "Network used"),
        (r.paid_api_used, "Paid API used"),
        (r.scraping_used, "Scraping used"),
        (r.html_parsing_used, "HTML parsing used"),
        (r.dashboard_started, "Dashboard started"),
        (r.daemon_started, "Daemon started"),
        (r.scheduler_enabled, "Scheduler enabled"),
        (r.produces_live_signal, "Produces live signal"),
        (r.produces_order_decision, "Produces order decision"),
        (r.produces_portfolio_weights, "Produces portfolio weights"),
        (r.investment_advice, "Investment advice detected"),
    ]
    return [msg for condition, msg in checks if condition]

def validate_optimizer_sandbox_result(r: OptimizerSandboxResult) -> List[str]:
    errs = []
    if r.actual_target_weight is not None: errs.append(f"{r.symbol}: actual target weight must be None")
    if r.actual_portfolio_weight is not None: errs.append("Actual portfolio weight must be None")
    if r.actual_allocation is not None: errs.append("Actual allocation must be None")
    if r.actual_position_size is not None: errs.append("Actual position size must be None")
    if r.order_size is not None: errs.append("Order size must be None")
    if r.capital_allocation is not None: errs.append("Capital allocation must be None")
    if r.live_signal: errs.append("Live signal must be false")
    if r.order_decision: errs.append("Order decision must be false")
    return errs

def validate_phase157_readiness_gate(r: Phase157ReadinessGate) -> List[str]:
    errs = []
    if r.ready_for_phase157 and not r.safety_boundary.boundary_passed:
        errs.append("ready_for_phase157 true but safety_boundary failed")
    return errs
