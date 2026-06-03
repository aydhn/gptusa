from typing import Any
from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressRobustnessContext,
    StressValidationReport,
    MonteCarloRobustnessReport,
    ScenarioReplayResult,
    MonteCarloReplayResult,
    RobustnessScorecard,
    StressSafetyBoundaryResult,
    Phase152ReadinessGate
)
from usa_signal_bot.core.enums import StressRobustnessRiskFlag
import pandas as pd

def validate_stress_robustness_context_safety(context: StressRobustnessContext) -> list[str]:
    errors = []
    if context.live_trading_enabled:
        errors.append("live_trading_enabled is true")
    if context.paper_trading_enabled:
        errors.append("paper_trading_enabled is true")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled is true")
    if context.real_order_creation_enabled:
        errors.append("real_order_creation_enabled is true")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled is true")
    if context.strategy_activation_allowed:
        errors.append("strategy_activation_allowed is true")
    if context.portfolio_optimization_enabled:
        errors.append("portfolio_optimization_enabled is true")
    if context.portfolio_allocation_output_enabled:
        errors.append("portfolio_allocation_output_enabled is true")
    if context.deployment_allowed:
        errors.append("deployment_allowed is true")
    return errors

def validate_stress_validation_report_safety(report: StressValidationReport) -> list[str]:
    errors = []
    if report.portfolio_optimization_enabled:
        errors.append("portfolio_optimization_enabled is true in report")
    if report.strategy_activation_allowed:
        errors.append("strategy_activation_allowed is true in report")
    if report.investment_advice:
        errors.append("investment_advice is true in report")
    return errors

def collect_stress_risk_flags(context: StressRobustnessContext | None = None) -> list[StressRobustnessRiskFlag]:
    if not context:
        return []
    flags = []
    if context.live_trading_enabled:
        flags.append(StressRobustnessRiskFlag.LIVE_TRADING_RISK)
    if context.portfolio_optimization_enabled:
        flags.append(StressRobustnessRiskFlag.PORTFOLIO_OPTIMIZATION_RISK)
    return flags
