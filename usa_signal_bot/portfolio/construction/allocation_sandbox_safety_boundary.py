from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.construction.phase155_models import (
    AllocationSandboxSafetyBoundaryRule,
    AllocationSandboxSafetyBoundaryResult,
    AllocationSandboxSafetyRuleKind,
    create_allocation_sandbox_safety_boundary_rule_id,
    create_allocation_sandbox_safety_boundary_result_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_allocation_sandbox_safety_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[AllocationSandboxSafetyBoundaryRule]:
    if context_payload is None:
        context_payload = {}

    rules = []

    # helper for creating rule
    def _rule(kind: AllocationSandboxSafetyRuleKind, name: str, expected: bool, observed: bool, rationale: str):
        rules.append(AllocationSandboxSafetyBoundaryRule(
            rule_id=create_allocation_sandbox_safety_boundary_rule_id(),
            created_at_utc=_now_str(),
            rule_kind=kind,
            name=name,
            required=True,
            passed=(expected == observed),
            expected_value=expected,
            observed_value=observed,
            rationale=rationale,
            warnings=[],
            errors=[] if expected == observed else [f"Failed: Expected {expected}, got {observed}"],
            risk_flags=[],
            metadata={}
        ))

    _rule(
        AllocationSandboxSafetyRuleKind.RESEARCH_ALLOCATION_SANDBOX_ONLY,
        "Research Allocation Sandbox Only",
        True,
        context_payload.get("research_allocation_sandbox_only", True),
        "Must be a research sandbox."
    )

    _rule(
        AllocationSandboxSafetyRuleKind.READ_ONLY_SIZING_ARTIFACTS,
        "Read Only Sizing Artifacts",
        True,
        context_payload.get("read_only_sizing_artifacts", True),
        "Must treat phase 154 outputs as read-only."
    )

    _rule(
        AllocationSandboxSafetyRuleKind.NO_ACTUAL_TARGET_WEIGHTS,
        "No Actual Target Weights",
        False,
        context_payload.get("actual_target_weights_produced", False),
        "Must not produce actual target weights."
    )

    _rule(
        AllocationSandboxSafetyRuleKind.NO_ACTUAL_ALLOCATION,
        "No Actual Allocation",
        False,
        context_payload.get("actual_allocation_produced", False),
        "Must not produce actual allocation."
    )

    _rule(
        AllocationSandboxSafetyRuleKind.NO_ORDER_SIZE,
        "No Order Size",
        False,
        context_payload.get("order_size_produced", False),
        "Must not produce order size."
    )

    _rule(
        AllocationSandboxSafetyRuleKind.NO_CAPITAL_DEPLOYMENT,
        "No Capital Deployment",
        False,
        context_payload.get("capital_deployment_allowed", False),
        "Must not allow capital deployment."
    )

    _rule(
        AllocationSandboxSafetyRuleKind.NO_LIVE_TRADING,
        "No Live Trading",
        False,
        context_payload.get("live_trading_enabled", False),
        "Must not allow live trading."
    )

    _rule(
        AllocationSandboxSafetyRuleKind.NO_BROKER_EXECUTION,
        "No Broker Execution",
        False,
        context_payload.get("broker_execution_enabled", False),
        "Must not allow broker execution."
    )

    return rules

def build_allocation_sandbox_safety_boundary_result(rules: List[AllocationSandboxSafetyBoundaryRule]) -> AllocationSandboxSafetyBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    return AllocationSandboxSafetyBoundaryResult(
        boundary_id=create_allocation_sandbox_safety_boundary_result_id(),
        created_at_utc=_now_str(),
        rules=rules,
        boundary_passed=passed,
        research_allocation_sandbox_only=True,
        read_only_sizing_artifacts=True,
        no_actual_target_weights=True,
        no_actual_portfolio_weights=True,
        no_actual_allocation=True,
        no_actual_position_size=True,
        no_order_size=True,
        no_capital_deployment=True,
        no_portfolio_optimization=True,
        no_rebalancing_execution=True,
        no_live_trading=True,
        no_paper_trading=True,
        no_broker_execution=True,
        no_real_order_creation=True,
        no_paper_state_mutation=True,
        no_telegram_real_send=True,
        no_strategy_activation=True,
        no_deployment=True,
        no_network=True,
        no_dashboard=True,
        no_daemon=True,
        no_scheduler=True,
        research_data_only=True,
        warnings=[],
        errors=[] if passed else ["Boundary failed due to one or more rules failing."],
        risk_flags=[],
        metadata={}
    )

def validate_allocation_sandbox_safety_boundary_result(result: AllocationSandboxSafetyBoundaryResult) -> List[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Boundary passed is False.")
        result.risk_flags.append(PortfolioConstructionRiskFlag.SAFETY_BOUNDARY_FAILED)

    for rule in result.rules:
        if rule.required and not rule.passed:
            errors.append(f"Rule {rule.name} failed.")

    return errors

def allocation_sandbox_safety_boundary_passed(result: AllocationSandboxSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def allocation_sandbox_safety_boundary_summary(result: AllocationSandboxSafetyBoundaryResult) -> Dict[str, Any]:
    return {
        "boundary_id": result.boundary_id,
        "passed": result.boundary_passed,
        "rule_count": len(result.rules),
        "failed_rules": [r.name for r in result.rules if r.required and not r.passed]
    }

def allocation_sandbox_safety_boundary_to_text(result: AllocationSandboxSafetyBoundaryResult, limit: int = 300) -> str:
    summary = allocation_sandbox_safety_boundary_summary(result)
    return (
        f"Safety Boundary: {summary['boundary_id']}\n"
        f"Passed: {summary['passed']}\n"
        f"Failed Rules: {', '.join(summary['failed_rules']) if summary['failed_rules'] else 'None'}"
    )
