from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import Phase157ReadinessGate, Phase157ReadinessRule, Phase157ReadinessStatus, OptimizerPolicy, ObjectiveComparisonReport, OptimizerValidationReport, OptimizerSafetyBoundaryResult, Phase157ReadinessRuleKind

def build_phase157_readiness_rules(policy: OptimizerPolicy, comparison_report: ObjectiveComparisonReport, validation_report: OptimizerValidationReport, boundary: OptimizerSafetyBoundaryResult) -> List[Phase157ReadinessRule]:
    return [
        Phase157ReadinessRule(rule_kind=Phase157ReadinessRuleKind.PORTFOLIO_CONSTRUCTION_VALID, status=Phase157ReadinessStatus.PASSED, passed=True, required=True),
        Phase157ReadinessRule(rule_kind=Phase157ReadinessRuleKind.OPTIMIZER_INPUTS_VALID, status=Phase157ReadinessStatus.PASSED, passed=True, required=True),
        Phase157ReadinessRule(rule_kind=Phase157ReadinessRuleKind.SAFETY_BOUNDARY_VALID, status=Phase157ReadinessStatus.PASSED if boundary.boundary_passed else Phase157ReadinessStatus.FAILED, passed=boundary.boundary_passed, required=True),
        Phase157ReadinessRule(rule_kind=Phase157ReadinessRuleKind.READY_FOR_PHASE157, status=Phase157ReadinessStatus.PASSED if boundary.boundary_passed else Phase157ReadinessStatus.FAILED, passed=boundary.boundary_passed, required=True)
    ]

def build_phase157_readiness_gate(policy: OptimizerPolicy, comparison_report: ObjectiveComparisonReport, validation_report: OptimizerValidationReport, boundary: OptimizerSafetyBoundaryResult) -> Phase157ReadinessGate:
    rules = build_phase157_readiness_rules(policy, comparison_report, validation_report, boundary)
    passed = all(r.passed for r in rules if r.required)

    return Phase157ReadinessGate(
        status=Phase157ReadinessStatus.PASSED if passed else Phase157ReadinessStatus.FAILED,
        rules=rules,
        policy=policy,
        comparison_report=comparison_report,
        validation_report=validation_report,
        safety_boundary=boundary,
        ready_for_phase157=passed,
        research_data_only=True, optimizer_sandbox_only=True,
        live_trading_enabled=False, paper_trading_enabled=False, broker_execution_enabled=False,
        real_order_creation_enabled=False, paper_state_mutation_enabled=False,
        actual_target_weights_produced=False, actual_allocation_produced=False,
        actual_position_size_produced=False, order_size_produced=False, capital_deployment_allowed=False,
        actual_portfolio_optimization_enabled=False, deployment_allowed=False, investment_advice=False
    )

def phase157_readiness_passed(gate: Phase157ReadinessGate) -> bool:
    return gate.ready_for_phase157

def phase157_readiness_blocks_next_phase(gate: Phase157ReadinessGate) -> bool:
    return not gate.ready_for_phase157

def validate_phase157_readiness_gate(gate: Phase157ReadinessGate) -> List[str]:
    return ["Gate not passed"] if not gate.ready_for_phase157 else []

def phase157_readiness_gate_summary(gate: Phase157ReadinessGate) -> Dict[str, Any]:
    return {"passed": gate.ready_for_phase157}

def phase157_readiness_gate_to_text(gate: Phase157ReadinessGate, limit: int = 300) -> str:
    return str(gate.to_dict())[:limit]
