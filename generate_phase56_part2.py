import os
import re

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# STRESS SCENARIOS (cost_robustness/stress_scenarios.py)
# ---------------------------------------------------------
stress_scenarios_content = """
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/stress_scenarios.py", stress_scenarios_content)

# ---------------------------------------------------------
# SLIPPAGE STRESS (cost_robustness/slippage_stress.py)
# ---------------------------------------------------------
slippage_stress_content = """
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/slippage_stress.py", slippage_stress_content)

# ---------------------------------------------------------
# SPREAD STRESS (cost_robustness/spread_stress.py)
# ---------------------------------------------------------
spread_stress_content = """
from typing import List, Optional, Any, Dict
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, create_cost_stress_scenario_id

def build_spread_stress_scenarios(multipliers: Optional[List[float]] = None) -> List[CostStressScenario]:
    if multipliers is None:
        multipliers = [1.0, 1.5, 2.0, 3.0]
    scenarios = []
    for m in multipliers:
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"spread_{m}x"),
            name=f"Spread Stress {m}x",
            stress_type=CostStressType.SPREAD,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=1.0,
            spread_multiplier=m,
            impact_multiplier=1.0,
            fee_multiplier=1.0,
            participation_multiplier=1.0,
            min_dollar_volume=None,
            fill_realism_mode=FillRealismMode.BASELINE,
            enabled=True
        ))
    return scenarios

def apply_spread_stress_to_breakdown(breakdown: Dict[str, Any], scenario: CostStressScenario) -> Dict[str, Any]:
    new_breakdown = dict(breakdown)
    if 'spread_bps' in new_breakdown and new_breakdown['spread_bps'] is not None:
        new_breakdown['spread_bps'] = new_breakdown['spread_bps'] * scenario.spread_multiplier
    else:
        new_breakdown['warnings'] = new_breakdown.get('warnings', []) + ["Missing spread_bps component"]
    return new_breakdown

def stress_spread_cost_bps(base_spread_cost_bps: Optional[float], scenario: CostStressScenario) -> Optional[float]:
    if base_spread_cost_bps is None:
        return None
    return base_spread_cost_bps * scenario.spread_multiplier

def spread_stress_summary_to_text(scenarios: List[CostStressScenario]) -> str:
    lines = ["--- Spread Stress Summary ---"]
    for s in scenarios:
        lines.append(f"{s.name}: multiplier {s.spread_multiplier}")
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/spread_stress.py", spread_stress_content)

# ---------------------------------------------------------
# IMPACT STRESS (cost_robustness/impact_stress.py)
# ---------------------------------------------------------
impact_stress_content = """
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/impact_stress.py", impact_stress_content)

# ---------------------------------------------------------
# FEE STRESS (cost_robustness/fee_stress.py)
# ---------------------------------------------------------
fee_stress_content = """
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/fee_stress.py", fee_stress_content)

# ---------------------------------------------------------
# PARTICIPATION STRESS (cost_robustness/participation_stress.py)
# ---------------------------------------------------------
participation_stress_content = """
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/participation_stress.py", participation_stress_content)

# ---------------------------------------------------------
# LIQUIDITY FILTER STRESS (cost_robustness/liquidity_filter_stress.py)
# ---------------------------------------------------------
liquidity_filter_stress_content = """
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/liquidity_filter_stress.py", liquidity_filter_stress_content)

# ---------------------------------------------------------
# FILL REALISM STRESS (cost_robustness/fill_realism_stress.py)
# ---------------------------------------------------------
fill_realism_stress_content = """
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
"""
write_file("usa_signal_bot/cost_robustness/fill_realism_stress.py", fill_realism_stress_content)
