def update_yaml():
    with open('config/default.yaml', 'a') as f:
        f.write("""
regime_aware_costs:
  enabled: true
  write_regime_cost_reports: true
  warn_no_broker_execution: true
  warn_no_real_order_book: true
  warn_no_real_fill_guarantee: true
  warn_not_investment_advice: true

volatility_regime_cost:
  enabled: true
  low_atr_pct: 1.0
  normal_atr_pct: 3.0
  high_atr_pct: 6.0
  extreme_gap_pct: 10.0
  very_low_multiplier: 0.85
  low_multiplier: 0.95
  normal_multiplier: 1.0
  high_multiplier: 1.5
  extreme_multiplier: 2.5
  insufficient_data_multiplier: 1.25

liquidity_regime_cost:
  enabled: true
  deep_adv_usd: 100000000
  normal_adv_usd: 10000000
  thin_adv_usd: 2000000
  deep_multiplier: 0.8
  normal_multiplier: 1.0
  thin_multiplier: 1.75
  illiquid_multiplier: 3.0
  frozen_multiplier: 5.0
  insufficient_data_multiplier: 1.5

spread_regime_cost:
  enabled: true
  tight_spread_bps: 20.0
  normal_spread_bps: 80.0
  wide_spread_bps: 200.0
  tight_multiplier: 0.85
  normal_multiplier: 1.0
  wide_multiplier: 1.75
  very_wide_multiplier: 2.75
  unreliable_multiplier: 3.5
  insufficient_data_multiplier: 1.25

session_regime_cost:
  enabled: true
  regular_multiplier: 1.0
  opening_window_multiplier: 1.4
  closing_window_multiplier: 1.25
  premarket_multiplier: 2.5
  after_hours_multiplier: 2.25
  closed_multiplier: 5.0
  block_closed_session_fill: true

lifecycle_regime_cost:
  enabled: true
  normal_multiplier: 1.0
  corporate_action_watch_multiplier: 1.5
  post_split_window_multiplier: 2.0
  adjusted_data_risk_multiplier: 2.5
  lifecycle_review_multiplier: 2.5
  delisting_risk_multiplier: 4.0
  require_review_on_lifecycle_risk: true

adaptive_execution_realism:
  enabled: true
  use_regime_cost_curve_selection: true
  use_conservative_costs_on_missing_data: true
  block_fill_on_closed_session: true
  block_fill_on_frozen_liquidity: true
  require_review_on_high_risk_regime: true
  block_signal_metadata_on_blocked_regime: true

regime_cost_curve_selection:
  enabled: true
  default_profile: "baseline"
  high_risk_profile: "stressed"
  blocked_profile: "blocked"
  max_combined_multiplier: 8.0
  min_adjusted_cost_bps: 1.0
  max_adjusted_cost_bps: 1000.0

regime_cost_notifications:
  enabled: true
  dry_run: true
  notify_regime_cost_report: true
  notify_adaptive_execution_warning: true
  notify_regime_cost_block_warning: true
  default_channel: "dry_run"
  warn_no_real_send_default: true
""")

    with open('config/local.example.yaml', 'a') as f:
        f.write("""
regime_aware_costs:
  enabled: true
  write_regime_cost_reports: true
""")

update_yaml()
