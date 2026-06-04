import datetime
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenarioPolicy,
    create_stress_scenario_policy_id
)
from usa_signal_bot.core.enums import StressScenarioKind, StressSeverityLevel, StressRobustnessRiskFlag

def build_default_stress_scenario_policy() -> StressScenarioPolicy:
    return build_custom_stress_scenario_policy(max_scenarios=32, deterministic_seed=151)

def build_custom_stress_scenario_policy(max_scenarios: int, deterministic_seed: int = 151) -> StressScenarioPolicy:
    valid = max_scenarios > 0
    errors = []
    if not valid:
        errors.append("max_scenarios must be > 0")

    return StressScenarioPolicy(
        policy_id=create_stress_scenario_policy_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        policy_name="default_stress_policy",
        scenario_kinds=[
            StressScenarioKind.PRICE_SHOCK,
            StressScenarioKind.VOLATILITY_SHOCK,
            StressScenarioKind.COST_SHOCK,
            StressScenarioKind.SLIPPAGE_SHOCK,
            StressScenarioKind.LIQUIDITY_SHOCK,
            StressScenarioKind.MISSING_DATA_SHOCK,
            StressScenarioKind.GAP_RISK_SHOCK,
            StressScenarioKind.DRAWDOWN_SHOCK,
            StressScenarioKind.COMBINED_ADVERSE_SHOCK
        ],
        severity_levels=[
            StressSeverityLevel.MILD,
            StressSeverityLevel.MODERATE,
            StressSeverityLevel.SEVERE,
            StressSeverityLevel.EXTREME
        ],
        deterministic_seed=deterministic_seed,
        max_scenarios=max_scenarios,
        price_shock_enabled=True,
        volatility_shock_enabled=True,
        cost_shock_enabled=True,
        slippage_shock_enabled=True,
        liquidity_shock_enabled=True,
        missing_data_shock_enabled=True,
        gap_risk_shock_enabled=True,
        drawdown_shock_enabled=True,
        combined_adverse_shock_enabled=True,
        policy_valid=valid,
        deterministic=True,
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[],
        errors=errors,
        risk_flags=[],
        metadata={}
    )

def validate_stress_scenario_policy(policy: StressScenarioPolicy) -> list[str]:
    errors = []
    if policy.max_scenarios <= 0:
        errors.append("max_scenarios must be positive")
    if not policy.deterministic:
        errors.append("Policy must be deterministic")
    if not policy.research_data_only:
        errors.append("Policy must be research_data_only")
    return errors
