import os

file_path = "usa_signal_bot/core/config_schema.py"

content = """
from dataclasses import dataclass, field
from typing import List

@dataclass
class CostRobustnessConfig:
    enabled: bool = True
    write_robustness_reports: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_order_book: bool = True
    warn_no_real_fill_guarantee: bool = True
    warn_not_investment_advice: bool = True

@dataclass
class CostStressScenariosConfig:
    enabled: bool = True
    include_baseline: bool = True
    include_mild: bool = True
    include_moderate: bool = True
    include_severe: bool = True
    include_extreme: bool = True
    max_default_scenarios: int = 12

@dataclass
class SlippageStressConfig:
    enabled: bool = True
    multipliers: List[float] = field(default_factory=lambda: [1.0, 1.5, 2.0, 3.0])
    max_stressed_slippage_bps: float = 750.0

@dataclass
class SpreadStressConfig:
    enabled: bool = True
    multipliers: List[float] = field(default_factory=lambda: [1.0, 1.5, 2.0, 3.0])
    max_stressed_spread_bps: float = 750.0

@dataclass
class MarketImpactStressConfig:
    enabled: bool = True
    multipliers: List[float] = field(default_factory=lambda: [1.0, 2.0, 3.0])
    block_on_extreme_impact_in_strict_mode: bool = True

@dataclass
class FeeStressConfig:
    enabled: bool = True
    multipliers: List[float] = field(default_factory=lambda: [1.0, 1.5, 2.0])
    warn_fee_proxy_not_official: bool = True

@dataclass
class ExecutionSensitivityMatrixConfig:
    enabled: bool = True
    max_cells: int = 100
    include_fill_realism_axis: bool = True
    include_slippage_axis: bool = True
    include_spread_axis: bool = True
    include_impact_axis: bool = True
    prevent_combinatorial_explosion: bool = True

@dataclass
class WalkForwardCostRobustnessConfig:
    enabled: bool = True
    require_out_of_sample_cost_survival: bool = True
    fragile_window_threshold_pct: float = 30.0
    failed_scenario_threshold_pct: float = 40.0

@dataclass
class CostFragilityConfig:
    enabled: bool = True
    min_breakeven_cost_bps_warning: float = 50.0
    min_breakeven_cost_bps_fail: float = 20.0
    profit_erased_by_costs_is_failure: bool = True
    sharpe_collapse_threshold_pct: float = 50.0
    drawdown_expansion_threshold_pct: float = 50.0

@dataclass
class CostRobustnessNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_cost_robustness_report: bool = True
    notify_cost_fragility_warning: bool = True
    notify_execution_sensitivity_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
"""

if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
else:
    with open(file_path, "a") as f:
        f.write("\n" + content)
