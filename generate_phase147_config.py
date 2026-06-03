import re
import os

schema_path = "usa_signal_bot/core/config_schema.py"
with open(schema_path, "r") as f:
    schema_content = f.read()

new_schema = """
@dataclass
class Phase147BacktestRunPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    local_fixture_only_default: bool = True
    allow_offline_deterministic_backtest_run: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_real_order_creation: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_trading: bool = False
    allow_paper_trading: bool = False
    allow_strategy_activation: bool = False
    allow_portfolio_optimization: bool = False
    allow_walk_forward: bool = False
    allow_stress_test: bool = False
    allow_monte_carlo: bool = False
    allow_benchmark_comparison: bool = False
    allow_scheduler: bool = False
    allow_background_daemon: bool = False
    produce_live_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False

@dataclass
class Phase147RunDefaultsConfig:
    initial_cash: float = 100000.0
    currency: str = "USD"
    deterministic_seed: int = 147
    exposure_side: str = "LONG_ONLY_RESEARCH"
    max_single_symbol_exposure_fraction: float = 1.0
    allow_fractional_shares: bool = False
    allow_short_exposure: bool = False
    allow_leverage: bool = False
    default_fill_policy: str = "NEXT_BAR_OPEN"
    require_deterministic_hashes: bool = True

@dataclass
class Phase147NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class RealisticBacktestRunConfig:
    enabled: bool = True
    current_phase: int = 147
    final_phase: int = 160
    require_phase146_backtest_foundation: bool = True
    backtest_foundation_ingestion_enabled: bool = True
    artifact_loader_enabled: bool = True
    input_resolver_enabled: bool = True
    run_config_enabled: bool = True
    research_decision_stream_enabled: bool = True
    simulation_clock_enabled: bool = True
    price_event_stream_enabled: bool = True
    simulated_execution_enabled: bool = True
    cost_application_enabled: bool = True
    liquidity_partial_fill_enabled: bool = True
    exposure_timeline_enabled: bool = True
    equity_curve_enabled: bool = True
    drawdown_curve_enabled: bool = True
    ledger_enabled: bool = True
    basic_performance_enabled: bool = True
    safety_boundary_enabled: bool = True
    validation_gate_enabled: bool = True
    write_backtest_run_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_simulated_fills_are_not_orders: bool = True
    warn_backtest_run_is_offline_only: bool = True
    policy: Phase147BacktestRunPolicyConfig = field(default_factory=Phase147BacktestRunPolicyConfig)
    run_defaults: Phase147RunDefaultsConfig = field(default_factory=Phase147RunDefaultsConfig)
    notifications: Phase147NotificationsConfig = field(default_factory=Phase147NotificationsConfig)
"""

if "RealisticBacktestRunConfig" not in schema_content:
    # insert before AppConfig
    parts = schema_content.split("AppConfig = Config")
    new_content = parts[0] + new_schema + "\nAppConfig = Config" + (parts[1] if len(parts) > 1 else "")

    # insert into Config
    new_content = re.sub(
        r'(class Config:)',
        r'\1\n    realistic_backtest_run: RealisticBacktestRunConfig = field(default_factory=RealisticBacktestRunConfig)',
        new_content
    )

    with open(schema_path, "w") as f:
        f.write(new_content)
    print("Schema updated.")

yaml_path = "config/default.yaml"
with open(yaml_path, "r") as f:
    yaml_content = f.read()

new_yaml = """
realistic_backtest_run:
  enabled: true
  current_phase: 147
  final_phase: 160
  require_phase146_backtest_foundation: true
  backtest_foundation_ingestion_enabled: true
  artifact_loader_enabled: true
  input_resolver_enabled: true
  run_config_enabled: true
  research_decision_stream_enabled: true
  simulation_clock_enabled: true
  price_event_stream_enabled: true
  simulated_execution_enabled: true
  cost_application_enabled: true
  liquidity_partial_fill_enabled: true
  exposure_timeline_enabled: true
  equity_curve_enabled: true
  drawdown_curve_enabled: true
  ledger_enabled: true
  basic_performance_enabled: true
  safety_boundary_enabled: true
  validation_gate_enabled: true
  write_backtest_run_reports: true
  warn_not_investment_advice: true
  warn_simulated_fills_are_not_orders: true
  warn_backtest_run_is_offline_only: true
  policy:
    compute_values_local_only: true
    research_data_only: true
    offline_backtest_research_only: true
    local_fixture_only_default: true
    allow_offline_deterministic_backtest_run: true
    allow_network: false
    allow_paid_api: false
    allow_scraping: false
    allow_html_parsing: false
    allow_broker: false
    allow_real_order_creation: false
    allow_paper_mutation: false
    allow_telegram_real_send: false
    allow_dashboard: false
    allow_deployment: false
    allow_live_trading: false
    allow_paper_trading: false
    allow_strategy_activation: false
    allow_portfolio_optimization: false
    allow_walk_forward: false
    allow_stress_test: false
    allow_monte_carlo: false
    allow_benchmark_comparison: false
    allow_scheduler: false
    allow_background_daemon: false
    produce_live_signals: false
    produce_order_decisions: false
    produce_portfolio_weights: false
    produce_investment_advice: false
  run_defaults:
    initial_cash: 100000.0
    currency: USD
    deterministic_seed: 147
    exposure_side: LONG_ONLY_RESEARCH
    max_single_symbol_exposure_fraction: 1.0
    allow_fractional_shares: false
    allow_short_exposure: false
    allow_leverage: false
    default_fill_policy: NEXT_BAR_OPEN
    require_deterministic_hashes: true
  notifications:
    enabled: true
    dry_run: true
    preview_only: true
    telegram_real_send: false
"""

if "realistic_backtest_run:" not in yaml_content:
    with open(yaml_path, "a") as f:
        f.write("\n" + new_yaml)
    print("YAML updated.")
