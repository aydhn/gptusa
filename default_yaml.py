import os

file_path = "config/default.yaml"
content = """
cost_robustness:
  enabled: true
  write_robustness_reports: true
  warn_no_broker_execution: true
  warn_no_real_order_book: true
  warn_no_real_fill_guarantee: true
  warn_not_investment_advice: true

cost_stress_scenarios:
  enabled: true
  include_baseline: true
  include_mild: true
  include_moderate: true
  include_severe: true
  include_extreme: true
  max_default_scenarios: 12

slippage_stress:
  enabled: true
  multipliers:
    - 1.0
    - 1.5
    - 2.0
    - 3.0
  max_stressed_slippage_bps: 750.0

spread_stress:
  enabled: true
  multipliers:
    - 1.0
    - 1.5
    - 2.0
    - 3.0
  max_stressed_spread_bps: 750.0

market_impact_stress:
  enabled: true
  multipliers:
    - 1.0
    - 2.0
    - 3.0
  block_on_extreme_impact_in_strict_mode: true

fee_stress:
  enabled: true
  multipliers:
    - 1.0
    - 1.5
    - 2.0
  warn_fee_proxy_not_official: true

execution_sensitivity_matrix:
  enabled: true
  max_cells: 100
  include_fill_realism_axis: true
  include_slippage_axis: true
  include_spread_axis: true
  include_impact_axis: true
  prevent_combinatorial_explosion: true

walk_forward_cost_robustness:
  enabled: true
  require_out_of_sample_cost_survival: true
  fragile_window_threshold_pct: 30.0
  failed_scenario_threshold_pct: 40.0

cost_fragility:
  enabled: true
  min_breakeven_cost_bps_warning: 50.0
  min_breakeven_cost_bps_fail: 20.0
  profit_erased_by_costs_is_failure: true
  sharpe_collapse_threshold_pct: 50.0
  drawdown_expansion_threshold_pct: 50.0

cost_robustness_notifications:
  enabled: true
  dry_run: true
  notify_cost_robustness_report: true
  notify_cost_fragility_warning: true
  notify_execution_sensitivity_warning: true
  default_channel: "dry_run"
  warn_no_real_send_default: true
"""

if os.path.exists(file_path):
    with open(file_path, "a") as f:
        f.write("\n" + content)
else:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
