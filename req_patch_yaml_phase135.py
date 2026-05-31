import sys

def patch_yaml(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    new_yaml = """
regime_final_closure:
  enabled: true
  current_phase: 135
  final_phase: 160
  require_phase134_research_freeze: true
  research_freeze_ingestion_enabled: true
  artifact_chain_validation_enabled: true
  final_closure_validation_enabled: true
  freeze_seal_enabled: true
  final_safety_audit_enabled: true
  ml_input_contract_enabled: true
  ml_kickoff_gate_enabled: true
  write_final_closure_reports: true
  warn_not_investment_advice: true
  warn_phase135_is_not_activation: true
  warn_freeze_seal_is_not_deployment: true
  warn_ml_kickoff_does_not_train_models: true

phase135_closure_policy:
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

phase135_artifact_chain:
  enabled: true
  require_phase126_foundation: true
  require_phase127_feature_engineering: true
  require_phase128_labeling: true
  require_phase129_transition_analytics: true
  require_phase130_market_behavior: true
  require_phase131_alignment: true
  require_phase132_context_validation: true
  require_phase133_monitoring: true
  require_phase134_research_freeze: true
  require_hashes: true
  require_read_only_references: true

phase135_freeze_seal:
  enabled: true
  seal_version: "phase135.v1"
  sealed_phase_start: 126
  sealed_phase_end: 135
  next_phase: 136
  require_final_safety_audit_pass: true
  require_artifact_chain_valid: true

phase135_ml_kickoff:
  enabled: true
  ready_for_phase136_allowed: true
  build_input_contract: true
  training_started: false
  prediction_started: false
  allow_training_in_phase135: false
  allow_prediction_in_phase135: false
  require_non_activation_boundary: true

phase135_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""
    if "regime_final_closure:" not in content:
        content += new_yaml

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_yaml("config/default.yaml")
    patch_yaml("config/local.example.yaml")
