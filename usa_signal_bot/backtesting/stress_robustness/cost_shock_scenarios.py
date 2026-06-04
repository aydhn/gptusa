import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    StressScenarioPolicy,
    create_stress_scenario_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel

def build_cost_shock_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.cost_shock_enabled:
        return []

    shocks = {
        StressSeverityLevel.MILD: 1.5,
        StressSeverityLevel.MODERATE: 2.0,
        StressSeverityLevel.SEVERE: 3.0,
        StressSeverityLevel.EXTREME: 5.0
    }

    scenarios = []
    for level, multiplier in shocks.items():
        if level in policy.severity_levels:
            scenarios.append(StressScenario(
                scenario_id=create_stress_scenario_id(),
                created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
                scenario_kind=StressScenarioKind.COST_SHOCK,
                severity_level=level,
                scenario_name=f"Cost Shock {level.value}",
                return_shock_multiplier=None,
                volatility_multiplier=None,
                cost_multiplier=multiplier,
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
