file_path = "config/default.yaml"
with open(file_path, "r") as f:
    content = f.read()

new_config = """
regime_research_freeze:
  enabled: true
  current_phase: 134
  final_phase: 160
  require_phase133_regime_monitoring: true
  monitoring_artifact_loader_enabled: true
  monitoring_validation_enabled: true
  drift_report_enabled: true
  drift_report_qa_enabled: true
  freeze_package_enabled: true
  freeze_readiness_gate_enabled: true
  write_research_freeze_reports: true
  warn_not_investment_advice: true
  warn_phase134_is_not_activation: true
  warn_freeze_package_is_not_deployment: true

phase134_freeze_policy:
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
  allow_background_daemon: false
  allow_scheduler: false
  produce_trade_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false
  produce_investment_advice: false
  strategy_activation_allowed: false

phase134_drift_report_qa:
  enabled: true
  require_qa_pass: true
  block_investment_advice_language: true
  block_trade_signal_language: true
  block_order_decision_language: true
  block_portfolio_allocation_language: true
  block_guarantee_language: true
  block_broker_execution_language: true
  block_deployment_language: true
  block_live_monitoring_language: true
  overwrite_reports_default: false

phase134_freeze_package:
  enabled: true
  package_version: "phase134.v1"
  require_required_artifact_coverage: true
  require_package_hash: true
  require_manifest_hash: true
  ready_for_phase135_allowed: true

phase134_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""

if "regime_research_freeze:" not in content:
    content += "\n" + new_config

with open(file_path, "w") as f:
    f.write(content)
