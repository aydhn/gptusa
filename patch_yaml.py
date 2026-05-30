import re

with open("config/default.yaml", "r") as f:
    yaml_content = f.read()

phase133_yaml = """
regime_monitoring:
  enabled: true
  current_phase: 133
  final_phase: 160
  require_phase132_context_validation: true
  context_validation_artifact_loader_enabled: true
  baseline_builder_enabled: true
  snapshot_builder_enabled: true
  drift_tracking_enabled: true
  degradation_diagnostics_enabled: true
  readiness_gate_enabled: true
  write_regime_monitoring_reports: true
  warn_not_investment_advice: true
  warn_phase133_is_not_activation: true
  warn_monitoring_is_not_live_daemon: true
  warn_drift_is_not_trade_signal: true

phase133_monitoring_policy:
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

phase133_drift_tracking:
  enabled: true
  baseline_version: "phase133.v1"
  warning_threshold_default: 10.0
  blocking_threshold_default: 25.0
  require_baseline_hash: true
  require_snapshot_hash: true
  ready_for_phase134_allowed: true

phase133_degradation_diagnostics:
  enabled: true
  allowed_recommended_action_types:
    - research_review
    - data_quality_review
    - documentation_review
    - monitor_context
    - baseline_refresh_review
  block_execution_action_types: true

phase133_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""

if "regime_monitoring:" not in yaml_content:
    with open("config/default.yaml", "a") as f:
        f.write("\n" + phase133_yaml)
    with open("config/local.example.yaml", "a") as f:
        f.write("\n" + phase133_yaml)

with open("usa_signal_bot/core/config_schema.py", "r") as f:
    schema = f.read()

new_schema = """

@dataclass
class RegimeMonitoringConfig:
    enabled: bool = True
    current_phase: int = 133
    final_phase: int = 160
    require_phase132_context_validation: bool = True
    context_validation_artifact_loader_enabled: bool = True
    baseline_builder_enabled: bool = True
    snapshot_builder_enabled: bool = True
    drift_tracking_enabled: bool = True
    degradation_diagnostics_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_regime_monitoring_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase133_is_not_activation: bool = True
    warn_monitoring_is_not_live_daemon: bool = True
    warn_drift_is_not_trade_signal: bool = True

@dataclass
class Phase133MonitoringPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
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
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase133DriftTrackingConfig:
    enabled: bool = True
    baseline_version: str = "phase133.v1"
    warning_threshold_default: float = 10.0
    blocking_threshold_default: float = 25.0
    require_baseline_hash: bool = True
    require_snapshot_hash: bool = True
    ready_for_phase134_allowed: bool = True

@dataclass
class Phase133DegradationDiagnosticsConfig:
    enabled: bool = True
    allowed_recommended_action_types: List[str] = field(default_factory=lambda: ["research_review", "data_quality_review", "documentation_review", "monitor_context", "baseline_refresh_review"])
    block_execution_action_types: bool = True

@dataclass
class Phase133NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
"""

if "RegimeMonitoringConfig" not in schema:
    schema = schema.replace("class Config:", new_schema + "\n@dataclass\nclass Config:")
    schema = schema.replace("    phase132_notifications: Phase132NotificationsConfig = field(default_factory=Phase132NotificationsConfig)",
                            "    phase132_notifications: Phase132NotificationsConfig = field(default_factory=Phase132NotificationsConfig)\n    regime_monitoring: RegimeMonitoringConfig = field(default_factory=RegimeMonitoringConfig)\n    phase133_monitoring_policy: Phase133MonitoringPolicyConfig = field(default_factory=Phase133MonitoringPolicyConfig)\n    phase133_drift_tracking: Phase133DriftTrackingConfig = field(default_factory=Phase133DriftTrackingConfig)\n    phase133_degradation_diagnostics: Phase133DegradationDiagnosticsConfig = field(default_factory=Phase133DegradationDiagnosticsConfig)\n    phase133_notifications: Phase133NotificationsConfig = field(default_factory=Phase133NotificationsConfig)")

    with open("usa_signal_bot/core/config_schema.py", "w") as f:
        f.write(schema)


with open("usa_signal_bot/core/config.py", "r") as f:
    config_py = f.read()

if "regime_monitoring=RegimeMonitoringConfig(**cfg" not in config_py:
    new_parsing = """            regime_monitoring=RegimeMonitoringConfig(**cfg.get("regime_monitoring", {})),
            phase133_monitoring_policy=Phase133MonitoringPolicyConfig(**cfg.get("phase133_monitoring_policy", {})),
            phase133_drift_tracking=Phase133DriftTrackingConfig(**cfg.get("phase133_drift_tracking", {})),
            phase133_degradation_diagnostics=Phase133DegradationDiagnosticsConfig(**cfg.get("phase133_degradation_diagnostics", {})),
            phase133_notifications=Phase133NotificationsConfig(**cfg.get("phase133_notifications", {})),"""

    config_py = config_py.replace("phase132_notifications=Phase132NotificationsConfig(**cfg.get(\"phase132_notifications\", {})),", "phase132_notifications=Phase132NotificationsConfig(**cfg.get(\"phase132_notifications\", {})),\n" + new_parsing)

    with open("usa_signal_bot/core/config.py", "w") as f:
        f.write(config_py)
