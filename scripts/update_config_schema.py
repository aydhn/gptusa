import re

def update_config_schema():
    with open('usa_signal_bot/core/config_schema.py', 'r') as f:
        content = f.read()

    new_dataclasses = """
@dataclass
class RegimeAwareCostsConfig:
    enabled: bool = True
    write_regime_cost_reports: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_order_book: bool = True
    warn_no_real_fill_guarantee: bool = True
    warn_not_investment_advice: bool = True

@dataclass
class VolatilityRegimeCostConfig:
    enabled: bool = True
    low_atr_pct: float = 1.0
    normal_atr_pct: float = 3.0
    high_atr_pct: float = 6.0
    extreme_gap_pct: float = 10.0
    very_low_multiplier: float = 0.85
    low_multiplier: float = 0.95
    normal_multiplier: float = 1.0
    high_multiplier: float = 1.5
    extreme_multiplier: float = 2.5
    insufficient_data_multiplier: float = 1.25

@dataclass
class LiquidityRegimeCostConfig:
    enabled: bool = True
    deep_adv_usd: float = 100000000.0
    normal_adv_usd: float = 10000000.0
    thin_adv_usd: float = 2000000.0
    deep_multiplier: float = 0.8
    normal_multiplier: float = 1.0
    thin_multiplier: float = 1.75
    illiquid_multiplier: float = 3.0
    frozen_multiplier: float = 5.0
    insufficient_data_multiplier: float = 1.5

@dataclass
class SpreadRegimeCostConfig:
    enabled: bool = True
    tight_spread_bps: float = 20.0
    normal_spread_bps: float = 80.0
    wide_spread_bps: float = 200.0
    tight_multiplier: float = 0.85
    normal_multiplier: float = 1.0
    wide_multiplier: float = 1.75
    very_wide_multiplier: float = 2.75
    unreliable_multiplier: float = 3.5
    insufficient_data_multiplier: float = 1.25

@dataclass
class SessionRegimeCostConfig:
    enabled: bool = True
    regular_multiplier: float = 1.0
    opening_window_multiplier: float = 1.4
    closing_window_multiplier: float = 1.25
    premarket_multiplier: float = 2.5
    after_hours_multiplier: float = 2.25
    closed_multiplier: float = 5.0
    block_closed_session_fill: bool = True

@dataclass
class LifecycleRegimeCostConfig:
    enabled: bool = True
    normal_multiplier: float = 1.0
    corporate_action_watch_multiplier: float = 1.5
    post_split_window_multiplier: float = 2.0
    adjusted_data_risk_multiplier: float = 2.5
    lifecycle_review_multiplier: float = 2.5
    delisting_risk_multiplier: float = 4.0
    require_review_on_lifecycle_risk: bool = True

@dataclass
class AdaptiveExecutionRealismConfig:
    enabled: bool = True
    use_regime_cost_curve_selection: bool = True
    use_conservative_costs_on_missing_data: bool = True
    block_fill_on_closed_session: bool = True
    block_fill_on_frozen_liquidity: bool = True
    require_review_on_high_risk_regime: bool = True
    block_signal_metadata_on_blocked_regime: bool = True

@dataclass
class RegimeCostCurveSelectionConfig:
    enabled: bool = True
    default_profile: str = "baseline"
    high_risk_profile: str = "stressed"
    blocked_profile: str = "blocked"
    max_combined_multiplier: float = 8.0
    min_adjusted_cost_bps: float = 1.0
    max_adjusted_cost_bps: float = 1000.0

@dataclass
class RegimeCostNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_regime_cost_report: bool = True
    notify_adaptive_execution_warning: bool = True
    notify_regime_cost_block_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
"""

    if "RegimeAwareCostsConfig" not in content:
        # Find where to insert (before class AppConfig)
        parts = content.split("class AppConfig:")
        if len(parts) == 2:
            new_content = parts[0] + new_dataclasses + "\nclass AppConfig:\n" + parts[1]

            # Now append them to AppConfig
            app_config_additions = """
    regime_aware_costs: RegimeAwareCostsConfig = field(default_factory=RegimeAwareCostsConfig)
    volatility_regime_cost: VolatilityRegimeCostConfig = field(default_factory=VolatilityRegimeCostConfig)
    liquidity_regime_cost: LiquidityRegimeCostConfig = field(default_factory=LiquidityRegimeCostConfig)
    spread_regime_cost: SpreadRegimeCostConfig = field(default_factory=SpreadRegimeCostConfig)
    session_regime_cost: SessionRegimeCostConfig = field(default_factory=SessionRegimeCostConfig)
    lifecycle_regime_cost: LifecycleRegimeCostConfig = field(default_factory=LifecycleRegimeCostConfig)
    adaptive_execution_realism: AdaptiveExecutionRealismConfig = field(default_factory=AdaptiveExecutionRealismConfig)
    regime_cost_curve_selection: RegimeCostCurveSelectionConfig = field(default_factory=RegimeCostCurveSelectionConfig)
    regime_cost_notifications: RegimeCostNotificationsConfig = field(default_factory=RegimeCostNotificationsConfig)
"""
            # find end of AppConfig
            last_field_idx = new_content.rfind("= field(default_factory=")
            end_of_line_idx = new_content.find("\n", last_field_idx)

            final_content = new_content[:end_of_line_idx] + app_config_additions + new_content[end_of_line_idx:]

            with open('usa_signal_bot/core/config_schema.py', 'w') as f:
                f.write(final_content)

update_config_schema()
