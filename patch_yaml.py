yaml_append = """
feature_factor_final_closure:
  enabled: true
  current_phase: 125
  final_phase: 160
  require_phase124_freeze_preparation: true
  final_artifact_chain_enabled: true
  final_closure_checks_enabled: true
  freeze_seal_enabled: true
  engine_readiness_certificate_enabled: true
  phase126_kickoff_gate_enabled: true
  write_final_closure_reports: true
  warn_not_investment_advice: true
  warn_phase125_is_not_activation: true
  warn_freeze_seal_is_not_deployment: true
  warn_phase126_gate_is_not_strategy_activation: true

phase125_final_closure_policy:
  compute_metadata_local_only: true
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
  produce_trade_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false
  produce_investment_advice: false
  strategy_activation_allowed: false

phase125_closure_requirements:
  require_phase124_ready: true
  require_final_artifact_chain_complete: true
  require_final_checks_passed: true
  require_freeze_seal_valid: true
  require_engine_certificate_valid: true
  require_phase126_gate_passed: true
  require_safety_pass: true
  ready_for_phase126_allowed: true

phase125_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""

for file_path in ["config/default.yaml", "config/local.example.yaml"]:
    with open(file_path, "a") as f:
        f.write("\n" + yaml_append)
