import datetime
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    StressScenarioPolicy,
    create_stress_scenario_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel

def build_price_shock_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.price_shock_enabled:
        return []

    shocks = {
        StressSeverityLevel.MILD: 0.95,
        StressSeverityLevel.MODERATE: 0.90,
        StressSeverityLevel.SEVERE: 0.80,
        StressSeverityLevel.EXTREME: 0.65
    }

    scenarios = []
    for level, multiplier in shocks.items():
        if level in policy.severity_levels:
            scenarios.append(StressScenario(
                scenario_id=create_stress_scenario_id(),
                created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
                scenario_kind=StressScenarioKind.PRICE_SHOCK,
                severity_level=level,
                scenario_name=f"Price Shock {level.value}",
                return_shock_multiplier=multiplier,
                volatility_multiplier=None,
                cost_multiplier=None,
                slippage_multiplier=None,
                liquidity_haircut=None,
                missing_data_fraction=None,
                gap_return_shock=None,
                drawdown_shock_floor=None,
                combined=False,
                scenario_valid=True,
                deterministic=True,
                not_investment_advice=True,
                not_strategy_activation=True,
                research_data_only=True,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={"multiplier": multiplier}
            ))

    return scenarios
