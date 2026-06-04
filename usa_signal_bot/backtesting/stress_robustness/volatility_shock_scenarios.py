import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    StressScenarioPolicy,
    create_stress_scenario_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel

def build_volatility_shock_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.volatility_shock_enabled:
        return []

    shocks = {
        StressSeverityLevel.MILD: 1.25,
        StressSeverityLevel.MODERATE: 1.50,
        StressSeverityLevel.SEVERE: 2.00,
        StressSeverityLevel.EXTREME: 3.00
    }

    scenarios = []
    for level, multiplier in shocks.items():
        if level in policy.severity_levels:
            scenarios.append(StressScenario(
                scenario_id=create_stress_scenario_id(),
                created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
                scenario_kind=StressScenarioKind.VOLATILITY_SHOCK,
                severity_level=level,
                scenario_name=f"Volatility Shock {level.value}",
                return_shock_multiplier=None,
                volatility_multiplier=multiplier,
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
