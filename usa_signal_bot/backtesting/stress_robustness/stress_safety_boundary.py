import datetime
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressSafetyBoundaryRule,
    StressSafetyBoundaryResult,
    create_stress_safety_boundary_rule_id,
    create_stress_safety_boundary_result_id
)
from usa_signal_bot.core.enums import StressSafetyRuleKind

def build_stress_safety_boundary_rules(context_payload: dict[str, Any] | None = None) -> list[StressSafetyBoundaryRule]:
    ctx = context_payload or {}

    rules = [
        _create_rule(StressSafetyRuleKind.OFFLINE_STRESS_MONTE_CARLO_ONLY, True, True, ctx.get("offline_backtest_research_only", True), "Must run offline"),
        _create_rule(StressSafetyRuleKind.READ_ONLY_WALK_FORWARD_ARTIFACTS, True, True, ctx.get("read_only_walk_forward_artifacts", True), "Inputs must be read-only"),
        _create_rule(StressSafetyRuleKind.LOCAL_INPUTS_ONLY, True, True, ctx.get("local_inputs_only", True), "Must use local inputs"),
        _create_rule(StressSafetyRuleKind.DETERMINISTIC_RANDOM_SEED_REQUIRED, True, True, ctx.get("deterministic", True), "Must be deterministic"),
        _create_rule(StressSafetyRuleKind.NO_LIVE_TRADING, False, False, ctx.get("live_trading_enabled", False), "No live trading allowed"),
        _create_rule(StressSafetyRuleKind.NO_PAPER_TRADING, False, False, ctx.get("paper_trading_enabled", False), "No paper trading allowed"),
        _create_rule(StressSafetyRuleKind.NO_BROKER_EXECUTION, False, False, ctx.get("broker_execution_enabled", False), "No broker allowed"),
        _create_rule(StressSafetyRuleKind.NO_REAL_ORDER_CREATION, False, False, ctx.get("real_order_creation_enabled", False), "No real orders"),
        _create_rule(StressSafetyRuleKind.NO_PAPER_STATE_MUTATION, False, False, ctx.get("paper_state_mutation_enabled", False), "No paper state mutation"),
        _create_rule(StressSafetyRuleKind.NO_TELEGRAM_REAL_SEND, False, False, ctx.get("telegram_real_send_enabled", False), "No telegram send"),
        _create_rule(StressSafetyRuleKind.NO_STRATEGY_ACTIVATION, False, False, ctx.get("strategy_activation_allowed", False), "No strategy activation"),
        _create_rule(StressSafetyRuleKind.NO_PORTFOLIO_OPTIMIZATION, False, False, ctx.get("portfolio_optimization_enabled", False), "No portfolio optimization"),
        _create_rule(StressSafetyRuleKind.NO_PORTFOLIO_ALLOCATION_OUTPUT, False, False, ctx.get("portfolio_allocation_output_enabled", False), "No portfolio allocation"),
        _create_rule(StressSafetyRuleKind.NO_DEPLOYMENT, False, False, ctx.get("deployment_allowed", False), "No deployment"),
        _create_rule(StressSafetyRuleKind.NO_NETWORK, False, False, ctx.get("network_used", False), "No network fetch"),
        _create_rule(StressSafetyRuleKind.NO_DASHBOARD, False, False, ctx.get("dashboard_started", False), "No dashboard"),
        _create_rule(StressSafetyRuleKind.NO_DAEMON, False, False, ctx.get("daemon_started", False), "No daemon"),
        _create_rule(StressSafetyRuleKind.NO_SCHEDULER, False, False, ctx.get("scheduler_enabled", False), "No scheduler")
    ]
    return rules

def _create_rule(kind: StressSafetyRuleKind, expected: bool, expected_val: Any, observed: Any, rationale: str) -> StressSafetyBoundaryRule:
    passed = observed == expected_val
    return StressSafetyBoundaryRule(
        rule_id=create_stress_safety_boundary_rule_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        rule_kind=kind,
        name=kind.value,
        required=True,
        passed=passed,
        expected_value=expected_val,
        observed_value=observed,
        rationale=rationale,
        warnings=[], errors=[] if passed else [f"Rule failed: expected {expected_val}, got {observed}"],
        risk_flags=[], metadata={}
    )

def build_stress_safety_boundary_result(rules: list[StressSafetyBoundaryRule]) -> StressSafetyBoundaryResult:
    passed = all(r.passed for r in rules)
    return StressSafetyBoundaryResult(
        boundary_id=create_stress_safety_boundary_result_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        rules=rules,
        boundary_passed=passed,
        offline_stress_monte_carlo_only=True,
        read_only_walk_forward_artifacts=True,
        local_inputs_only=True,
        deterministic_random_seed_required=True,
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
        research_data_only=True,
        warnings=[], errors=[] if passed else ["Boundary check failed"], risk_flags=[], metadata={}
    )

def stress_safety_boundary_passed(result: StressSafetyBoundaryResult) -> bool:
    return result.boundary_passed
