from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    Phase156ReadinessGate,
    Phase156ReadinessRule,
    Phase156ReadinessRuleKind,
    Phase156ReadinessStatus,
    PortfolioConstructionPolicy,
    SandboxAllocationMethodContract,
    AllocationSandboxComparisonReport,
    PortfolioConstructionValidationReport,
    AllocationSandboxSafetyBoundaryResult,
    create_phase156_readiness_rule_id,
    create_phase156_readiness_gate_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_phase156_readiness_rules(
    policy: PortfolioConstructionPolicy,
    contracts: List[SandboxAllocationMethodContract],
    comparison_report: AllocationSandboxComparisonReport,
    validation_report: PortfolioConstructionValidationReport,
    boundary: AllocationSandboxSafetyBoundaryResult
) -> List[Phase156ReadinessRule]:

    rules = []

    def _rule(kind: Phase156ReadinessRuleKind, name: str, passed: bool, rationale: str):
        rules.append(Phase156ReadinessRule(
            rule_id=create_phase156_readiness_rule_id(),
            created_at_utc=_now_str(),
            rule_kind=kind,
            name=name,
            status=Phase156ReadinessStatus.PASSED if passed else Phase156ReadinessStatus.FAILED,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=rationale,
            warnings=[],
            errors=[] if passed else [f"Failed: {name}"],
            risk_flags=[],
            metadata={}
        ))

    _rule(
        Phase156ReadinessRuleKind.CONSTRUCTION_POLICY_VALID,
        "Policy Valid",
        policy.policy_valid,
        "Construction policy must be valid."
    )

    _rule(
        Phase156ReadinessRuleKind.METHOD_CONTRACTS_VALID,
        "Method Contracts Valid",
        len(contracts) > 0 and all(c.enabled for c in contracts),
        "Must have valid and enabled method contracts."
    )

    _rule(
        Phase156ReadinessRuleKind.ALLOCATION_COMPARISON_REPORT_VALID,
        "Comparison Report Valid",
        comparison_report.report_valid,
        "Comparison report must be valid."
    )

    _rule(
        Phase156ReadinessRuleKind.CONSTRUCTION_VALIDATION_REPORT_VALID,
        "Validation Report Valid",
        validation_report.report_valid,
        "Validation report must be valid."
    )

    _rule(
        Phase156ReadinessRuleKind.SAFETY_BOUNDARY_VALID,
        "Safety Boundary Passed",
        boundary.boundary_passed,
        "Safety boundary must pass."
    )

    _rule(
        Phase156ReadinessRuleKind.NO_ACTUAL_TARGET_WEIGHT_OUTPUT,
        "No Actual Target Weight Output",
        boundary.no_actual_target_weights,
        "Must not produce actual target weights."
    )

    _rule(
        Phase156ReadinessRuleKind.NO_LIVE_TRADING,
        "No Live Trading",
        boundary.no_live_trading,
        "Must not enable live trading."
    )

    return rules

def build_phase156_readiness_gate(
    policy: PortfolioConstructionPolicy,
    contracts: List[SandboxAllocationMethodContract],
    comparison_report: AllocationSandboxComparisonReport,
    validation_report: PortfolioConstructionValidationReport,
    boundary: AllocationSandboxSafetyBoundaryResult
) -> Phase156ReadinessGate:

    rules = build_phase156_readiness_rules(policy, contracts, comparison_report, validation_report, boundary)
    passed = all(r.passed for r in rules if r.required)
    status = Phase156ReadinessStatus.PASSED if passed else Phase156ReadinessStatus.FAILED

    return Phase156ReadinessGate(
        gate_id=create_phase156_readiness_gate_id(),
        created_at_utc=_now_str(),
        status=status,
        rules=rules,
        policy=policy,
        method_contracts=contracts,
        comparison_report=comparison_report,
        validation_report=validation_report,
        safety_boundary=boundary,
        ready_for_phase156=passed,
        research_data_only=True,
        allocation_sandbox_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        actual_target_weights_produced=False,
        actual_allocation_produced=False,
        actual_position_size_produced=False,
        order_size_produced=False,
        capital_deployment_allowed=False,
        portfolio_optimization_enabled=False,
        deployment_allowed=False,
        investment_advice=False,
        warnings=[],
        errors=[] if passed else ["Phase 156 readiness gate failed."],
        risk_flags=[],
        metadata={}
    )

def phase156_readiness_passed(gate: Phase156ReadinessGate) -> bool:
    return gate.ready_for_phase156

def phase156_readiness_blocks_next_phase(gate: Phase156ReadinessGate) -> bool:
    return not gate.ready_for_phase156

def validate_phase156_readiness_gate(gate: Phase156ReadinessGate) -> List[str]:
    errors = []
    if not gate.ready_for_phase156:
        errors.append("Gate is not ready for Phase 156.")
        gate.risk_flags.append(PortfolioConstructionRiskFlag.PHASE155_NOT_READY)
    return errors

def phase156_readiness_gate_summary(gate: Phase156ReadinessGate) -> Dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "status": gate.status.value,
        "ready": gate.ready_for_phase156,
        "failed_rules": [r.name for r in gate.rules if not r.passed]
    }

def phase156_readiness_gate_to_text(gate: Phase156ReadinessGate, limit: int = 300) -> str:
    summary = phase156_readiness_gate_summary(gate)
    return (
        f"Phase 156 Readiness Gate: {summary['gate_id']}\n"
        f"Status: {summary['status']}, Ready: {summary['ready']}\n"
        f"Failed Rules: {', '.join(summary['failed_rules']) if summary['failed_rules'] else 'None'}"
    )
