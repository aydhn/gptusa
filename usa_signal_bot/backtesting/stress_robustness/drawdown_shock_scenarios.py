import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    StressScenarioPolicy,
    create_stress_scenario_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel

def build_drawdown_shock_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.drawdown_shock_enabled:
        return []

    shocks = {
        StressSeverityLevel.MILD: 0.10,
        StressSeverityLevel.MODERATE: 0.20,
        StressSeverityLevel.SEVERE: 0.35,
        StressSeverityLevel.EXTREME: 0.50
    }

    scenarios = []
    for level, floor in shocks.items():
        if level in policy.severity_levels:
            scenarios.append(StressScenario(
                scenario_id=create_stress_scenario_id(),
                created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
                scenario_kind=StressScenarioKind.DRAWDOWN_SHOCK,
                severity_level=level,
                scenario_name=f"Drawdown Shock {level.value}",
                return_shock_multiplier=None,
                volatility_multiplier=None,
                cost_multiplier=None,
                slippage_multiplier=None,
                liquidity_haircut=None,
                missing_data_fraction=None,
                gap_return_shock=None,
                drawdown_shock_floor=floor,
                combined=False,
                scenario_valid=True,
                deterministic=True,
                not_investment_advice=True,
                not_strategy_activation=True,
                research_data_only=True,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={"floor": floor}
            ))

    return scenarios

def build_combined_adverse_scenarios(policy: StressScenarioPolicy) -> list[StressScenario]:
    if not policy.combined_adverse_shock_enabled:
        return []

    scenarios = []

    if StressSeverityLevel.SEVERE in policy.severity_levels:
        scenarios.append(StressScenario(
            scenario_id=create_stress_scenario_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            scenario_kind=StressScenarioKind.COMBINED_ADVERSE_SHOCK,
            severity_level=StressSeverityLevel.SEVERE,
            scenario_name="Combined Adverse Severe",
            return_shock_multiplier=0.80,
            volatility_multiplier=2.00,
            cost_multiplier=3.0,
            slippage_multiplier=3.0,
            liquidity_haircut=0.50,
            missing_data_fraction=0.10,
            gap_return_shock=-0.15,
            drawdown_shock_floor=None,
            combined=True,
            scenario_valid=True,
            deterministic=True,
            not_investment_advice=True,
            not_strategy_activation=True,
            research_data_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    if StressSeverityLevel.EXTREME in policy.severity_levels:
        scenarios.append(StressScenario(
            scenario_id=create_stress_scenario_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            scenario_kind=StressScenarioKind.COMBINED_ADVERSE_SHOCK,
            severity_level=StressSeverityLevel.EXTREME,
            scenario_name="Combined Adverse Extreme",
            return_shock_multiplier=0.65,
            volatility_multiplier=3.00,
            cost_multiplier=5.0,
            slippage_multiplier=5.0,
            liquidity_haircut=0.75,
            missing_data_fraction=0.20,
            gap_return_shock=-0.30,
            drawdown_shock_floor=None,
            combined=True,
            scenario_valid=True,
            deterministic=True,
            not_investment_advice=True,
            not_strategy_activation=True,
            research_data_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    return scenarios
