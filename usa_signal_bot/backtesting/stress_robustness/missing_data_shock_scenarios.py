import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    StressScenarioPolicy,
    create_stress_scenario_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel

def build_missing_data_shock_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.missing_data_shock_enabled:
        return []

    shocks = {
        StressSeverityLevel.MILD: 0.02,
        StressSeverityLevel.MODERATE: 0.05,
        StressSeverityLevel.SEVERE: 0.10,
        StressSeverityLevel.EXTREME: 0.20
    }

    scenarios = []
    for level, fraction in shocks.items():
        if level in policy.severity_levels:
            scenarios.append(StressScenario(
                scenario_id=create_stress_scenario_id(),
                created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
                scenario_kind=StressScenarioKind.MISSING_DATA_SHOCK,
                severity_level=level,
                scenario_name=f"Missing Data Shock {level.value}",
                return_shock_multiplier=None,
                volatility_multiplier=None,
                cost_multiplier=None,
                slippage_multiplier=None,
                liquidity_haircut=None,
                missing_data_fraction=fraction,
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
                metadata={"fraction": fraction}
            ))

    return scenarios
