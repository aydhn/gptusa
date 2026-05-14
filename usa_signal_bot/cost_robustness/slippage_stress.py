
from typing import List, Optional, Any, Dict
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def build_slippage_stress_scenarios(multipliers: Optional[List[float]] = None) -> List[CostStressScenario]:
    if multipliers is None:
        multipliers = [1.0, 1.5, 2.0, 3.0]
    scenarios = []
    for m in multipliers:
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"slip_{m}x"),
            name=f"Slippage Stress {m}x",
            stress_type=CostStressType.SLIPPAGE,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=m,
            spread_multiplier=1.0,
            impact_multiplier=1.0,
            fee_multiplier=1.0,
            participation_multiplier=1.0,
            min_dollar_volume=None,
            fill_realism_mode=FillRealismMode.BASELINE,
            enabled=True
        ))
    return scenarios

def apply_slippage_stress_to_breakdown(breakdown: Dict[str, Any], scenario: CostStressScenario) -> Dict[str, Any]:
    new_breakdown = dict(breakdown)
    if 'slippage_bps' in new_breakdown and new_breakdown['slippage_bps'] is not None:
        new_breakdown['slippage_bps'] = new_breakdown['slippage_bps'] * scenario.slippage_multiplier
    else:
        new_breakdown['warnings'] = new_breakdown.get('warnings', []) + ["Missing slippage_bps component"]
    return new_breakdown

def stress_slippage_bps(base_slippage_bps: Optional[float], scenario: CostStressScenario) -> Optional[float]:
    if base_slippage_bps is None:
        return None
    return base_slippage_bps * scenario.slippage_multiplier

def slippage_stress_summary_to_text(scenarios: List[CostStressScenario]) -> str:
    lines = ["--- Slippage Stress Summary ---"]
    for s in scenarios:
        lines.append(f"{s.name}: multiplier {s.slippage_multiplier}")
    return "\n".join(lines)
