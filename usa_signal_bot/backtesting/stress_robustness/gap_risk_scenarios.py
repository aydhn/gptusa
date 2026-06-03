import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    StressScenarioPolicy,
    create_stress_scenario_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel

def build_gap_risk_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.gap_risk_shock_enabled:
        return []

    shocks = {
        StressSeverityLevel.MILD: -0.03,
        StressSeverityLevel.MODERATE: -0.07,
        StressSeverityLevel.SEVERE: -0.15,
        StressSeverityLevel.EXTREME: -0.30
    }

    scenarios = []
    for level, return_shock in shocks.items():
        if level in policy.severity_levels:
            scenarios.append(StressScenario(
                scenario_id=create_stress_scenario_id(),
                created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
                scenario_kind=StressScenarioKind.GAP_RISK_SHOCK,
                severity_level=level,
                scenario_name=f"Gap Risk Shock {level.value}",
                return_shock_multiplier=None,
                volatility_multiplier=None,
                cost_multiplier=None,
                slippage_multiplier=None,
                liquidity_haircut=None,
                missing_data_fraction=None,
                gap_return_shock=return_shock,
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
                metadata={"return_shock": return_shock}
            ))

    return scenarios
