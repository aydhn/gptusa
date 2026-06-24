from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.serialization import to_dict_clean
import uuid
import datetime

from usa_signal_bot.core.enums import (
    PortfolioFoundationStatus,
    PortfolioFoundationDecision,
    PortfolioInputKind,
    PortfolioCandidateUniverseKind,
    PortfolioEligibilityRuleKind,
    PortfolioConstraintKind,
    RiskBudgetContractKind,
    PositionSizingBoundaryKind,
    PortfolioConstructionBoundaryKind,
    PortfolioFoundationSafetyRuleKind,
    Phase154ReadinessStatus,
    Phase154ReadinessRuleKind,
    PortfolioFoundationRiskFlag,
    PortfolioFoundationReportType,
)


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@dataclass
class BacktestClosureIngestionResult:
    ingestion_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    source_path: str | None = None
    source_review_id: str | None = None
    source_context_id: str | None = None
    available: bool = False
    final_audit_report_built: bool = False
    band_closure_certificate_built: bool = False
    phase153_handoff_contract_built: bool = False
    phase153_handoff_package_built: bool = False
    handoff_safety_boundary_validated: bool = False
    phase153_readiness_gate_built: bool = False
    phase153_readiness_gate_passed: bool = False
    ready_for_phase153: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    portfolio_construction_executed: bool = False
    position_sizing_executed: bool = False
    portfolio_optimization_enabled: bool = False
    portfolio_allocation_output_enabled: bool = False
    target_weights_produced: bool = False
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
    valid_for_phase153: bool = False
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioInputReference:
    input_ref_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    input_kind: PortfolioInputKind = PortfolioInputKind.UNKNOWN
    source_artifact_name: str = ""
    source_path: str | None = None
    source_hash: str | None = None
    available: bool = False
    read_only: bool = True
    row_count: int | None = None
    columns: list[str] = field(default_factory=list)
    forbidden_columns_detected: list[str] = field(default_factory=list)
    research_data_only: bool = True
    portfolio_research_contract_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioCandidate:
    candidate_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    symbol: str = ""
    candidate_universe_kind: PortfolioCandidateUniverseKind = (
        PortfolioCandidateUniverseKind.UNKNOWN
    )
    source_phase: str | None = None
    has_metric_inventory: bool = False
    has_risk_notes: bool = False
    has_robustness_evidence: bool = False
    eligible_metadata_only: bool = False
    live_signal: bool = False
    order_decision: bool = False
    target_weight: float | None = None
    allocation: float | None = None
    position_size: float | None = None
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CandidateUniverseContract:
    contract_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    universe_name: str = ""
    universe_kind: PortfolioCandidateUniverseKind = (
        PortfolioCandidateUniverseKind.UNKNOWN
    )
    candidates: list[PortfolioCandidate] = field(default_factory=list)
    candidate_count: int = 0
    symbols: list[str] = field(default_factory=list)
    min_required_candidates: int = 0
    max_allowed_candidates: int = 0
    contract_valid: bool = False
    read_only: bool = True
    research_data_only: bool = True
    portfolio_research_contract_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    produces_live_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioEligibilityRule:
    rule_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rule_kind: PortfolioEligibilityRuleKind = PortfolioEligibilityRuleKind.UNKNOWN
    name: str = ""
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    applies_to_symbol: str | None = None
    rationale: str = ""
    metadata_only: bool = True
    not_trade_approval: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioConstraint:
    constraint_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    constraint_kind: PortfolioConstraintKind = PortfolioConstraintKind.UNKNOWN
    name: str = ""
    constraint_value: float | int | str | bool | None = None
    hard_constraint: bool = False
    soft_constraint: bool = False
    contract_only: bool = True
    actual_weight_output: bool = False
    actual_allocation_output: bool = False
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioConstraintCatalog:
    catalog_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    constraints: list[PortfolioConstraint] = field(default_factory=list)
    constraint_count: int = 0
    catalog_valid: bool = False
    contract_only: bool = True
    no_actual_weights: bool = True
    no_actual_allocation: bool = True
    no_actual_position_size: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskBudgetContractItem:
    item_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    budget_kind: RiskBudgetContractKind = RiskBudgetContractKind.UNKNOWN
    name: str = ""
    budget_value: float | int | str | None = None
    budget_unit: str = ""
    hard_limit: bool = False
    contract_only: bool = True
    actual_capital_allocation: bool = False
    actual_position_size: bool = False
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskBudgetContract:
    contract_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    items: list[RiskBudgetContractItem] = field(default_factory=list)
    item_count: int = 0
    contract_valid: bool = False
    contract_only: bool = True
    no_capital_allocation: bool = True
    no_position_sizing: bool = True
    no_target_weights: bool = True
    no_portfolio_optimization: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PositionSizingBoundaryRule:
    rule_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    boundary_kind: PositionSizingBoundaryKind = PositionSizingBoundaryKind.UNKNOWN
    name: str = ""
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PositionSizingBoundaryContract:
    boundary_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rules: list[PositionSizingBoundaryRule] = field(default_factory=list)
    boundary_valid: bool = False
    no_actual_position_size_phase153: bool = True
    no_target_weight_phase153: bool = True
    no_allocation_phase153: bool = True
    no_capital_deployment_phase153: bool = True
    no_order_size_phase153: bool = True
    sizing_prototype_allowed_phase154: bool = False
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioConstructionBoundary:
    boundary_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    boundary_kinds: list[PortfolioConstructionBoundaryKind] = field(
        default_factory=list
    )
    contract_only_phase153: bool = True
    no_optimization_phase153: bool = True
    no_rebalancing_phase153: bool = True
    no_execution_phase153: bool = True
    no_deployment_phase153: bool = True
    research_only_phase153: bool = True
    boundary_valid: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CandidateUniverseDiagnostics:
    diagnostics_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    candidate_count: int = 0
    symbols: list[str] = field(default_factory=list)
    missing_metric_inventory_count: int = 0
    missing_risk_note_count: int = 0
    missing_robustness_evidence_count: int = 0
    forbidden_output_field_count: int = 0
    diagnostics_valid: bool = False
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConstraintValidationReport:
    report_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    catalog: PortfolioConstraintCatalog = field(
        default_factory=PortfolioConstraintCatalog
    )
    rules: list[PortfolioEligibilityRule] = field(default_factory=list)
    report_valid: bool = False
    hard_constraint_count: int = 0
    soft_constraint_count: int = 0
    violated_constraint_count: int = 0
    actual_weight_output_detected: bool = False
    actual_allocation_output_detected: bool = False
    actual_position_size_detected: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskBudgetValidationReport:
    report_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    contract: RiskBudgetContract = field(default_factory=RiskBudgetContract)
    report_valid: bool = False
    budget_item_count: int = 0
    actual_capital_allocation_detected: bool = False
    actual_position_size_detected: bool = False
    target_weight_detected: bool = False
    portfolio_optimization_detected: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SizingBoundaryValidationReport:
    report_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    boundary: PositionSizingBoundaryContract = field(
        default_factory=PositionSizingBoundaryContract
    )
    construction_boundary: PortfolioConstructionBoundary = field(
        default_factory=PortfolioConstructionBoundary
    )
    report_valid: bool = False
    no_actual_position_size: bool = True
    no_target_weight: bool = True
    no_allocation: bool = True
    no_capital_deployment: bool = True
    no_order_size: bool = True
    ready_for_phase154_sizing_prototypes: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioFoundationSafetyBoundaryRule:
    rule_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rule_kind: PortfolioFoundationSafetyRuleKind = (
        PortfolioFoundationSafetyRuleKind.UNKNOWN
    )
    name: str = ""
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioFoundationSafetyBoundaryResult:
    boundary_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rules: list[PortfolioFoundationSafetyBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    read_only_handoff_ingestion: bool = True
    contract_only_portfolio_foundation: bool = True
    no_actual_portfolio_construction: bool = True
    no_position_sizing: bool = True
    no_target_weights: bool = True
    no_allocation_output: bool = True
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
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase154ReadinessRule:
    rule_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rule_kind: Phase154ReadinessRuleKind = Phase154ReadinessRuleKind.UNKNOWN
    name: str = ""
    status: Phase154ReadinessStatus = Phase154ReadinessStatus.NOT_CHECKED
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase154ReadinessGate:
    gate_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    status: Phase154ReadinessStatus = Phase154ReadinessStatus.NOT_CHECKED
    rules: list[Phase154ReadinessRule] = field(default_factory=list)
    candidate_universe_contract: CandidateUniverseContract = field(
        default_factory=CandidateUniverseContract
    )
    constraint_catalog: PortfolioConstraintCatalog = field(
        default_factory=PortfolioConstraintCatalog
    )
    risk_budget_contract: RiskBudgetContract = field(default_factory=RiskBudgetContract)
    sizing_boundary: PositionSizingBoundaryContract = field(
        default_factory=PositionSizingBoundaryContract
    )
    safety_boundary: PortfolioFoundationSafetyBoundaryResult = field(
        default_factory=PortfolioFoundationSafetyBoundaryResult
    )
    ready_for_phase154: bool = False
    research_data_only: bool = True
    portfolio_research_contract_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    actual_position_size_produced: bool = False
    target_weights_produced: bool = False
    allocation_output_produced: bool = False
    capital_deployment_allowed: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioFoundationContext:
    context_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    status: PortfolioFoundationStatus = PortfolioFoundationStatus.DRAFT
    decision: PortfolioFoundationDecision = PortfolioFoundationDecision.UNKNOWN
    source_backtest_closure_review_id: str | None = None
    ingestion: BacktestClosureIngestionResult = field(
        default_factory=BacktestClosureIngestionResult
    )
    input_references: list[PortfolioInputReference] = field(default_factory=list)
    candidate_universe_contract: CandidateUniverseContract = field(
        default_factory=CandidateUniverseContract
    )
    eligibility_rules: list[PortfolioEligibilityRule] = field(default_factory=list)
    constraint_catalog: PortfolioConstraintCatalog = field(
        default_factory=PortfolioConstraintCatalog
    )
    risk_budget_contract: RiskBudgetContract = field(default_factory=RiskBudgetContract)
    sizing_boundary: PositionSizingBoundaryContract = field(
        default_factory=PositionSizingBoundaryContract
    )
    construction_boundary: PortfolioConstructionBoundary = field(
        default_factory=PortfolioConstructionBoundary
    )
    candidate_diagnostics: CandidateUniverseDiagnostics = field(
        default_factory=CandidateUniverseDiagnostics
    )
    constraint_validation_report: ConstraintValidationReport = field(
        default_factory=ConstraintValidationReport
    )
    risk_budget_validation_report: RiskBudgetValidationReport = field(
        default_factory=RiskBudgetValidationReport
    )
    sizing_boundary_validation_report: SizingBoundaryValidationReport = field(
        default_factory=SizingBoundaryValidationReport
    )
    safety_boundary: PortfolioFoundationSafetyBoundaryResult = field(
        default_factory=PortfolioFoundationSafetyBoundaryResult
    )
    phase154_readiness_gate: Phase154ReadinessGate = field(
        default_factory=Phase154ReadinessGate
    )
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
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[PortfolioFoundationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioFoundationFullReview:
    review_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    report_type: PortfolioFoundationReportType = (
        PortfolioFoundationReportType.FULL_PHASE153_REVIEW
    )
    ingestion: BacktestClosureIngestionResult = field(
        default_factory=BacktestClosureIngestionResult
    )
    context: PortfolioFoundationContext = field(
        default_factory=PortfolioFoundationContext
    )
    candidate_universe_contract: CandidateUniverseContract = field(
        default_factory=CandidateUniverseContract
    )
    constraint_catalog: PortfolioConstraintCatalog = field(
        default_factory=PortfolioConstraintCatalog
    )
    risk_budget_contract: RiskBudgetContract = field(default_factory=RiskBudgetContract)
    sizing_boundary: PositionSizingBoundaryContract = field(
        default_factory=PositionSizingBoundaryContract
    )
    safety_boundary: PortfolioFoundationSafetyBoundaryResult = field(
        default_factory=PortfolioFoundationSafetyBoundaryResult
    )
    phase154_readiness_gate: Phase154ReadinessGate = field(
        default_factory=Phase154ReadinessGate
    )
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_backtest_closure_ingestion_id() -> str:
    return _uid()


def create_portfolio_input_reference_id() -> str:
    return _uid()


def create_portfolio_candidate_id() -> str:
    return _uid()


def create_candidate_universe_contract_id() -> str:
    return _uid()


def create_portfolio_eligibility_rule_id() -> str:
    return _uid()


def create_portfolio_constraint_id() -> str:
    return _uid()


def create_portfolio_constraint_catalog_id() -> str:
    return _uid()


def create_risk_budget_contract_item_id() -> str:
    return _uid()


def create_risk_budget_contract_id() -> str:
    return _uid()


def create_position_sizing_boundary_rule_id() -> str:
    return _uid()


def create_position_sizing_boundary_contract_id() -> str:
    return _uid()


def create_portfolio_construction_boundary_id() -> str:
    return _uid()


def create_candidate_universe_diagnostics_id() -> str:
    return _uid()


def create_constraint_validation_report_id() -> str:
    return _uid()


def create_risk_budget_validation_report_id() -> str:
    return _uid()


def create_sizing_boundary_validation_report_id() -> str:
    return _uid()


def create_portfolio_foundation_safety_boundary_rule_id() -> str:
    return _uid()


def create_portfolio_foundation_safety_boundary_result_id() -> str:
    return _uid()


def create_phase154_readiness_rule_id() -> str:
    return _uid()


def create_phase154_readiness_gate_id() -> str:
    return _uid()


def create_portfolio_foundation_context_id() -> str:
    return _uid()


def create_portfolio_foundation_full_review_id() -> str:
    return _uid()


def backtest_closure_ingestion_result_to_dict(
    item: BacktestClosureIngestionResult,
) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_input_reference_to_dict(item: PortfolioInputReference) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_candidate_to_dict(item: PortfolioCandidate) -> dict[str, Any]:
    return to_dict_clean(item)


def candidate_universe_contract_to_dict(
    item: CandidateUniverseContract,
) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_eligibility_rule_to_dict(
    item: PortfolioEligibilityRule,
) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_constraint_to_dict(item: PortfolioConstraint) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_constraint_catalog_to_dict(
    item: PortfolioConstraintCatalog,
) -> dict[str, Any]:
    return to_dict_clean(item)


def risk_budget_contract_item_to_dict(item: RiskBudgetContractItem) -> dict[str, Any]:
    return to_dict_clean(item)


def risk_budget_contract_to_dict(item: RiskBudgetContract) -> dict[str, Any]:
    return to_dict_clean(item)


def position_sizing_boundary_rule_to_dict(
    item: PositionSizingBoundaryRule,
) -> dict[str, Any]:
    return to_dict_clean(item)


def position_sizing_boundary_contract_to_dict(
    item: PositionSizingBoundaryContract,
) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_construction_boundary_to_dict(
    item: PortfolioConstructionBoundary,
) -> dict[str, Any]:
    return to_dict_clean(item)


def candidate_universe_diagnostics_to_dict(
    item: CandidateUniverseDiagnostics,
) -> dict[str, Any]:
    return to_dict_clean(item)


def constraint_validation_report_to_dict(
    item: ConstraintValidationReport,
) -> dict[str, Any]:
    return to_dict_clean(item)


def risk_budget_validation_report_to_dict(
    item: RiskBudgetValidationReport,
) -> dict[str, Any]:
    return to_dict_clean(item)


def sizing_boundary_validation_report_to_dict(
    item: SizingBoundaryValidationReport,
) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_foundation_safety_boundary_rule_to_dict(
    item: PortfolioFoundationSafetyBoundaryRule,
) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_foundation_safety_boundary_result_to_dict(
    item: PortfolioFoundationSafetyBoundaryResult,
) -> dict[str, Any]:
    return to_dict_clean(item)


def phase154_readiness_rule_to_dict(item: Phase154ReadinessRule) -> dict[str, Any]:
    return to_dict_clean(item)


def phase154_readiness_gate_to_dict(item: Phase154ReadinessGate) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_foundation_context_to_dict(
    item: PortfolioFoundationContext,
) -> dict[str, Any]:
    return to_dict_clean(item)


def portfolio_foundation_full_review_to_dict(
    item: PortfolioFoundationFullReview,
) -> dict[str, Any]:
    return to_dict_clean(item)


def validate_backtest_closure_ingestion_result(
    item: BacktestClosureIngestionResult,
) -> list[str]:
    errors = []
    if not item.ready_for_phase153:
        errors.append("Not ready for phase 153")
    if not item.research_data_only:
        errors.append("Must be research data only")
    if item.live_trading_enabled:
        errors.append("Live trading must be false")
    if item.portfolio_construction_executed:
        errors.append("Actual portfolio construction must be false")
    return errors


def validate_portfolio_input_reference(item: PortfolioInputReference) -> list[str]:
    return []


def validate_portfolio_candidate(item: PortfolioCandidate) -> list[str]:
    return []


def validate_candidate_universe_contract(item: CandidateUniverseContract) -> list[str]:
    return []


def validate_portfolio_eligibility_rule(item: PortfolioEligibilityRule) -> list[str]:
    return []


def validate_portfolio_constraint(item: PortfolioConstraint) -> list[str]:
    return []


def validate_portfolio_constraint_catalog(
    item: PortfolioConstraintCatalog,
) -> list[str]:
    return []


def validate_risk_budget_contract_item(item: RiskBudgetContractItem) -> list[str]:
    return []


def validate_risk_budget_contract(item: RiskBudgetContract) -> list[str]:
    return []


def validate_position_sizing_boundary_rule(
    item: PositionSizingBoundaryRule,
) -> list[str]:
    return []


def validate_position_sizing_boundary_contract(
    item: PositionSizingBoundaryContract,
) -> list[str]:
    return []


def validate_portfolio_construction_boundary(
    item: PortfolioConstructionBoundary,
) -> list[str]:
    return []


def validate_candidate_universe_diagnostics(
    item: CandidateUniverseDiagnostics,
) -> list[str]:
    return []


def validate_constraint_validation_report(
    item: ConstraintValidationReport,
) -> list[str]:
    return []


def validate_risk_budget_validation_report(
    item: RiskBudgetValidationReport,
) -> list[str]:
    return []


def validate_sizing_boundary_validation_report(
    item: SizingBoundaryValidationReport,
) -> list[str]:
    return []


def validate_portfolio_foundation_safety_boundary_rule(
    item: PortfolioFoundationSafetyBoundaryRule,
) -> list[str]:
    return []


def validate_portfolio_foundation_safety_boundary_result(
    item: PortfolioFoundationSafetyBoundaryResult,
) -> list[str]:
    return []


def validate_phase154_readiness_rule(item: Phase154ReadinessRule) -> list[str]:
    return []


def validate_phase154_readiness_gate(item: Phase154ReadinessGate) -> list[str]:
    return []


def validate_portfolio_foundation_context(
    item: PortfolioFoundationContext,
) -> list[str]:
    return []


def validate_portfolio_foundation_full_review(
    item: PortfolioFoundationFullReview,
) -> list[str]:
    return []
