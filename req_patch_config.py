import json

with open("config/default.yaml", "r") as f:
    content = f.read()

config_add = """
market_behavior_reporting:
  enabled: true
  current_phase: 130
  final_phase: 160
  require_phase129_regime_transition_analytics: true
  behavior_profiles_enabled: true
  regime_behavior_summaries_enabled: true
  diagnostics_interpretation_enabled: true
  report_document_enabled: true
  report_qa_enabled: true
  readiness_gate_enabled: true
  write_market_behavior_reports: true
  warn_not_investment_advice: true
  warn_phase130_is_not_activation: true
  warn_behavior_profiles_are_not_trade_signals: true

phase130_behavior_policy:
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
  allow_deployment: false
  allow_model_training: false
  allow_model_prediction: false
  allow_heavy_ml_dependencies: false
  produce_trade_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false
  produce_investment_advice: false
  strategy_activation_allowed: false

phase130_report_policy:
  formats:
    - MARKDOWN
    - JSON
    - TEXT
  require_qa_pass: true
  block_investment_advice_language: true
  block_trade_signal_language: true
  block_order_decision_language: true
  block_portfolio_allocation_language: true
  block_guarantee_language: true
  block_broker_execution_language: true
  block_deployment_language: true
  overwrite_reports_default: false

phase130_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""
if "market_behavior_reporting:" not in content:
    with open("config/default.yaml", "a") as f:
        f.write("\n" + config_add)

with open("config/local.example.yaml", "r") as f:
    content_local = f.read()
if "market_behavior_reporting:" not in content_local:
    with open("config/local.example.yaml", "a") as f:
        f.write("\nmarket_behavior_reporting:\n  enabled: true\n")

print("Updated config files.")
