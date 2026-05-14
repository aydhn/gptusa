
from typing import List, Optional, Any, Dict
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def build_fee_stress_scenarios(multipliers: Optional[List[float]] = None) -> List[CostStressScenario]:
    if multipliers is None:
        multipliers = [1.0, 1.5, 2.0]
    scenarios = []
    for m in multipliers:
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"fee_{m}x"),
            name=f"Fee Stress {m}x",
            stress_type=CostStressType.FEE,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=1.0,
            spread_multiplier=1.0,
            impact_multiplier=1.0,
            fee_multiplier=m,
            participation_multiplier=1.0,
            min_dollar_volume=None,
            fill_realism_mode=FillRealismMode.BASELINE,
            enabled=True
        ))
    return scenarios

def apply_fee_stress_to_breakdown(breakdown: Dict[str, Any], scenario: CostStressScenario) -> Dict[str, Any]:
    new_breakdown = dict(breakdown)
    if 'fee_bps' in new_breakdown and new_breakdown['fee_bps'] is not None:
        new_breakdown['fee_bps'] = new_breakdown['fee_bps'] * scenario.fee_multiplier
    else:
        new_breakdown['warnings'] = new_breakdown.get('warnings', []) + ["Missing fee_bps component"]
    return new_breakdown

def stress_fee_cost_bps(base_fee_bps: Optional[float], scenario: CostStressScenario) -> Optional[float]:
    if base_fee_bps is None:
        return None
    return base_fee_bps * scenario.fee_multiplier

def fee_stress_summary_to_text(scenarios: List[CostStressScenario]) -> str:
    lines = ["--- Fee/Commission Stress Summary ---"]
    for s in scenarios:
        lines.append(f"{s.name}: multiplier {s.fee_multiplier}")
    return "\n".join(lines)
