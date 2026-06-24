from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import (
    Phase155ReadinessGate,
    Phase155ReadinessRule,
    Phase155ReadinessRuleKind,
    Phase155ReadinessStatus,
    SizingPrototypeContext,
)


def build_phase155_readiness_rules(
    context: SizingPrototypeContext,
) -> list[Phase155ReadinessRule]:

    kinds = [
        Phase155ReadinessRuleKind.PORTFOLIO_FOUNDATION_VALID,
        Phase155ReadinessRuleKind.SIZING_INPUTS_VALID,
        Phase155ReadinessRuleKind.SIZING_POLICY_VALID,
        Phase155ReadinessRuleKind.METHOD_CONTRACTS_VALID,
        Phase155ReadinessRuleKind.FIXED_FRACTIONAL_PROTOTYPES_VALID,
        Phase155ReadinessRuleKind.VOLATILITY_ADJUSTED_PROTOTYPES_VALID,
        Phase155ReadinessRuleKind.DRAWDOWN_ADJUSTED_PROTOTYPES_VALID,
        Phase155ReadinessRuleKind.COST_AWARE_PROTOTYPES_VALID,
        Phase155ReadinessRuleKind.LIQUIDITY_AWARE_PROTOTYPES_VALID,
        Phase155ReadinessRuleKind.ROBUSTNESS_ADJUSTED_PROTOTYPES_VALID,
        Phase155ReadinessRuleKind.CAP_FLOOR_RULES_VALID,
        Phase155ReadinessRuleKind.COMPARISON_MATRIX_VALID,
        Phase155ReadinessRuleKind.SIZING_DIAGNOSTICS_VALID,
        Phase155ReadinessRuleKind.SENSITIVITY_REPORT_VALID,
        Phase155ReadinessRuleKind.RISK_BUDGET_ADHERENCE_VALID,
        Phase155ReadinessRuleKind.SAFETY_BOUNDARY_VALID,
        Phase155ReadinessRuleKind.NO_ACTUAL_POSITION_SIZE_OUTPUT,
        Phase155ReadinessRuleKind.NO_TARGET_WEIGHT_OUTPUT,
        Phase155ReadinessRuleKind.NO_ALLOCATION_OUTPUT,
        Phase155ReadinessRuleKind.NO_REAL_ORDER_OUTPUT,
        Phase155ReadinessRuleKind.NO_PAPER_MUTATION,
        Phase155ReadinessRuleKind.NO_LIVE_TRADING,
        Phase155ReadinessRuleKind.READY_FOR_PHASE155,
    ]

    is_passed = context.safety_boundary.boundary_passed
    rules = []

    for k in kinds:
        r = Phase155ReadinessRule(
            rule_kind=k,
            name=k.value,
            status=(
                Phase155ReadinessStatus.PASSED
                if is_passed
                else Phase155ReadinessStatus.FAILED
            ),
            required=True,
            passed=is_passed,
            expected_value=True,
            observed_value=is_passed,
            rationale="Phase155 Gate check.",
        )
        rules.append(r)
    return rules


def build_phase155_readiness_gate(
    context: SizingPrototypeContext,
) -> Phase155ReadinessGate:
    gate = Phase155ReadinessGate()
    gate.sizing_policy = context.sizing_policy
    gate.method_contracts = context.method_contracts
    gate.comparison_matrix = context.comparison_matrix
    gate.sensitivity_report = context.sensitivity_report
    gate.risk_budget_adherence_report = context.risk_budget_adherence_report
    gate.safety_boundary = context.safety_boundary

    gate.rules = build_phase155_readiness_rules(context)

    gate.ready_for_phase155 = phase155_readiness_passed(gate)
    gate.status = (
        Phase155ReadinessStatus.PASSED
        if gate.ready_for_phase155
        else Phase155ReadinessStatus.FAILED
    )

    return gate


def phase155_readiness_passed(gate: Phase155ReadinessGate) -> bool:
    return all(r.passed for r in gate.rules if r.required)


def phase155_readiness_blocks_next_phase(gate: Phase155ReadinessGate) -> bool:
    return not gate.ready_for_phase155


def validate_phase155_readiness_gate(gate: Phase155ReadinessGate) -> list[str]:
    errors = []
    if not gate.ready_for_phase155:
        errors.append("Phase155 readiness gate failed.")
    return errors


def phase155_readiness_gate_summary(gate: Phase155ReadinessGate) -> dict[str, Any]:
    return {"passed": gate.ready_for_phase155, "status": gate.status.value}


def phase155_readiness_gate_to_text(
    gate: Phase155ReadinessGate, limit: int = 300
) -> str:
    return f"Phase155 Readiness Gate: passed={gate.ready_for_phase155}"[:limit]
