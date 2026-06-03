from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardSafetyRuleKind, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardSafetyBoundaryRule,
    WalkForwardSafetyBoundaryResult,
    create_walk_forward_safety_boundary_rule_id,
    create_walk_forward_safety_boundary_result_id,
    _now_utc
)

def _build_rule(kind: WalkForwardSafetyRuleKind, passed: bool, val: Any) -> WalkForwardSafetyBoundaryRule:
    return WalkForwardSafetyBoundaryRule(
        rule_id=create_walk_forward_safety_boundary_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=kind,
        name=kind.value,
        required=True,
        passed=passed,
        expected_value=not passed, # Usually expected is opposite of violating flag
        observed_value=val,
        rationale=f"Checking {kind.value}"
    )

def build_walk_forward_safety_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[WalkForwardSafetyBoundaryRule]:
    payload = context_payload or {}
    rules = [
        _build_rule(WalkForwardSafetyRuleKind.OFFLINE_WALK_FORWARD_ONLY, payload.get("offline_backtest_research_only", True), True),
        _build_rule(WalkForwardSafetyRuleKind.NO_LIVE_TRADING, not payload.get("live_trading_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_PAPER_TRADING, not payload.get("paper_trading_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_BROKER_EXECUTION, not payload.get("broker_execution_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_REAL_ORDER_CREATION, not payload.get("real_order_creation_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_PAPER_STATE_MUTATION, not payload.get("paper_state_mutation_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_TELEGRAM_REAL_SEND, not payload.get("telegram_real_send_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_STRATEGY_ACTIVATION, not payload.get("strategy_activation_allowed", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_PORTFOLIO_OPTIMIZATION, not payload.get("portfolio_optimization_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_PORTFOLIO_ALLOCATION_OUTPUT, not payload.get("portfolio_allocation_output_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_DEPLOYMENT, not payload.get("deployment_allowed", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_NETWORK, not payload.get("network_used", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_DASHBOARD, not payload.get("dashboard_started", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_DAEMON, not payload.get("daemon_started", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_SCHEDULER, not payload.get("scheduler_enabled", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_STRESS_TEST_PHASE150, not payload.get("stress_test_executed", False), False),
        _build_rule(WalkForwardSafetyRuleKind.NO_MONTE_CARLO_PHASE150, not payload.get("monte_carlo_executed", False), False)
    ]
    return rules

def build_walk_forward_safety_boundary_result(rules: List[WalkForwardSafetyBoundaryRule]) -> WalkForwardSafetyBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    result = WalkForwardSafetyBoundaryResult(
        boundary_id=create_walk_forward_safety_boundary_result_id(),
        created_at_utc=_now_utc(),
        rules=rules,
        boundary_passed=passed,
        offline_walk_forward_only=True,
        read_only_benchmark_artifacts=True,
        local_inputs_only=True,
        no_live_trading=True,
        no_paper_trading=True,
        no_broker_execution=True,
        no_real_order_creation=True,
        no_paper_state_mutation=True,
        no_telegram_real_send=True,
        no_strategy_activation=True,
        no_portfolio_optimization=True,
        no_portfolio_allocation_output=True,
        no_deployment=True,
        no_network=True,
        no_dashboard=True,
        no_daemon=True,
        no_scheduler=True,
        no_stress_test_phase150=True,
        no_monte_carlo_phase150=True,
        research_data_only=True
    )

    errors = validate_walk_forward_safety_boundary_result(result)
    if errors:
        result.boundary_passed = False
        result.errors = errors
        result.risk_flags.append(WalkForwardRiskFlag.SAFETY_BOUNDARY_FAILED)

    return result

def validate_walk_forward_safety_boundary_result(result: WalkForwardSafetyBoundaryResult) -> List[str]:
    errors = []
    failed_rules = [r.name for r in result.rules if r.required and not r.passed]
    if failed_rules:
        errors.append(f"Safety boundary failed rules: {failed_rules}")
    return errors

def walk_forward_safety_boundary_passed(result: WalkForwardSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def walk_forward_safety_boundary_summary(result: WalkForwardSafetyBoundaryResult) -> Dict[str, Any]:
    return {
        "passed": result.boundary_passed,
        "total_rules": len(result.rules),
        "failed_rules": sum(1 for r in result.rules if not r.passed)
    }

def walk_forward_safety_boundary_to_text(result: WalkForwardSafetyBoundaryResult, limit: int = 300) -> str:
    summary = walk_forward_safety_boundary_summary(result)
    lines = [
        f"Walk Forward Safety Boundary:",
        f"  Passed: {summary['passed']}",
        f"  Failed Rules: {summary['failed_rules']}/{summary['total_rules']}"
    ]
    return "\n".join(lines)[:limit]
