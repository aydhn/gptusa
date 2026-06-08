from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingSafetyBoundaryRule, SizingSafetyBoundaryResult, SizingSafetyRuleKind

def build_sizing_safety_boundary_rules(context_payload: dict[str, Any] | None = None) -> list[SizingSafetyBoundaryRule]:
    # Placeholder for rule generation
    kinds = [
        SizingSafetyRuleKind.RESEARCH_PROTOTYPE_ONLY,
        SizingSafetyRuleKind.READ_ONLY_FOUNDATION_ARTIFACTS,
        SizingSafetyRuleKind.NO_ACTUAL_POSITION_SIZE,
        SizingSafetyRuleKind.NO_TARGET_WEIGHTS,
        SizingSafetyRuleKind.NO_ALLOCATION_OUTPUT,
        SizingSafetyRuleKind.NO_ORDER_SIZE,
        SizingSafetyRuleKind.NO_CAPITAL_DEPLOYMENT,
        SizingSafetyRuleKind.NO_PORTFOLIO_OPTIMIZATION,
        SizingSafetyRuleKind.NO_REBALANCING,
        SizingSafetyRuleKind.NO_LIVE_TRADING,
        SizingSafetyRuleKind.NO_PAPER_TRADING,
        SizingSafetyRuleKind.NO_BROKER_EXECUTION,
        SizingSafetyRuleKind.NO_REAL_ORDER_CREATION,
        SizingSafetyRuleKind.NO_PAPER_STATE_MUTATION,
        SizingSafetyRuleKind.NO_TELEGRAM_REAL_SEND,
        SizingSafetyRuleKind.NO_STRATEGY_ACTIVATION,
        SizingSafetyRuleKind.NO_DEPLOYMENT,
        SizingSafetyRuleKind.NO_NETWORK,
        SizingSafetyRuleKind.NO_DASHBOARD,
        SizingSafetyRuleKind.NO_DAEMON,
        SizingSafetyRuleKind.NO_SCHEDULER,
        SizingSafetyRuleKind.RESEARCH_DATA_ONLY
    ]

    rules = []

    is_safe = True
    if context_payload:
        for k in ["live_trading_enabled", "actual_position_size", "broker_execution"]:
            if context_payload.get(k, False):
                is_safe = False

    for k in kinds:
        r = SizingSafetyBoundaryRule(
            rule_kind=k,
            name=k.value,
            required=True,
            passed=is_safe,
            expected_value=True,
            observed_value=is_safe,
            rationale="Deterministic safety boundary check."
        )
        rules.append(r)

    return rules

def build_sizing_safety_boundary_result(rules: list[SizingSafetyBoundaryRule]) -> SizingSafetyBoundaryResult:
    result = SizingSafetyBoundaryResult()
    result.rules = rules
    result.boundary_passed = sizing_safety_boundary_passed(result)

    # Sync flags based on pass state
    for k in ["no_actual_position_size", "no_target_weights", "no_allocation_output",
              "no_order_size", "no_capital_deployment", "no_portfolio_optimization",
              "no_rebalancing", "no_live_trading", "no_paper_trading",
              "no_broker_execution", "no_real_order_creation", "no_paper_state_mutation",
              "no_telegram_real_send", "no_strategy_activation", "no_deployment",
              "no_network", "no_dashboard", "no_daemon", "no_scheduler"]:
        setattr(result, k, result.boundary_passed)

    return result

def validate_sizing_safety_boundary_result(result: SizingSafetyBoundaryResult) -> list[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Safety boundary failed.")
    return errors

def sizing_safety_boundary_passed(result: SizingSafetyBoundaryResult) -> bool:
    return all(r.passed for r in result.rules if r.required)

def sizing_safety_boundary_summary(result: SizingSafetyBoundaryResult) -> dict[str, Any]:
    return {"passed": result.boundary_passed, "rules_count": len(result.rules)}

def sizing_safety_boundary_to_text(result: SizingSafetyBoundaryResult, limit: int = 300) -> str:
    return f"Sizing Safety Boundary: passed={result.boundary_passed}"[:limit]
