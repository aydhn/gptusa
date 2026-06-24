from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioFoundationSafetyBoundaryResult,
    PortfolioFoundationSafetyBoundaryRule,
    PortfolioFoundationSafetyRuleKind,
)

UNSAFE_FLAGS = [
    "live_trading_enabled",
    "paper_trading_enabled",
    "broker_execution_enabled",
    "real_order_creation_enabled",
    "paper_state_mutation_enabled",
    "telegram_real_send_enabled",
    "strategy_activation_allowed",
    "actual_portfolio_construction_executed",
    "actual_position_sizing_executed",
    "portfolio_optimization_enabled",
    "rebalancing_enabled",
    "target_weights_produced",
    "allocation_output_produced",
    "capital_deployment_allowed",
    "deployment_allowed",
    "network_used",
    "dashboard_started",
    "daemon_started",
    "scheduler_enabled",
]


def _find_unsafe_flags(context_payload: dict[str, Any] | None) -> list[str]:
    if not context_payload:
        return []
    return [unsafe for unsafe in UNSAFE_FLAGS if context_payload.get(unsafe, False)]


def build_portfolio_foundation_safety_boundary_rules(
    context_payload: dict[str, Any] | None = None,
) -> list[PortfolioFoundationSafetyBoundaryRule]:
    unsafe_flags = _find_unsafe_flags(context_payload)
    rules = []

    kinds = [
        PortfolioFoundationSafetyRuleKind.READ_ONLY_HANDOFF_INGESTION,
        PortfolioFoundationSafetyRuleKind.CONTRACT_ONLY_PORTFOLIO_FOUNDATION,
        PortfolioFoundationSafetyRuleKind.NO_ACTUAL_PORTFOLIO_CONSTRUCTION,
        PortfolioFoundationSafetyRuleKind.NO_POSITION_SIZING,
        PortfolioFoundationSafetyRuleKind.NO_TARGET_WEIGHTS,
        PortfolioFoundationSafetyRuleKind.NO_ALLOCATION_OUTPUT,
        PortfolioFoundationSafetyRuleKind.NO_CAPITAL_DEPLOYMENT,
        PortfolioFoundationSafetyRuleKind.NO_PORTFOLIO_OPTIMIZATION,
        PortfolioFoundationSafetyRuleKind.NO_REBALANCING,
        PortfolioFoundationSafetyRuleKind.NO_LIVE_TRADING,
        PortfolioFoundationSafetyRuleKind.NO_PAPER_TRADING,
        PortfolioFoundationSafetyRuleKind.NO_BROKER_EXECUTION,
        PortfolioFoundationSafetyRuleKind.NO_REAL_ORDER_CREATION,
        PortfolioFoundationSafetyRuleKind.NO_PAPER_STATE_MUTATION,
        PortfolioFoundationSafetyRuleKind.NO_TELEGRAM_REAL_SEND,
        PortfolioFoundationSafetyRuleKind.NO_STRATEGY_ACTIVATION,
        PortfolioFoundationSafetyRuleKind.NO_DEPLOYMENT,
        PortfolioFoundationSafetyRuleKind.NO_NETWORK,
        PortfolioFoundationSafetyRuleKind.NO_DASHBOARD,
        PortfolioFoundationSafetyRuleKind.NO_DAEMON,
        PortfolioFoundationSafetyRuleKind.NO_SCHEDULER,
        PortfolioFoundationSafetyRuleKind.RESEARCH_DATA_ONLY,
    ]

    for kind in kinds:
        r = PortfolioFoundationSafetyBoundaryRule()
        r.rule_kind = kind
        r.name = kind.value
        r.passed = len(unsafe_flags) == 0

        for unsafe in unsafe_flags:
            r.errors.append(f"Found unsafe context flag: {unsafe}")

        rules.append(r)

    return rules


def build_portfolio_foundation_safety_boundary_result(
    rules: list[PortfolioFoundationSafetyBoundaryRule],
) -> PortfolioFoundationSafetyBoundaryResult:
    res = PortfolioFoundationSafetyBoundaryResult()
    res.rules = rules
    res.boundary_passed = all(r.passed for r in rules)
    return res


def validate_portfolio_foundation_safety_boundary_result(
    result: PortfolioFoundationSafetyBoundaryResult,
) -> list[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Safety boundary did not pass")
    for field in [
        "read_only_handoff_ingestion",
        "contract_only_portfolio_foundation",
        "no_actual_portfolio_construction",
        "no_position_sizing",
        "no_target_weights",
        "no_allocation_output",
        "no_capital_deployment",
        "no_portfolio_optimization",
        "no_rebalancing",
        "no_live_trading",
        "no_paper_trading",
        "no_broker_execution",
        "no_real_order_creation",
        "no_paper_state_mutation",
        "no_telegram_real_send",
        "no_strategy_activation",
        "no_deployment",
        "no_network",
        "no_dashboard",
        "no_daemon",
        "no_scheduler",
        "research_data_only",
    ]:
        if not getattr(result, field):
            errors.append(f"Safety constraint {field} must be True")
    return errors


def portfolio_foundation_safety_boundary_passed(
    result: PortfolioFoundationSafetyBoundaryResult,
) -> bool:
    return result.boundary_passed


def portfolio_foundation_safety_boundary_summary(
    result: PortfolioFoundationSafetyBoundaryResult,
) -> dict[str, Any]:
    return {"passed": result.boundary_passed, "rule_count": len(result.rules)}


def portfolio_foundation_safety_boundary_to_text(
    result: PortfolioFoundationSafetyBoundaryResult, limit: int = 300
) -> str:
    return f"PortfolioFoundationSafetyBoundary: passed={result.boundary_passed}"
