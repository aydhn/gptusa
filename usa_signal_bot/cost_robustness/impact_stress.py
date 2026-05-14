
from typing import List, Optional, Any, Dict
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def build_market_impact_stress_scenarios(multipliers: Optional[List[float]] = None) -> List[CostStressScenario]:
    if multipliers is None:
        multipliers = [1.0, 2.0, 3.0]
    scenarios = []
    for m in multipliers:
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"impact_{m}x"),
            name=f"Market Impact Stress {m}x",
            stress_type=CostStressType.MARKET_IMPACT,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=1.0,
            spread_multiplier=1.0,
            impact_multiplier=m,
            fee_multiplier=1.0,
            participation_multiplier=1.0,
            min_dollar_volume=None,
            fill_realism_mode=FillRealismMode.BASELINE,
            enabled=True
        ))
    return scenarios

def apply_impact_stress_to_breakdown(breakdown: Dict[str, Any], scenario: CostStressScenario) -> Dict[str, Any]:
    new_breakdown = dict(breakdown)
    if 'impact_bps' in new_breakdown and new_breakdown['impact_bps'] is not None:
        new_breakdown['impact_bps'] = new_breakdown['impact_bps'] * scenario.impact_multiplier
    else:
        new_breakdown['warnings'] = new_breakdown.get('warnings', []) + ["Missing impact_bps component"]
    return new_breakdown

def stress_market_impact_bps(base_impact_bps: Optional[float], scenario: CostStressScenario) -> Optional[float]:
    if base_impact_bps is None:
        return None
    return base_impact_bps * scenario.impact_multiplier

def impact_stress_summary_to_text(scenarios: List[CostStressScenario]) -> str:
    lines = ["--- Market Impact Stress Summary ---"]
    for s in scenarios:
        lines.append(f"{s.name}: multiplier {s.impact_multiplier}")
    return "\n".join(lines)
