
from typing import List, Any, Dict
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def build_fill_realism_stress_scenarios() -> List[CostStressScenario]:
    modes = [FillRealismMode.OPTIMISTIC, FillRealismMode.BASELINE, FillRealismMode.CONSERVATIVE, FillRealismMode.PESSIMISTIC, FillRealismMode.STRICT]
    scenarios = []
    for mode in modes:
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"fill_{mode.value.lower()}"),
            name=f"Fill Realism Stress - {mode.value}",
            stress_type=CostStressType.FILL_REALISM,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=1.0,
            spread_multiplier=1.0,
            impact_multiplier=1.0,
            fee_multiplier=1.0,
            participation_multiplier=1.0,
            min_dollar_volume=None,
            fill_realism_mode=mode,
            enabled=True
        ))
    return scenarios

def fill_realism_mode_penalty_bps(mode: FillRealismMode) -> float:
    if mode == FillRealismMode.OPTIMISTIC:
        return 0.0
    elif mode == FillRealismMode.BASELINE:
        return 0.0
    elif mode == FillRealismMode.CONSERVATIVE:
        return 15.0
    elif mode == FillRealismMode.PESSIMISTIC:
        return 50.0
    elif mode == FillRealismMode.STRICT:
        return 100.0
    return 0.0

def apply_fill_realism_mode_to_trade(trade: Dict[str, Any], scenario: CostStressScenario) -> Dict[str, Any]:
    new_trade = dict(trade)
    penalty = fill_realism_mode_penalty_bps(scenario.fill_realism_mode)

    if 'metadata' not in new_trade:
        new_trade['metadata'] = {}

    new_trade['metadata']['fill_realism_mode_applied'] = scenario.fill_realism_mode.value
    new_trade['metadata']['fill_realism_penalty_bps'] = penalty

    if scenario.fill_realism_mode == FillRealismMode.STRICT:
        if new_trade.get('participation_pct', 0) > 10.0:
            new_trade['metadata']['fill_realism_blocked'] = True
            new_trade['warnings'] = new_trade.get('warnings', []) + ["Blocked by STRICT fill realism due to high participation"]

    return new_trade

def fill_realism_mode_to_text(mode: FillRealismMode) -> str:
    return f"FillRealismMode: {mode.value}"
