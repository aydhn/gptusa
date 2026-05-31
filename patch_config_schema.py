import re

file_path = "usa_signal_bot/core/config_schema.py"

with open(file_path, "r") as f:
    content = f.read()

new_config_schema = """
@dataclass
class RegimeResearchFreezeConfig:
    enabled: bool = True
    current_phase: int = 134
    final_phase: int = 160
    require_phase133_regime_monitoring: bool = True
    monitoring_artifact_loader_enabled: bool = True
    monitoring_validation_enabled: bool = True
    drift_report_enabled: bool = True
    drift_report_qa_enabled: bool = True
    freeze_package_enabled: bool = True
    freeze_readiness_gate_enabled: bool = True
    write_research_freeze_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase134_is_not_activation: bool = True
    warn_freeze_package_is_not_deployment: bool = True

@dataclass
class Phase134FreezePolicyConfig:
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
class Phase134DriftReportQaConfig:
    enabled: bool = True
    require_qa_pass: bool = True
    block_investment_advice_language: bool = True
    block_trade_signal_language: bool = True
    block_order_decision_language: bool = True
    block_portfolio_allocation_language: bool = True
    block_guarantee_language: bool = True
    block_broker_execution_language: bool = True
    block_deployment_language: bool = True
    block_live_monitoring_language: bool = True
    overwrite_reports_default: bool = False

@dataclass
class Phase134FreezePackageConfig:
    enabled: bool = True
    package_version: str = "phase134.v1"
    require_required_artifact_coverage: bool = True
    require_package_hash: bool = True
    require_manifest_hash: bool = True
    ready_for_phase135_allowed: bool = True

@dataclass
class Phase134NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
"""

if "RegimeResearchFreezeConfig" not in content:
    # Add after FeatureFactorClosureConfig or similar
    content = content.replace(
        "class FeatureFactorClosureConfig:",
        new_config_schema + "\n@dataclass\nclass FeatureFactorClosureConfig:"
    )

    # In AppConfig add fields
    if "regime_research_freeze" not in content:
        content = content.replace(
            "    feature_factor_closure: FeatureFactorClosureConfig = field(default_factory=FeatureFactorClosureConfig)",
            "    feature_factor_closure: FeatureFactorClosureConfig = field(default_factory=FeatureFactorClosureConfig)\n    regime_research_freeze: RegimeResearchFreezeConfig = field(default_factory=RegimeResearchFreezeConfig)\n    phase134_freeze_policy: Phase134FreezePolicyConfig = field(default_factory=Phase134FreezePolicyConfig)\n    phase134_drift_report_qa: Phase134DriftReportQaConfig = field(default_factory=Phase134DriftReportQaConfig)\n    phase134_freeze_package: Phase134FreezePackageConfig = field(default_factory=Phase134FreezePackageConfig)\n    phase134_notifications: Phase134NotificationsConfig = field(default_factory=Phase134NotificationsConfig)"
        )

with open(file_path, "w") as f:
    f.write(content)
