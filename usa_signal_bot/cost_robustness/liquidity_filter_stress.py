
from typing import List, Optional, Any, Dict, Tuple
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def build_liquidity_filter_stress_scenarios(min_dollar_volume_values: Optional[List[float]] = None) -> List[CostStressScenario]:
    if min_dollar_volume_values is None:
        min_dollar_volume_values = [1_000_000.0, 5_000_000.0, 10_000_000.0]
    scenarios = []
    for val in min_dollar_volume_values:
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"liq_{val}"),
            name=f"Liquidity Filter Stress (Min ${val})",
            stress_type=CostStressType.LIQUIDITY_FILTER,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=1.0,
            spread_multiplier=1.0,
            impact_multiplier=1.0,
            fee_multiplier=1.0,
            participation_multiplier=1.0,
            min_dollar_volume=val,
            fill_realism_mode=FillRealismMode.BASELINE,
            enabled=True
        ))
    return scenarios

def symbol_passes_liquidity_filter(avg_dollar_volume: Optional[float], scenario: CostStressScenario) -> bool:
    if scenario.min_dollar_volume is None:
        return True
    if avg_dollar_volume is None:
        return False
    return avg_dollar_volume >= scenario.min_dollar_volume

def apply_liquidity_filter_to_trades(trades: List[Dict[str, Any]], scenario: CostStressScenario) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    kept = []
    skipped = []
    for trade in trades:
        adv = trade.get('avg_dollar_volume')
        if symbol_passes_liquidity_filter(adv, scenario):
            kept.append(trade)
        else:
            skipped.append(trade)
    return kept, skipped

def liquidity_filter_stress_summary_to_text(scenarios: List[CostStressScenario]) -> str:
    lines = ["--- Liquidity Filter Stress Summary ---"]
    for s in scenarios:
        lines.append(f"{s.name}: min_dollar_volume {s.min_dollar_volume}")
    return "\n".join(lines)
