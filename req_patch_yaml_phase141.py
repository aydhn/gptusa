new_yaml = """

calibration_diagnostics:
  enabled: true
  current_phase: 141
  final_phase: 160
  require_phase140_model_comparison: true
  model_comparison_ingestion_enabled: true
  comparison_artifact_loader_enabled: true
  calibration_input_resolver_enabled: true
  reliability_binning_enabled: true
  calibration_metric_enabled: true
  brier_decomposition_enabled: true
  score_distribution_enabled: true
  class_balance_enabled: true
  post_training_validation_enabled: true
  calibration_governance_enabled: true
  model_card_update_enabled: true
  readiness_gate_enabled: true
  write_calibration_diagnostics_reports: true
  warn_not_investment_advice: true
  warn_diagnostics_are_not_trade_signals: true
  warn_phase141_does_not_fit_calibrators: true
  warn_phase141_does_not_create_calibrated_models: true

phase141_calibration_policy:
  compute_values_local_only: true
  research_data_only: true
  offline_ml_research_only: true
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
  allow_live_inference: false
  allow_online_inference: false
  allow_calibration_fitting: false
  allow_calibrated_model_creation: false
  allow_threshold_optimization: false
  allow_heavy_ml_dependencies: false
  allow_background_daemon: false
  allow_scheduler: false
  produce_trade_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false
  produce_investment_advice: false
  strategy_activation_allowed: false

phase141_reliability:
  enabled: true
  default_bin_count: 10
  default_bin_strategy: FIXED_10_BIN
  require_ece: true
  require_mce: true
  require_brier_score: true
  require_brier_decomposition: true
  require_score_distribution: true
  require_class_balance: true
  probability_missing_allowed_with_warning: true

phase141_post_training_validation:
  enabled: true
  require_model_registry_consistency: true
  require_candidate_shortlist_consistency: true
  require_offline_predictions_available: true
  require_no_forbidden_output_fields: true
  require_no_live_inference: true
  require_no_calibration_fitting: true
  require_no_deployment: true

phase141_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""

for filepath in ['config/default.yaml', 'config/local.example.yaml']:
    with open(filepath, 'r') as f:
        content = f.read()
    if "calibration_diagnostics:" not in content:
        with open(filepath, 'a') as f:
            f.write(new_yaml)
