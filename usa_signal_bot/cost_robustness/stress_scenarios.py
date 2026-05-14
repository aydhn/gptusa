
from typing import List
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def baseline_cost_scenario() -> CostStressScenario:
    return CostStressScenario(
        scenario_id=create_cost_stress_scenario_id("baseline"),
        name="Baseline Scenario",
        stress_type=CostStressType.SLIPPAGE,
        severity=CostStressSeverity.BASELINE,
        slippage_multiplier=1.0,
        spread_multiplier=1.0,
        impact_multiplier=1.0,
        fee_multiplier=1.0,
        participation_multiplier=1.0,
        min_dollar_volume=None,
        fill_realism_mode=FillRealismMode.BASELINE,
        enabled=True
    )

def mild_cost_stress_scenario() -> CostStressScenario:
    return CostStressScenario(
        scenario_id=create_cost_stress_scenario_id("mild"),
        name="Mild Cost Stress",
        stress_type=CostStressType.COMBINED,
        severity=CostStressSeverity.MILD,
        slippage_multiplier=1.25,
        spread_multiplier=1.25,
        impact_multiplier=1.25,
        fee_multiplier=1.0,
        participation_multiplier=1.0,
        min_dollar_volume=None,
        fill_realism_mode=FillRealismMode.CONSERVATIVE,
        enabled=True
    )

def moderate_cost_stress_scenario() -> CostStressScenario:
    return CostStressScenario(
        scenario_id=create_cost_stress_scenario_id("moderate"),
        name="Moderate Cost Stress",
        stress_type=CostStressType.COMBINED,
        severity=CostStressSeverity.MODERATE,
        slippage_multiplier=1.5,
        spread_multiplier=1.5,
        impact_multiplier=1.5,
        fee_multiplier=1.25,
        participation_multiplier=1.0,
        min_dollar_volume=None,
        fill_realism_mode=FillRealismMode.CONSERVATIVE,
        enabled=True
    )

def severe_cost_stress_scenario() -> CostStressScenario:
    return CostStressScenario(
        scenario_id=create_cost_stress_scenario_id("severe"),
        name="Severe Cost Stress",
        stress_type=CostStressType.COMBINED,
        severity=CostStressSeverity.SEVERE,
        slippage_multiplier=2.0,
        spread_multiplier=2.0,
        impact_multiplier=2.0,
        fee_multiplier=1.5,
        participation_multiplier=1.0,
        min_dollar_volume=None,
        fill_realism_mode=FillRealismMode.PESSIMISTIC,
        enabled=True
    )

def extreme_cost_stress_scenario() -> CostStressScenario:
    return CostStressScenario(
        scenario_id=create_cost_stress_scenario_id("extreme"),
        name="Extreme Cost Stress",
        stress_type=CostStressType.COMBINED,
        severity=CostStressSeverity.EXTREME,
        slippage_multiplier=3.0,
        spread_multiplier=3.0,
        impact_multiplier=3.0,
        fee_multiplier=2.0,
        participation_multiplier=1.0,
        min_dollar_volume=None,
        fill_realism_mode=FillRealismMode.STRICT,
        enabled=True
    )

def default_cost_stress_scenarios() -> List[CostStressScenario]:
    return [
        baseline_cost_scenario(),
        mild_cost_stress_scenario(),
        moderate_cost_stress_scenario(),
        severe_cost_stress_scenario(),
        extreme_cost_stress_scenario()
    ]

def combined_cost_stress_scenarios() -> List[CostStressScenario]:
    return default_cost_stress_scenarios()

def filter_enabled_scenarios(scenarios: List[CostStressScenario]) -> List[CostStressScenario]:
    return [s for s in scenarios if s.enabled]

def stress_scenarios_to_text(scenarios: List[CostStressScenario]) -> str:
    lines = ["--- Cost Stress Scenarios ---"]
    for s in scenarios:
        lines.append(f"{s.name} ({s.severity.value}) - Enabled: {s.enabled}")
    return "\n".join(lines)
