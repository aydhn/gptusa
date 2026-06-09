from pathlib import Path

path = Path("config/default.yaml")
content = ""
if path.exists():
    content = path.read_text()

new_config = """
full_system_integration:
  enabled: true
  current_phase: 158
  final_phase: 160
  require_phase157_portfolio_risk_handoff: true
  phase158_handoff_ingestion_enabled: true
  artifact_loader_enabled: true
  integration_input_resolver_enabled: true
  artifact_inventory_enabled: true
  dependency_graph_enabled: true
  boundary_contract_enabled: true
  e2e_rehearsal_plan_enabled: true
  dry_run_rehearsal_executor_enabled: true
  acceptance_result_enabled: true
  schema_compatibility_report_enabled: true
  cli_integration_report_enabled: true
  config_integration_report_enabled: true
  storage_integration_report_enabled: true
  health_integration_report_enabled: true
  quality_observability_report_enabled: true
  notification_dry_run_report_enabled: true
  safety_boundary_enabled: true
  final_delivery_preparation_checklist_enabled: true
  phase159_readiness_gate_enabled: true
  write_full_system_integration_reports: true
  warn_integration_only: true
  warn_dry_run_only: true
  warn_not_deployment_approval: true
  warn_not_trading_approval: true
  warn_not_investment_advice: true

phase158_integration_policy:
  compute_values_local_only: true
  research_data_only: true
  integration_only: true
  dry_run_only: true
  local_fixture_only_default: true
  read_only_phase158_handoff: true
  allow_full_system_integration: true
  allow_e2e_rehearsal: true
  allow_local_artifact_write: true
  allow_live_trading: false
  allow_paper_state_mutation: false
  allow_broker_execution: false
  allow_real_order_creation: false
  allow_telegram_real_send: false
  allow_strategy_activation: false
  allow_deployment: false
  allow_production_patch: false
  allow_network: false
  allow_paid_api: false
  allow_scraping: false
  allow_html_parsing: false
  allow_dashboard: false
  allow_daemon: false
  allow_scheduler: false
  allow_actual_target_weights: false
  allow_actual_allocation: false
  allow_order_size: false
  allow_capital_deployment: false
  produce_live_signals: false
  produce_order_decisions: false
  produce_investment_advice: false

phase158_rehearsal_defaults:
  deterministic_seed: 158
  dry_run: true
  preview_only: true
  local_fixture_only: true
  no_real_side_effects: true
  no_network: true
  no_paper_mutation: true
  no_broker_execution: true
  no_real_orders: true
  no_telegram_real_send: true
  no_deployment: true
  require_deterministic_hashes: true

phase158_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""
if "full_system_integration:" not in content:
    path.write_text(content + "\n" + new_config)
