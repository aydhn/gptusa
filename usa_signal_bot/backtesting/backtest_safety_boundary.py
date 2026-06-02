from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestSafetyBoundaryRule,
    BacktestSafetyBoundaryResult,
    create_backtest_safety_boundary_rule_id,
    create_backtest_safety_boundary_result_id
)
from usa_signal_bot.core.enums import BacktestSafetyRuleKind

def build_backtest_safety_boundary_rules(context_payload: dict[str, Any] | None = None) -> list[BacktestSafetyBoundaryRule]:
    ctx = context_payload or {}
    rules = []

    # helper for creating a rule
    def make_rule(kind: BacktestSafetyRuleKind, name: str, expected: bool, observed: bool, rationale: str) -> BacktestSafetyBoundaryRule:
        passed = (observed == expected)
        return BacktestSafetyBoundaryRule(
            rule_id=create_backtest_safety_boundary_rule_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            rule_kind=kind,
            name=name,
            required=True,
            passed=passed,
            expected_value=expected,
            observed_value=observed,
            rationale=rationale,
            warnings=[],
            errors=["Rule failed"] if not passed else [],
            risk_flags=[],
            metadata={}
        )

    # All these must be False in payload context to pass. The expected is False.
    # If payload says True, observed is True, so passed=False.
    checks = [
        (BacktestSafetyRuleKind.NO_LIVE_TRADING, "No live trading", ctx.get("live_trading_enabled", False)),
        (BacktestSafetyRuleKind.NO_PAPER_TRADING, "No paper trading", ctx.get("paper_trading_enabled", False)),
        (BacktestSafetyRuleKind.NO_BROKER_EXECUTION, "No broker execution", ctx.get("broker_execution_enabled", False)),
        (BacktestSafetyRuleKind.NO_ORDER_CREATION, "No order creation", ctx.get("order_creation_enabled", False)),
        (BacktestSafetyRuleKind.NO_PAPER_STATE_MUTATION, "No paper state mutation", ctx.get("paper_state_mutation_enabled", False)),
        (BacktestSafetyRuleKind.NO_TELEGRAM_REAL_SEND, "No Telegram real send", ctx.get("telegram_real_send_enabled", False)),
        (BacktestSafetyRuleKind.NO_STRATEGY_ACTIVATION, "No strategy activation", ctx.get("strategy_activation_allowed", False)),
        (BacktestSafetyRuleKind.NO_PORTFOLIO_ALLOCATION, "No portfolio allocation", ctx.get("portfolio_allocation_allowed", False)),
        (BacktestSafetyRuleKind.NO_DEPLOYMENT, "No deployment", ctx.get("deployment_allowed", False)),
        (BacktestSafetyRuleKind.NO_NETWORK, "No network", ctx.get("network_used", False)),
        (BacktestSafetyRuleKind.NO_DASHBOARD, "No dashboard", ctx.get("dashboard_started", False)),
        (BacktestSafetyRuleKind.NO_DAEMON, "No daemon", ctx.get("daemon_started", False)),
        (BacktestSafetyRuleKind.NO_SCHEDULER, "No scheduler", ctx.get("scheduler_enabled", False)),
        (BacktestSafetyRuleKind.NO_FULL_BACKTEST_RUN_PHASE146, "No full backtest run in Phase 146", ctx.get("full_backtest_run_executed", False)),
        (BacktestSafetyRuleKind.NO_WALK_FORWARD_PHASE146, "No walk forward in Phase 146", ctx.get("walk_forward_executed", False)),
        (BacktestSafetyRuleKind.NO_STRESS_TEST_PHASE146, "No stress test in Phase 146", ctx.get("stress_test_executed", False)),
        (BacktestSafetyRuleKind.NO_MONTE_CARLO_PHASE146, "No Monte Carlo in Phase 146", ctx.get("monte_carlo_executed", False)),
    ]

    for kind, name, observed in checks:
        rules.append(make_rule(kind, name, expected=False, observed=observed, rationale=f"{name} must be strictly disabled."))

    # Offline research expected True
    rules.append(make_rule(
        BacktestSafetyRuleKind.OFFLINE_BACKTEST_RESEARCH_ONLY,
        "Offline backtest research only",
        expected=True,
        observed=ctx.get("offline_backtest_research_only", True),
        rationale="Must strictly operate as offline backtest research."
    ))

    return rules

def build_backtest_safety_boundary_result(rules: list[BacktestSafetyBoundaryRule]) -> BacktestSafetyBoundaryResult:
    passed = all(r.passed for r in rules)

    # Helper to find observed
    def get_obs(kind: BacktestSafetyRuleKind, default: bool) -> bool:
        for r in rules:
            if r.rule_kind == kind:
                return bool(r.observed_value)
        return default

    return BacktestSafetyBoundaryResult(
        boundary_id=create_backtest_safety_boundary_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rules=rules,
        boundary_passed=passed,
        offline_backtest_research_only=get_obs(BacktestSafetyRuleKind.OFFLINE_BACKTEST_RESEARCH_ONLY, True),
        no_live_trading=not get_obs(BacktestSafetyRuleKind.NO_LIVE_TRADING, False),
        no_paper_trading=not get_obs(BacktestSafetyRuleKind.NO_PAPER_TRADING, False),
        no_broker_execution=not get_obs(BacktestSafetyRuleKind.NO_BROKER_EXECUTION, False),
        no_order_creation=not get_obs(BacktestSafetyRuleKind.NO_ORDER_CREATION, False),
        no_paper_state_mutation=not get_obs(BacktestSafetyRuleKind.NO_PAPER_STATE_MUTATION, False),
        no_telegram_real_send=not get_obs(BacktestSafetyRuleKind.NO_TELEGRAM_REAL_SEND, False),
        no_strategy_activation=not get_obs(BacktestSafetyRuleKind.NO_STRATEGY_ACTIVATION, False),
        no_portfolio_allocation=not get_obs(BacktestSafetyRuleKind.NO_PORTFOLIO_ALLOCATION, False),
        no_deployment=not get_obs(BacktestSafetyRuleKind.NO_DEPLOYMENT, False),
        no_network=not get_obs(BacktestSafetyRuleKind.NO_NETWORK, False),
        no_dashboard=not get_obs(BacktestSafetyRuleKind.NO_DASHBOARD, False),
        no_daemon=not get_obs(BacktestSafetyRuleKind.NO_DAEMON, False),
        no_scheduler=not get_obs(BacktestSafetyRuleKind.NO_SCHEDULER, False),
        no_full_backtest_run_phase146=not get_obs(BacktestSafetyRuleKind.NO_FULL_BACKTEST_RUN_PHASE146, False),
        no_walk_forward_phase146=not get_obs(BacktestSafetyRuleKind.NO_WALK_FORWARD_PHASE146, False),
        no_stress_test_phase146=not get_obs(BacktestSafetyRuleKind.NO_STRESS_TEST_PHASE146, False),
        no_monte_carlo_phase146=not get_obs(BacktestSafetyRuleKind.NO_MONTE_CARLO_PHASE146, False),
        research_data_only=True,
        warnings=[],
        errors=["Safety boundary failed"] if not passed else [],
        risk_flags=[],
        metadata={}
    )

def validate_backtest_safety_boundary_result(result: BacktestSafetyBoundaryResult) -> list[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Safety boundary failed.")
    for r in result.rules:
        if not r.passed:
            errors.append(f"Rule {r.name} failed.")
    return errors

def backtest_safety_boundary_passed(result: BacktestSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def backtest_safety_boundary_summary(result: BacktestSafetyBoundaryResult) -> dict[str, Any]:
    return {"passed": result.boundary_passed, "rules_count": len(result.rules)}

def backtest_safety_boundary_to_text(result: BacktestSafetyBoundaryResult, limit: int = 300) -> str:
    return f"SafetyBoundary(passed={result.boundary_passed}, rules={len(result.rules)})"
