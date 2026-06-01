with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

new_configs = """

@dataclass
class Phase141CalibrationPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_inference: bool = False
    allow_online_inference: bool = False
    allow_calibration_fitting: bool = False
    allow_calibrated_model_creation: bool = False
    allow_threshold_optimization: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase141ReliabilityConfig:
    enabled: bool = True
    default_bin_count: int = 10
    default_bin_strategy: str = "FIXED_10_BIN"
    require_ece: bool = True
    require_mce: bool = True
    require_brier_score: bool = True
    require_brier_decomposition: bool = True
    require_score_distribution: bool = True
    require_class_balance: bool = True
    probability_missing_allowed_with_warning: bool = True

@dataclass
class Phase141PostTrainingValidationConfig:
    enabled: bool = True
    require_model_registry_consistency: bool = True
    require_candidate_shortlist_consistency: bool = True
    require_offline_predictions_available: bool = True
    require_no_forbidden_output_fields: bool = True
    require_no_live_inference: bool = True
    require_no_calibration_fitting: bool = True
    require_no_deployment: bool = True

@dataclass
class Phase141NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class CalibrationDiagnosticsConfig:
    enabled: bool = True
    current_phase: int = 141
    final_phase: int = 160
    require_phase140_model_comparison: bool = True
    model_comparison_ingestion_enabled: bool = True
    comparison_artifact_loader_enabled: bool = True
    calibration_input_resolver_enabled: bool = True
    reliability_binning_enabled: bool = True
    calibration_metric_enabled: bool = True
    brier_decomposition_enabled: bool = True
    score_distribution_enabled: bool = True
    class_balance_enabled: bool = True
    post_training_validation_enabled: bool = True
    calibration_governance_enabled: bool = True
    model_card_update_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_calibration_diagnostics_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_diagnostics_are_not_trade_signals: bool = True
    warn_phase141_does_not_fit_calibrators: bool = True
    warn_phase141_does_not_create_calibrated_models: bool = True
    phase141_calibration_policy: Phase141CalibrationPolicyConfig = field(default_factory=Phase141CalibrationPolicyConfig)
    phase141_reliability: Phase141ReliabilityConfig = field(default_factory=Phase141ReliabilityConfig)
    phase141_post_training_validation: Phase141PostTrainingValidationConfig = field(default_factory=Phase141PostTrainingValidationConfig)
    phase141_notifications: Phase141NotificationsConfig = field(default_factory=Phase141NotificationsConfig)
"""

if "CalibrationDiagnosticsConfig" not in content:
    content += new_configs

    # We also need to add calibration_diagnostics to AppConfig
    # Find AppConfig
    import re
    app_config_match = re.search(r'class AppConfig:.*?\n(.*?)\n\n', content, re.DOTALL)
    if app_config_match:
        pass

    # Let's just append it to the end of the file since it's probably easier
    # to add it to AppConfig manually if we need to. Let's see if AppConfig has it.

    if "calibration_diagnostics:" not in content:
        content = re.sub(r'(class AppConfig:\n.*?)(\s*@classmethod)', r'\1    calibration_diagnostics: CalibrationDiagnosticsConfig = field(default_factory=CalibrationDiagnosticsConfig)\n\2', content, flags=re.DOTALL)


with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.write(content)
