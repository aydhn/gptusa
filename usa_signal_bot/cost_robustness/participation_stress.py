
from typing import List, Optional
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def build_participation_stress_scenarios(multipliers: Optional[List[float]] = None) -> List[CostStressScenario]:
    if multipliers is None:
        multipliers = [1.0, 1.5, 2.0]
    scenarios = []
    for m in multipliers:
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"part_{m}x"),
            name=f"Participation Stress {m}x",
            stress_type=CostStressType.PARTICIPATION,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=1.0,
            spread_multiplier=1.0,
            impact_multiplier=1.0,
            fee_multiplier=1.0,
            participation_multiplier=m,
            min_dollar_volume=None,
            fill_realism_mode=FillRealismMode.BASELINE,
            enabled=True
        ))
    return scenarios

def stress_participation_rate(base_participation_pct: Optional[float], scenario: CostStressScenario) -> Optional[float]:
    if base_participation_pct is None:
        return None
    return base_participation_pct * scenario.participation_multiplier

def participation_stress_risk_label(participation_pct: Optional[float]) -> str:
    if participation_pct is None:
        return "UNKNOWN"
    if participation_pct > 10.0:
        return "CRITICAL"
    elif participation_pct > 5.0:
        return "HIGH"
    return "LOW"

def participation_stress_summary_to_text(scenarios: List[CostStressScenario]) -> str:
    lines = ["--- Participation Stress Summary ---"]
    for s in scenarios:
        lines.append(f"{s.name}: multiplier {s.participation_multiplier}")
    return "\n".join(lines)
