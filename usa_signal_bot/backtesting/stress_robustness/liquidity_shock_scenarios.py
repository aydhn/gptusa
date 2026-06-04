import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    StressScenarioPolicy,
    create_stress_scenario_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel

def build_liquidity_shock_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.liquidity_shock_enabled:
        return []

    shocks = {
        StressSeverityLevel.MILD: 0.10,
        StressSeverityLevel.MODERATE: 0.25,
        StressSeverityLevel.SEVERE: 0.50,
        StressSeverityLevel.EXTREME: 0.75
    }

    scenarios = []
    for level, haircut in shocks.items():
        if level in policy.severity_levels:
            scenarios.append(StressScenario(
                scenario_id=create_stress_scenario_id(),
                created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
                scenario_kind=StressScenarioKind.LIQUIDITY_SHOCK,
                severity_level=level,
                scenario_name=f"Liquidity Shock {level.value}",
                return_shock_multiplier=None,
                volatility_multiplier=None,
                cost_multiplier=None,
                slippage_multiplier=None,
                liquidity_haircut=haircut,
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
                metadata={"haircut": haircut}
            ))

    return scenarios
