cat >> config/default.yaml << 'EOL'

factor_scoring:
  enabled: true
  current_phase: 121
  final_phase: 160
  require_phase120_factor_composition: true
  factor_scoring_enabled: true
  factor_normalization_enabled: true
  factor_diagnostics_enabled: true
  factor_table_builder_enabled: true
  write_factor_scoring_reports: true
  warn_not_investment_advice: true
  warn_phase121_is_not_activation: true
  warn_factor_scores_are_not_trade_signals: true

phase121_factor_policy:
  compute_values_local_only: true
  research_data_only: true
  local_fixture_only_default: true
  allow_network: false
  allow_paid_api: false
  allow_scraping: false
  allow_html_parsing: false
  allow_broker: false
  allow_order: false
  allow_paper_mutation: false
  allow_telegram_real_send: false
  allow_dashboard: false
  produce_trade_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false
  strategy_activation_allowed: false

phase121_factor_normalization:
  enabled: true
  default_method: "Z_SCORE"
  winsorization_enabled: true
  lower_pct: 0.01
  upper_pct: 0.99
  cross_sectional_ranks_enabled: true
  produce_trade_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false

phase121_factor_table:
  preserve_enriched_feature_columns: true
  preserve_warmup_nulls: true
  block_forbidden_columns: true
  allow_macd_signal_line_column: true
  write_factor_tables: true
  overwrite_factor_tables_default: false

phase121_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
EOL
