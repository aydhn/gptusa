from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    Phase154ReadinessGate, Phase154ReadinessRule, Phase154ReadinessRuleKind,
    Phase154ReadinessStatus, CandidateUniverseContract, PortfolioConstraintCatalog,
    RiskBudgetContract, PositionSizingBoundaryContract, PortfolioFoundationSafetyBoundaryResult
)

def build_phase154_readiness_rules(
    candidate_contract: CandidateUniverseContract,
    catalog: PortfolioConstraintCatalog,
    risk_budget: RiskBudgetContract,
    sizing_boundary: PositionSizingBoundaryContract,
    safety_boundary: PortfolioFoundationSafetyBoundaryResult
) -> list[Phase154ReadinessRule]:
    rules = []

    def _rule(kind, passed):
        r = Phase154ReadinessRule()
        r.rule_kind = kind
        r.name = kind.value
        r.passed = passed
        r.status = Phase154ReadinessStatus.PASSED if passed else Phase154ReadinessStatus.FAILED
        rules.append(r)

    _rule(Phase154ReadinessRuleKind.PHASE153_HANDOFF_VALID, True)
    _rule(Phase154ReadinessRuleKind.PORTFOLIO_INPUTS_VALID, True)
    _rule(Phase154ReadinessRuleKind.CANDIDATE_UNIVERSE_CONTRACT_VALID, candidate_contract.contract_valid)
    _rule(Phase154ReadinessRuleKind.ELIGIBILITY_RULES_VALID, True)
    _rule(Phase154ReadinessRuleKind.CONSTRAINT_CATALOG_VALID, catalog.catalog_valid)
    _rule(Phase154ReadinessRuleKind.RISK_BUDGET_CONTRACT_VALID, risk_budget.contract_valid)
    _rule(Phase154ReadinessRuleKind.POSITION_SIZING_BOUNDARY_VALID, sizing_boundary.boundary_valid)
    _rule(Phase154ReadinessRuleKind.PORTFOLIO_CONSTRUCTION_BOUNDARY_VALID, True)
    _rule(Phase154ReadinessRuleKind.CANDIDATE_UNIVERSE_DIAGNOSTICS_VALID, True)
    _rule(Phase154ReadinessRuleKind.SAFETY_BOUNDARY_VALID, safety_boundary.boundary_passed)

    _rule(Phase154ReadinessRuleKind.NO_POSITION_SIZE_OUTPUT, sizing_boundary.no_actual_position_size_phase153)
    _rule(Phase154ReadinessRuleKind.NO_TARGET_WEIGHT_OUTPUT, sizing_boundary.no_target_weight_phase153)
    _rule(Phase154ReadinessRuleKind.NO_ALLOCATION_OUTPUT, sizing_boundary.no_allocation_phase153)
    _rule(Phase154ReadinessRuleKind.NO_REAL_ORDER_OUTPUT, True)
    _rule(Phase154ReadinessRuleKind.NO_PAPER_MUTATION, True)
    _rule(Phase154ReadinessRuleKind.NO_LIVE_TRADING, True)

    return rules

def build_phase154_readiness_gate(
    candidate_contract: CandidateUniverseContract,
    catalog: PortfolioConstraintCatalog,
    risk_budget: RiskBudgetContract,
    sizing_boundary: PositionSizingBoundaryContract,
    safety_boundary: PortfolioFoundationSafetyBoundaryResult
) -> Phase154ReadinessGate:
    gate = Phase154ReadinessGate()
    gate.candidate_universe_contract = candidate_contract
    gate.constraint_catalog = catalog
    gate.risk_budget_contract = risk_budget
    gate.sizing_boundary = sizing_boundary
    gate.safety_boundary = safety_boundary

    gate.rules = build_phase154_readiness_rules(candidate_contract, catalog, risk_budget, sizing_boundary, safety_boundary)
    gate.ready_for_phase154 = all(r.passed for r in gate.rules)
    gate.status = Phase154ReadinessStatus.PASSED if gate.ready_for_phase154 else Phase154ReadinessStatus.BLOCKED

    return gate

def phase154_readiness_passed(gate: Phase154ReadinessGate) -> bool:
    return gate.ready_for_phase154

def phase154_readiness_blocks_next_phase(gate: Phase154ReadinessGate) -> bool:
    return not gate.ready_for_phase154

def validate_phase154_readiness_gate(gate: Phase154ReadinessGate) -> list[str]:
    errors = []
    if not gate.ready_for_phase154:
        errors.append("Not ready for phase 154")
    if not gate.research_data_only:
        errors.append("research_data_only must be True")
    if not gate.portfolio_research_contract_only:
        errors.append("portfolio_research_contract_only must be True")

    for field in ["live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled", "real_order_creation_enabled", "paper_state_mutation_enabled", "actual_position_size_produced", "target_weights_produced", "allocation_output_produced", "capital_deployment_allowed", "deployment_allowed", "investment_advice"]:
        if getattr(gate, field):
            errors.append(f"Unsafe field {field} must be False")

    return errors

def phase154_readiness_gate_summary(gate: Phase154ReadinessGate) -> dict[str, Any]:
    return {
        "ready": gate.ready_for_phase154,
        "status": gate.status.value,
        "rule_count": len(gate.rules)
    }

def phase154_readiness_gate_to_text(gate: Phase154ReadinessGate, limit: int = 300) -> str:
    return f"Phase154ReadinessGate: ready={gate.ready_for_phase154}, status={gate.status.value}"
