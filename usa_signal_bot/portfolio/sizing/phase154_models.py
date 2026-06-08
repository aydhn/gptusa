import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    SizingPrototypeStatus,
    SizingPrototypeDecision,
    SizingInputKind,
    SizingMethodKind,
    SizingPolicyKind,
    SizingCapFloorRuleKind,
    SizingDiagnosticKind,
    SizingSensitivityKind,
    SizingSafetyRuleKind,
    Phase155ReadinessStatus,
    Phase155ReadinessRuleKind,
    SizingPrototypeQuality,
    SizingPrototypeRiskFlag,
    SizingPrototypeReportType
)

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_portfolio_foundation_ingestion_id() -> str:
    return f"pfi_{uuid.uuid4().hex[:12]}"

def create_sizing_input_reference_id() -> str:
    return f"sir_{uuid.uuid4().hex[:12]}"

def create_sizing_candidate_id() -> str:
    return f"sc_{uuid.uuid4().hex[:12]}"

def create_sizing_policy_id() -> str:
    return f"spo_{uuid.uuid4().hex[:12]}"

def create_sizing_method_contract_id() -> str:
    return f"smc_{uuid.uuid4().hex[:12]}"

def create_sizing_prototype_result_id() -> str:
    return f"spr_{uuid.uuid4().hex[:12]}"

def create_sizing_cap_floor_rule_id() -> str:
    return f"cfr_{uuid.uuid4().hex[:12]}"

def create_sizing_comparison_matrix_id() -> str:
    return f"scm_{uuid.uuid4().hex[:12]}"

def create_sizing_diagnostic_id() -> str:
    return f"sd_{uuid.uuid4().hex[:12]}"

def create_sizing_sensitivity_id() -> str:
    return f"ss_{uuid.uuid4().hex[:12]}"

def create_sizing_sensitivity_report_id() -> str:
    return f"ssr_{uuid.uuid4().hex[:12]}"

def create_risk_budget_adherence_report_id() -> str:
    return f"rba_{uuid.uuid4().hex[:12]}"

def create_sizing_safety_boundary_rule_id() -> str:
    return f"sbr_{uuid.uuid4().hex[:12]}"

def create_sizing_safety_boundary_result_id() -> str:
    return f"sbs_{uuid.uuid4().hex[:12]}"

def create_phase155_readiness_rule_id() -> str:
    return f"p155r_{uuid.uuid4().hex[:12]}"

def create_phase155_readiness_gate_id() -> str:
    return f"p155g_{uuid.uuid4().hex[:12]}"

def create_sizing_prototype_context_id() -> str:
    return f"spc_{uuid.uuid4().hex[:12]}"

def create_sizing_prototype_full_review_id() -> str:
    return f"p154r_{uuid.uuid4().hex[:12]}"

@dataclass
class PortfolioFoundationIngestionResult:
    ingestion_id: str = field(default_factory=create_portfolio_foundation_ingestion_id)
    created_at_utc: str = field(default_factory=_now_utc)
    source_path: str | None = None
    source_review_id: str | None = None
    source_context_id: str | None = None
    available: bool = False
    backtest_closure_ingested: bool = False
    handoff_package_loaded: bool = False
    inputs_resolved: bool = False
    candidate_universe_contract_built: bool = False
    eligibility_rules_built: bool = False
    constraint_catalog_built: bool = False
    risk_budget_contract_built: bool = False
    position_sizing_boundary_built: bool = False
    portfolio_construction_boundary_built: bool = False
    candidate_universe_diagnostics_built: bool = False
    constraint_validation_report_built: bool = False
    risk_budget_validation_report_built: bool = False
    sizing_boundary_validation_report_built: bool = False
    safety_boundary_validated: bool = False
    phase154_readiness_gate_built: bool = False
    phase154_readiness_gate_passed: bool = False
    ready_for_phase154: bool = False
    research_data_only: bool = True
    portfolio_research_contract_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    actual_portfolio_construction_executed: bool = False
    actual_position_sizing_executed: bool = False
    portfolio_optimization_enabled: bool = False
    rebalancing_enabled: bool = False
    target_weights_produced: bool = False
    allocation_output_produced: bool = False
    capital_deployment_allowed: bool = False
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
    valid_for_phase154: bool = False
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingInputReference:
    input_ref_id: str = field(default_factory=create_sizing_input_reference_id)
    created_at_utc: str = field(default_factory=_now_utc)
    input_kind: SizingInputKind = SizingInputKind.UNKNOWN
    source_artifact_name: str = ""
    source_path: str | None = None
    source_hash: str | None = None
    available: bool = False
    read_only: bool = True
    row_count: int | None = None
    columns: list[str] = field(default_factory=list)
    forbidden_columns_detected: list[str] = field(default_factory=list)
    research_data_only: bool = True
    sizing_research_prototype_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingCandidate:
    candidate_id: str = field(default_factory=create_sizing_candidate_id)
    created_at_utc: str = field(default_factory=_now_utc)
    symbol: str = ""
    candidate_valid: bool = False
    eligible_for_research_prototype: bool = False
    volatility_proxy: float | None = None
    drawdown_proxy: float | None = None
    cost_proxy: float | None = None
    liquidity_proxy: float | None = None
    robustness_proxy: float | None = None
    risk_budget_proxy: float | None = None
    live_signal: bool = False
    order_decision: bool = False
    actual_position_size: float | None = None
    target_weight: float | None = None
    allocation: float | None = None
    order_size: float | None = None
    capital_allocation: float | None = None
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingPolicy:
    policy_id: str = field(default_factory=create_sizing_policy_id)
    created_at_utc: str = field(default_factory=_now_utc)
    policy_kind: SizingPolicyKind = SizingPolicyKind.UNKNOWN
    policy_name: str = ""
    base_prototype_fraction: float = 0.01
    max_prototype_fraction: float = 0.05
    min_prototype_fraction: float = 0.0
    max_risk_budget_usage_fraction: float = 0.25
    volatility_penalty_enabled: bool = False
    drawdown_penalty_enabled: bool = False
    cost_penalty_enabled: bool = False
    liquidity_penalty_enabled: bool = False
    robustness_penalty_enabled: bool = False
    deterministic: bool = True
    policy_valid: bool = False
    research_data_only: bool = True
    sizing_research_prototype_only: bool = True
    actual_position_sizing_allowed: bool = False
    target_weights_allowed: bool = False
    allocation_output_allowed: bool = False
    capital_deployment_allowed: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingMethodContract:
    contract_id: str = field(default_factory=create_sizing_method_contract_id)
    created_at_utc: str = field(default_factory=_now_utc)
    method_kind: SizingMethodKind = SizingMethodKind.UNKNOWN
    method_name: str = ""
    enabled: bool = False
    deterministic: bool = True
    contract_only: bool = True
    produces_research_prototype_fraction: bool = True
    produces_actual_position_size: bool = False
    produces_target_weight: bool = False
    produces_allocation: bool = False
    produces_order_size: bool = False
    produces_capital_allocation: bool = False
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingPrototypeResult:
    result_id: str = field(default_factory=create_sizing_prototype_result_id)
    created_at_utc: str = field(default_factory=_now_utc)
    symbol: str = ""
    method_kind: SizingMethodKind = SizingMethodKind.UNKNOWN
    method_name: str = ""
    raw_prototype_fraction: float | None = None
    capped_prototype_fraction: float | None = None
    normalized_research_score: float | None = None
    volatility_penalty: float | None = None
    drawdown_penalty: float | None = None
    cost_penalty: float | None = None
    liquidity_penalty: float | None = None
    robustness_penalty: float | None = None
    risk_budget_usage_fraction: float | None = None
    cap_floor_applied: bool = False
    prototype_valid: bool = False
    research_prototype_only: bool = True
    actual_position_size: float | None = None
    target_weight: float | None = None
    allocation: float | None = None
    order_size: float | None = None
    capital_allocation: float | None = None
    live_signal: bool = False
    order_decision: bool = False
    not_investment_advice: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingCapFloorRule:
    rule_id: str = field(default_factory=create_sizing_cap_floor_rule_id)
    created_at_utc: str = field(default_factory=_now_utc)
    rule_kind: SizingCapFloorRuleKind = SizingCapFloorRuleKind.UNKNOWN
    name: str = ""
    required: bool = False
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    applies_to_symbol: str | None = None
    applies_to_method: SizingMethodKind | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingComparisonMatrix:
    matrix_id: str = field(default_factory=create_sizing_comparison_matrix_id)
    created_at_utc: str = field(default_factory=_now_utc)
    results: list[SizingPrototypeResult] = field(default_factory=list)
    symbol_count: int = 0
    method_count: int = 0
    matrix_hash: str | None = None
    matrix_valid: bool = False
    research_prototype_only: bool = True
    no_actual_position_size: bool = True
    no_target_weights: bool = True
    no_allocation_output: bool = True
    no_order_size: bool = True
    no_capital_allocation: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingDiagnosticRecord:
    diagnostic_id: str = field(default_factory=create_sizing_diagnostic_id)
    created_at_utc: str = field(default_factory=_now_utc)
    diagnostic_kind: SizingDiagnosticKind = SizingDiagnosticKind.UNKNOWN
    value: float | int | str | dict[str, Any] | None = None
    diagnostic_notes: list[str] = field(default_factory=list)
    diagnostic_valid: bool = False
    research_prototype_only: bool = True
    not_investment_advice: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingSensitivityRecord:
    sensitivity_id: str = field(default_factory=create_sizing_sensitivity_id)
    created_at_utc: str = field(default_factory=_now_utc)
    sensitivity_kind: SizingSensitivityKind = SizingSensitivityKind.UNKNOWN
    value: float | int | str | dict[str, Any] | None = None
    sensitivity_notes: list[str] = field(default_factory=list)
    sensitivity_valid: bool = False
    research_prototype_only: bool = True
    not_investment_advice: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingSensitivityReport:
    report_id: str = field(default_factory=create_sizing_sensitivity_report_id)
    created_at_utc: str = field(default_factory=_now_utc)
    records: list[SizingSensitivityRecord] = field(default_factory=list)
    report_valid: bool = False
    report_hash: str | None = None
    research_prototype_only: bool = True
    actual_position_size_detected: bool = False
    target_weight_detected: bool = False
    allocation_detected: bool = False
    order_size_detected: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RiskBudgetAdherenceReport:
    report_id: str = field(default_factory=create_risk_budget_adherence_report_id)
    created_at_utc: str = field(default_factory=_now_utc)
    result_count: int = 0
    max_risk_budget_usage_fraction: float | None = None
    average_risk_budget_usage_fraction: float | None = None
    breach_count: int = 0
    report_valid: bool = False
    report_hash: str | None = None
    research_prototype_only: bool = True
    actual_capital_allocation_detected: bool = False
    actual_position_size_detected: bool = False
    target_weight_detected: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingSafetyBoundaryRule:
    rule_id: str = field(default_factory=create_sizing_safety_boundary_rule_id)
    created_at_utc: str = field(default_factory=_now_utc)
    rule_kind: SizingSafetyRuleKind = SizingSafetyRuleKind.UNKNOWN
    name: str = ""
    required: bool = False
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingSafetyBoundaryResult:
    boundary_id: str = field(default_factory=create_sizing_safety_boundary_result_id)
    created_at_utc: str = field(default_factory=_now_utc)
    rules: list[SizingSafetyBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    research_prototype_only: bool = True
    read_only_foundation_artifacts: bool = True
    no_actual_position_size: bool = True
    no_target_weights: bool = True
    no_allocation_output: bool = True
    no_order_size: bool = True
    no_capital_deployment: bool = True
    no_portfolio_optimization: bool = True
    no_rebalancing: bool = True
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
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase155ReadinessRule:
    rule_id: str = field(default_factory=create_phase155_readiness_rule_id)
    created_at_utc: str = field(default_factory=_now_utc)
    rule_kind: Phase155ReadinessRuleKind = Phase155ReadinessRuleKind.UNKNOWN
    name: str = ""
    status: Phase155ReadinessStatus = Phase155ReadinessStatus.NOT_CHECKED
    required: bool = False
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase155ReadinessGate:
    gate_id: str = field(default_factory=create_phase155_readiness_gate_id)
    created_at_utc: str = field(default_factory=_now_utc)
    status: Phase155ReadinessStatus = Phase155ReadinessStatus.NOT_CHECKED
    rules: list[Phase155ReadinessRule] = field(default_factory=list)
    sizing_policy: SizingPolicy = field(default_factory=SizingPolicy)
    method_contracts: list[SizingMethodContract] = field(default_factory=list)
    comparison_matrix: SizingComparisonMatrix = field(default_factory=SizingComparisonMatrix)
    sensitivity_report: SizingSensitivityReport = field(default_factory=SizingSensitivityReport)
    risk_budget_adherence_report: RiskBudgetAdherenceReport = field(default_factory=RiskBudgetAdherenceReport)
    safety_boundary: SizingSafetyBoundaryResult = field(default_factory=SizingSafetyBoundaryResult)
    ready_for_phase155: bool = False
    research_data_only: bool = True
    sizing_research_prototype_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    actual_position_size_produced: bool = False
    target_weights_produced: bool = False
    allocation_output_produced: bool = False
    order_size_produced: bool = False
    capital_deployment_allowed: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingPrototypeContext:
    context_id: str = field(default_factory=create_sizing_prototype_context_id)
    created_at_utc: str = field(default_factory=_now_utc)
    status: SizingPrototypeStatus = SizingPrototypeStatus.DRAFT
    decision: SizingPrototypeDecision = SizingPrototypeDecision.UNKNOWN
    source_portfolio_foundation_review_id: str | None = None
    ingestion: PortfolioFoundationIngestionResult = field(default_factory=PortfolioFoundationIngestionResult)
    input_references: list[SizingInputReference] = field(default_factory=list)
    candidates: list[SizingCandidate] = field(default_factory=list)
    sizing_policy: SizingPolicy = field(default_factory=SizingPolicy)
    method_contracts: list[SizingMethodContract] = field(default_factory=list)
    prototype_results: list[SizingPrototypeResult] = field(default_factory=list)
    cap_floor_rules: list[SizingCapFloorRule] = field(default_factory=list)
    comparison_matrix: SizingComparisonMatrix = field(default_factory=SizingComparisonMatrix)
    diagnostics: list[SizingDiagnosticRecord] = field(default_factory=list)
    sensitivity_report: SizingSensitivityReport = field(default_factory=SizingSensitivityReport)
    risk_budget_adherence_report: RiskBudgetAdherenceReport = field(default_factory=RiskBudgetAdherenceReport)
    safety_boundary: SizingSafetyBoundaryResult = field(default_factory=SizingSafetyBoundaryResult)
    phase155_readiness_gate: Phase155ReadinessGate = field(default_factory=Phase155ReadinessGate)
    portfolio_foundation_ingested: bool = False
    artifacts_loaded: bool = False
    inputs_resolved: bool = False
    sizing_policy_built: bool = False
    method_contracts_built: bool = False
    fixed_fractional_sizing_built: bool = False
    volatility_adjusted_sizing_built: bool = False
    drawdown_adjusted_sizing_built: bool = False
    cost_aware_sizing_built: bool = False
    liquidity_aware_sizing_built: bool = False
    robustness_adjusted_sizing_built: bool = False
    cap_floor_rules_applied: bool = False
    comparison_matrix_built: bool = False
    sizing_diagnostics_built: bool = False
    sensitivity_report_built: bool = False
    risk_budget_adherence_built: bool = False
    safety_boundary_validated: bool = False
    phase155_readiness_gate_built: bool = False
    phase155_readiness_gate_passed: bool = False
    ready_for_phase155: bool = False
    research_data_only: bool = True
    sizing_research_prototype_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    actual_portfolio_construction_executed: bool = False
    actual_position_sizing_executed: bool = False
    portfolio_optimization_enabled: bool = False
    rebalancing_enabled: bool = False
    target_weights_produced: bool = False
    allocation_output_produced: bool = False
    order_size_produced: bool = False
    capital_deployment_allowed: bool = False
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
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[SizingPrototypeRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingPrototypeFullReview:
    review_id: str = field(default_factory=create_sizing_prototype_full_review_id)
    created_at_utc: str = field(default_factory=_now_utc)
    report_type: SizingPrototypeReportType = SizingPrototypeReportType.UNKNOWN
    ingestion: PortfolioFoundationIngestionResult = field(default_factory=PortfolioFoundationIngestionResult)
    context: SizingPrototypeContext = field(default_factory=SizingPrototypeContext)
    sizing_policy: SizingPolicy = field(default_factory=SizingPolicy)
    comparison_matrix: SizingComparisonMatrix = field(default_factory=SizingComparisonMatrix)
    diagnostics: list[SizingDiagnosticRecord] = field(default_factory=list)
    sensitivity_report: SizingSensitivityReport = field(default_factory=SizingSensitivityReport)
    risk_budget_adherence_report: RiskBudgetAdherenceReport = field(default_factory=RiskBudgetAdherenceReport)
    safety_boundary: SizingSafetyBoundaryResult = field(default_factory=SizingSafetyBoundaryResult)
    phase155_readiness_gate: Phase155ReadinessGate = field(default_factory=Phase155ReadinessGate)
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
