"""Configuration management for USA Signal Bot."""

import yaml
from pathlib import Path
from dataclasses import asdict
from typing import Optional


from usa_signal_bot.core.config_schema import Config, RegimeMonitoringConfig, Phase133MonitoringPolicyConfig, Phase133DriftTrackingConfig, Phase133DegradationDiagnosticsConfig, Phase133NotificationsConfig as AppConfig, AdvancedFeaturesConfig, Phase118FeaturePolicyConfig, Phase118CrossSectionalConfig, Phase118FeatureTableConfig, Phase118NotificationsConfig, CoreRuntimeAcceptanceConfig, AdvancedFoundationFreezeConfig, DataProviderExpansionKickoffGateConfig, Phase105NotificationsConfig

from usa_signal_bot.core.exceptions import ConfigError
from usa_signal_bot.utils.dict_utils import deep_merge_dicts
from usa_signal_bot.core import paths

def validate_config(config: AppConfig) -> None:
    pass
def _load_yaml(file_path: Path) -> dict:
    """Loads a YAML file and returns its content as a dictionary."""
    if not file_path.exists():
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Error parsing YAML file {file_path}: {e}")

def load_app_config(config_dir: Optional[Path] = None) -> AppConfig:
    """
    Loads and merges the application configuration.
    It reads default.yaml and overrides it with local.yaml if present.
    """
    cfg_dir = config_dir or paths.CONFIG_DIR
    default_path = cfg_dir / "default.yaml"
    local_path = cfg_dir / "local.yaml"

    if not default_path.exists():
        raise ConfigError(f"Default configuration file not found at {default_path}")

    default_cfg = _load_yaml(default_path)
    local_cfg = _load_yaml(local_path)

    merged_cfg_dict = deep_merge_dicts(default_cfg, local_cfg)

    # Simple manual deserialization mapping nested dicts to dataclasses
    try:
        config = AppConfig()
        if 'regime_final_closure' in merged_cfg_dict:
            from usa_signal_bot.core.config_schema import RegimeFinalClosureConfig
            config.regime_final_closure = RegimeFinalClosureConfig(**merged_cfg_dict['regime_final_closure'])
        if 'phase135_closure_policy' in merged_cfg_dict:
            from usa_signal_bot.core.config_schema import Phase135ClosurePolicyConfig
            config.phase135_closure_policy = Phase135ClosurePolicyConfig(**merged_cfg_dict['phase135_closure_policy'])
        if 'phase135_artifact_chain' in merged_cfg_dict:
            from usa_signal_bot.core.config_schema import Phase135ArtifactChainConfig
            config.phase135_artifact_chain = Phase135ArtifactChainConfig(**merged_cfg_dict['phase135_artifact_chain'])
        if 'phase135_freeze_seal' in merged_cfg_dict:
            from usa_signal_bot.core.config_schema import Phase135FreezeSealConfig
            config.phase135_freeze_seal = Phase135FreezeSealConfig(**merged_cfg_dict['phase135_freeze_seal'])
        if 'phase135_ml_kickoff' in merged_cfg_dict:
            from usa_signal_bot.core.config_schema import Phase135MLKickoffConfig
            config.phase135_ml_kickoff = Phase135MLKickoffConfig(**merged_cfg_dict['phase135_ml_kickoff'])
        if 'phase135_notifications' in merged_cfg_dict:
            from usa_signal_bot.core.config_schema import Phase135NotificationsConfig
            config.phase135_notifications = Phase135NotificationsConfig(**merged_cfg_dict['phase135_notifications'])

        if "project" in merged_cfg_dict:
            for k, v in merged_cfg_dict["project"].items():
                setattr(config.project, k, v)

        if "runtime" in merged_cfg_dict:
            for k, v in merged_cfg_dict["runtime"].items():
                setattr(config.runtime, k, v)

        if "data" in merged_cfg_dict:
            for k, v in merged_cfg_dict["data"].items():
                setattr(config.data, k, v)

        if "logging" in merged_cfg_dict:
            for k, v in merged_cfg_dict["logging"].items():
                setattr(config.logging, k, v)

        if "telegram" in merged_cfg_dict:
            for k, v in merged_cfg_dict["telegram"].items():
                setattr(config.telegram, k, v)

        if "universe" in merged_cfg_dict:
            for k, v in merged_cfg_dict["universe"].items():
                setattr(config.universe, k, v)

        if "paper" in merged_cfg_dict:
            for k, v in merged_cfg_dict["paper"].items():
                setattr(config.paper, k, v)

        if "risk" in merged_cfg_dict:
            for k, v in merged_cfg_dict["risk"].items():
                setattr(config.risk, k, v)

        if "backtest" in merged_cfg_dict:
            for k, v in merged_cfg_dict["backtest"].items():
                setattr(config.backtest, k, v)

        if "optimization" in merged_cfg_dict:
            for k, v in merged_cfg_dict["optimization"].items():
                setattr(config.optimization, k, v)

        if "regime" in merged_cfg_dict:
            for k, v in merged_cfg_dict["regime"].items():
                setattr(config.regime, k, v)


        if "ml" in merged_cfg_dict:
            for k, v in merged_cfg_dict["ml"].items():
                setattr(config.ml, k, v)

        if "storage" in merged_cfg_dict:
            for k, v in merged_cfg_dict["storage"].items():
                setattr(config.storage, k, v)

        if "transaction_costs" in merged_cfg_dict:
            for k, v in merged_cfg_dict["transaction_costs"].items():
                setattr(config.transaction_costs, k, v)

        if "slippage" in merged_cfg_dict:
            for k, v in merged_cfg_dict["slippage"].items():
                setattr(config.slippage, k, v)

        if "trade_ledger" in merged_cfg_dict:
            for k, v in merged_cfg_dict["trade_ledger"].items():
                setattr(config.trade_ledger, k, v)

        if "advanced_backtest_metrics" in merged_cfg_dict:
            for k, v in merged_cfg_dict["advanced_backtest_metrics"].items():
                setattr(config.advanced_backtest_metrics, k, v)
        if "active_universe" in merged_cfg_dict:
            for k, v in merged_cfg_dict["active_universe"].items():
                setattr(config.active_universe, k, v)


        if "alert_policy" in merged_cfg_dict:
            for k, v in merged_cfg_dict["alert_policy"].items():
                setattr(config.alert_policy, k, v)

        if "alert_thresholds" in merged_cfg_dict:
            for k, v in merged_cfg_dict["alert_thresholds"].items():
                setattr(config.alert_thresholds, k, v)

        if "severity_routing" in merged_cfg_dict:
            for k, v in merged_cfg_dict["severity_routing"].items():
                setattr(config.severity_routing, k, v)

        if "alert_cooldown" in merged_cfg_dict:
            for k, v in merged_cfg_dict["alert_cooldown"].items():
                setattr(config.alert_cooldown, k, v)

        if "universe_readiness_gate" in merged_cfg_dict:
            for k, v in merged_cfg_dict["universe_readiness_gate"].items():
                setattr(config.universe_readiness_gate, k, v)

        if "universe_runs" in merged_cfg_dict:
            for k, v in merged_cfg_dict["universe_runs"].items():
                setattr(config.universe_runs, k, v)




        if "incident_response" in merged_cfg_dict:
            for k, v in merged_cfg_dict["incident_response"].items():
                setattr(config.incident_response, k, v)
        if "recovery" in merged_cfg_dict:
            for k, v in merged_cfg_dict["recovery"].items():
                setattr(config.recovery, k, v)
        if "rollback" in merged_cfg_dict:
            for k, v in merged_cfg_dict["rollback"].items():
                setattr(config.rollback, k, v)
        if "rollback_sources" in merged_cfg_dict:
            for k, v in merged_cfg_dict["rollback_sources"].items():
                setattr(config.rollback_sources, k, v)
        if "incident_audit" in merged_cfg_dict:
            for k, v in merged_cfg_dict["incident_audit"].items():
                setattr(config.incident_audit, k, v)
        if "taskqueue" in merged_cfg_dict:
            for k, v in merged_cfg_dict["taskqueue"].items():
                setattr(config.taskqueue, k, v)
        if "task_priority" in merged_cfg_dict:
            for k, v in merged_cfg_dict["task_priority"].items():
                setattr(config.task_priority, k, v)
        if "workload_budget" in merged_cfg_dict:
            for k, v in merged_cfg_dict["workload_budget"].items():
                setattr(config.workload_budget, k, v)
        if "run_windows" in merged_cfg_dict:
            for k, v in merged_cfg_dict["run_windows"].items():
                setattr(config.run_windows, k, v)
        if "task_conflicts" in merged_cfg_dict:
            for k, v in merged_cfg_dict["task_conflicts"].items():
                setattr(config.task_conflicts, k, v)
        if "queue_executor" in merged_cfg_dict:
            for k, v in merged_cfg_dict["queue_executor"].items():
                setattr(config.queue_executor, k, v)
        if "taskqueue_notifications" in merged_cfg_dict:
            for k, v in merged_cfg_dict["taskqueue_notifications"].items():
                setattr(config.taskqueue_notifications, k, v)
        if "incident_notifications" in merged_cfg_dict:
            for k, v in merged_cfg_dict["incident_notifications"].items():
                setattr(config.incident_notifications, k, v)

        validate_config(config)

        if "basket_simulation" in merged_cfg_dict:
            config.basket_simulation = BasketSimulationConfigSchema(**merged_cfg_dict["basket_simulation"])
        else:
            pass

        if "allocation_replay" in merged_cfg_dict:
            config.allocation_replay = AllocationReplayConfig(**merged_cfg_dict["allocation_replay"])
        else:
            pass

        if "allocation_drift" in merged_cfg_dict:
            config.allocation_drift = AllocationDriftConfigSchema(**merged_cfg_dict["allocation_drift"])
        else:
            pass

        from usa_signal_bot.core.config_schema import RuntimeLifecycleConfig, Phase104StartupChecksConfig, Phase104ReadinessGateConfig, Phase104NotificationsConfig, CoreRuntimeAcceptanceConfig, AdvancedFoundationFreezeConfig, DataProviderExpansionKickoffGateConfig, Phase105NotificationsConfig
        config.runtime_lifecycle = RuntimeLifecycleConfig(**merged_cfg_dict.get('runtime_lifecycle', {}))
        config.phase104_startup_checks = Phase104StartupChecksConfig(**merged_cfg_dict.get('phase104_startup_checks', {}))
        config.phase104_readiness_gate = Phase104ReadinessGateConfig(**merged_cfg_dict.get('phase104_readiness_gate', {}))
        config.phase104_notifications = Phase104NotificationsConfig(**merged_cfg_dict.get('phase104_notifications', {}))
        from usa_signal_bot.core.config_schema import RuntimeLifecycleConfig, Phase104StartupChecksConfig, Phase104ReadinessGateConfig, Phase104NotificationsConfig, CoreRuntimeAcceptanceConfig, AdvancedFoundationFreezeConfig, DataProviderExpansionKickoffGateConfig, Phase105NotificationsConfig
        config.runtime_lifecycle = RuntimeLifecycleConfig(**merged_cfg_dict.get('runtime_lifecycle', {}))
        config.phase104_startup_checks = Phase104StartupChecksConfig(**merged_cfg_dict.get('phase104_startup_checks', {}))
        config.phase104_readiness_gate = Phase104ReadinessGateConfig(**merged_cfg_dict.get('phase104_readiness_gate', {}))
        config.phase104_notifications = Phase104NotificationsConfig(**merged_cfg_dict.get('phase104_notifications', {}))



        if 'core_runtime_acceptance' in merged_cfg_dict:
            config.core_runtime_acceptance = CoreRuntimeAcceptanceConfig(**merged_cfg_dict['core_runtime_acceptance'])
        if 'advanced_foundation_freeze' in merged_cfg_dict:
            config.advanced_foundation_freeze = AdvancedFoundationFreezeConfig(**merged_cfg_dict['advanced_foundation_freeze'])
        if 'data_provider_expansion_kickoff_gate' in merged_cfg_dict:
            config.data_provider_expansion_kickoff_gate = DataProviderExpansionKickoffGateConfig(**merged_cfg_dict['data_provider_expansion_kickoff_gate'])
        if 'phase105_notifications' in merged_cfg_dict:
            config.phase105_notifications = Phase105NotificationsConfig(**merged_cfg_dict['phase105_notifications'])


        if "advanced_features" in merged_cfg_dict:
            af_dict = merged_cfg_dict.get("advanced_features", {})
            config.advanced_features = AdvancedFeaturesConfig(
                enabled=af_dict.get("enabled", True),
                current_phase=af_dict.get("current_phase", 118),
                final_phase=af_dict.get("final_phase", 160),
                require_phase117_core_indicators=af_dict.get("require_phase117_core_indicators", True),
                advanced_volatility_enabled=af_dict.get("advanced_volatility_enabled", True),
                advanced_momentum_enabled=af_dict.get("advanced_momentum_enabled", True),
                advanced_trend_enabled=af_dict.get("advanced_trend_enabled", True),
                normalization_enabled=af_dict.get("normalization_enabled", True),
                cross_sectional_enabled=af_dict.get("cross_sectional_enabled", True),
                multi_symbol_feature_table_enabled=af_dict.get("multi_symbol_feature_table_enabled", True),
                write_advanced_feature_reports=af_dict.get("write_advanced_feature_reports", True),
                warn_not_investment_advice=af_dict.get("warn_not_investment_advice", True),
                warn_phase118_is_not_activation=af_dict.get("warn_phase118_is_not_activation", True),
                warn_advanced_features_are_not_trade_signals=af_dict.get("warn_advanced_features_are_not_trade_signals", True),
            )
        if "phase118_feature_policy" in merged_cfg_dict:
             pd = merged_cfg_dict.get("phase118_feature_policy", {})
             config.advanced_features.policy = Phase118FeaturePolicyConfig(
                 compute_values_local_only=pd.get("compute_values_local_only", True),
                 research_data_only=pd.get("research_data_only", True),
                 local_fixture_only_default=pd.get("local_fixture_only_default", True),
                 allow_network=pd.get("allow_network", False),
                 allow_paid_api=pd.get("allow_paid_api", False),
                 allow_scraping=pd.get("allow_scraping", False),
                 allow_html_parsing=pd.get("allow_html_parsing", False),
                 allow_broker=pd.get("allow_broker", False),
                 allow_order=pd.get("allow_order", False),
                 allow_paper_mutation=pd.get("allow_paper_mutation", False),
                 allow_telegram_real_send=pd.get("allow_telegram_real_send", False),
                 allow_dashboard=pd.get("allow_dashboard", False),
                 produce_trade_signals=pd.get("produce_trade_signals", False),
                 produce_order_decisions=pd.get("produce_order_decisions", False),
                 produce_portfolio_weights=pd.get("produce_portfolio_weights", False),
                 strategy_activation_allowed=pd.get("strategy_activation_allowed", False),
             )
        if "phase118_cross_sectional" in merged_cfg_dict:
             cd = merged_cfg_dict.get("phase118_cross_sectional", {})
             config.advanced_features.cross_sectional = Phase118CrossSectionalConfig(
                 enabled=cd.get("enabled", True),
                 min_required_symbols=cd.get("min_required_symbols", 2),
                 default_benchmark_symbol=cd.get("default_benchmark_symbol", "SPY"),
                 align_on_common_timestamps=cd.get("align_on_common_timestamps", True),
                 produce_portfolio_weights=cd.get("produce_portfolio_weights", False),
                 produce_trade_signals=cd.get("produce_trade_signals", False),
                 produce_order_decisions=cd.get("produce_order_decisions", False),
             )
        if "phase118_feature_table" in merged_cfg_dict:
             fd = merged_cfg_dict.get("phase118_feature_table", {})
             config.advanced_features.feature_table = Phase118FeatureTableConfig(
                 preserve_core_feature_columns=fd.get("preserve_core_feature_columns", True),
                 preserve_warmup_nulls=fd.get("preserve_warmup_nulls", True),
                 block_forbidden_columns=fd.get("block_forbidden_columns", True),
                 allow_macd_signal_line_column=fd.get("allow_macd_signal_line_column", True),
                 write_feature_tables=fd.get("write_feature_tables", True),
                 overwrite_feature_tables_default=fd.get("overwrite_feature_tables_default", False),
             )
        if "phase118_notifications" in merged_cfg_dict:
             nd = merged_cfg_dict.get("phase118_notifications", {})
             config.advanced_features.notifications = Phase118NotificationsConfig(
                 enabled=nd.get("enabled", True),
                 dry_run=nd.get("dry_run", True),
                 preview_only=nd.get("preview_only", True),
                 telegram_real_send=nd.get("telegram_real_send", False),
             )

        if "regime_monitoring" in merged_cfg_dict:
            config.regime_monitoring = RegimeMonitoringConfig(**merged_cfg_dict["regime_monitoring"])
        if "phase133_monitoring_policy" in merged_cfg_dict:
            config.phase133_monitoring_policy = Phase133MonitoringPolicyConfig(**merged_cfg_dict["phase133_monitoring_policy"])
        if "phase133_drift_tracking" in merged_cfg_dict:
            config.phase133_drift_tracking = Phase133DriftTrackingConfig(**merged_cfg_dict["phase133_drift_tracking"])
        if "phase133_degradation_diagnostics" in merged_cfg_dict:
            config.phase133_degradation_diagnostics = Phase133DegradationDiagnosticsConfig(**merged_cfg_dict["phase133_degradation_diagnostics"])
        if "phase133_notifications" in merged_cfg_dict:
            config.phase133_notifications = Phase133NotificationsConfig(**merged_cfg_dict["phase133_notifications"])

        return config

    except Exception as e:
        if isinstance(e, ConfigError):
            raise
        raise ConfigError(f"Error mapping configuration to schema: {e}")

def config_to_dict(config: AppConfig) -> dict:
    """Converts the active configuration back to a dictionary."""
    return asdict(config)


def load_paper_mode_dry_admission_gate_config(data: dict):
    d = data.get("paper_mode_dry_admission_gate", {})
    return PaperModeDryAdmissionGateConfig(
        enabled=d.get("enabled", True),
        write_dry_admission_reports=d.get("write_dry_admission_reports", True),
        warn_not_investment_advice=d.get("warn_not_investment_advice", True),
        warn_no_broker_execution=d.get("warn_no_broker_execution", True),
        warn_no_real_paper_mutation=d.get("warn_no_real_paper_mutation", True),
        warn_shadow_replay_is_metadata_only=d.get("warn_shadow_replay_is_metadata_only", True),
        warn_board_evidence_freeze_is_metadata_only=d.get("warn_board_evidence_freeze_is_metadata_only", True),
        warn_dry_admission_gate_is_not_activation=d.get("warn_dry_admission_gate_is_not_activation", True)
    )

def load_shadow_launch_blocker_replay_config(data: dict):
    d = data.get("shadow_launch_blocker_replay", {})
    return ShadowLaunchBlockerReplayConfig(
        enabled=d.get("enabled", True),
        deterministic_replay=d.get("deterministic_replay", True),
        require_all_attempts_blocked=d.get("require_all_attempts_blocked", True),
        require_shadow_launch_blocker_events=d.get("require_shadow_launch_blocker_events", True),
        execution_enabled=d.get("execution_enabled", False),
        shadow_launch_enabled=d.get("shadow_launch_enabled", False),
        paper_mode_launch_enabled=d.get("paper_mode_launch_enabled", False),
        active_paper_enabled=d.get("active_paper_enabled", False),
        paper_admission_enabled=d.get("paper_admission_enabled", False),
        broker_execution_enabled=d.get("broker_execution_enabled", False),
        paper_state_mutation_enabled=d.get("paper_state_mutation_enabled", False),
        config_patch_enabled=d.get("config_patch_enabled", False),
        telegram_real_send_enabled=d.get("telegram_real_send_enabled", False)
    )

def load_board_evidence_freeze_config(data: dict):
    d = data.get("board_evidence_freeze", {})
    return BoardEvidenceFreezeConfig(
        enabled=d.get("enabled", True),
        freeze_is_metadata_only=d.get("freeze_is_metadata_only", True),
        require_frozen=d.get("require_frozen", True),
        require_immutable=d.get("require_immutable", True),
        require_evidence_available=d.get("require_evidence_available", True),
        block_on_missing_evidence=d.get("block_on_missing_evidence", True),
        block_on_stale_evidence=d.get("block_on_stale_evidence", True),
        block_on_freeze_failed=d.get("block_on_freeze_failed", True)
    )

def load_final_paper_mode_dry_admission_gate_config(data: dict):
    d = data.get("final_paper_mode_dry_admission_gate", {})
    return FinalPaperModeDryAdmissionGateConfig(
        enabled=d.get("enabled", True),
        gate_is_metadata_only=d.get("gate_is_metadata_only", True),
        require_board_dossier=d.get("require_board_dossier", True),
        require_acceptance_board_seal=d.get("require_acceptance_board_seal", True),
        require_shadow_replay=d.get("require_shadow_replay", True),
        require_board_evidence_freeze=d.get("require_board_evidence_freeze", True),
        require_dry_admission_rules=d.get("require_dry_admission_rules", True),
        require_dry_admission_assertions=d.get("require_dry_admission_assertions", True),
        require_manual_review=d.get("require_manual_review", True),
        activation_allowed=d.get("activation_allowed", False),
        admission_allowed=d.get("admission_allowed", False),
        transition_allowed=d.get("transition_allowed", False),
        shadow_launch_allowed=d.get("shadow_launch_allowed", False),
        paper_mode_launch_allowed=d.get("paper_mode_launch_allowed", False),
        all_writes_blocked_required=d.get("all_writes_blocked_required", True),
        require_order_created_false=d.get("require_order_created_false", True),
        require_mutation_detected_false=d.get("require_mutation_detected_false", True),
        allow_active_paper=d.get("allow_active_paper", False),
        allow_broker_execution=d.get("allow_broker_execution", False),
        allow_paper_state_mutation=d.get("allow_paper_state_mutation", False),
        allow_config_patch=d.get("allow_config_patch", False),
        allow_telegram_real_send=d.get("allow_telegram_real_send", False)
    )

def load_dry_admission_gate_safety_config(data: dict):
    d = data.get("dry_admission_gate_safety", {})
    return DryAdmissionGateSafetyConfig(
        enabled=d.get("enabled", True),
        block_on_real_order_risk=d.get("block_on_real_order_risk", True),
        block_on_paper_order_risk=d.get("block_on_paper_order_risk", True),
        block_on_broker_order_risk=d.get("block_on_broker_order_risk", True),
        block_on_paper_state_mutation_risk=d.get("block_on_paper_state_mutation_risk", True),
        block_on_telegram_real_send_risk=d.get("block_on_telegram_real_send_risk", True),
        block_on_production_config_write_risk=d.get("block_on_production_config_write_risk", True),
        block_on_active_paper_enable_risk=d.get("block_on_active_paper_enable_risk", True),
        block_on_shadow_launch_risk=d.get("block_on_shadow_launch_risk", True),
        block_on_paper_mode_launch_risk=d.get("block_on_paper_mode_launch_risk", True),
        block_on_admission_allowed_risk=d.get("block_on_admission_allowed_risk", True),
        block_on_activation_allowed_risk=d.get("block_on_activation_allowed_risk", True),
        block_on_transition_allowed_risk=d.get("block_on_transition_allowed_risk", True),
        block_on_order_created_risk=d.get("block_on_order_created_risk", True),
        block_on_mutation_detected_risk=d.get("block_on_mutation_detected_risk", True),
        block_on_shadow_replay_failed=d.get("block_on_shadow_replay_failed", True),
        block_on_board_evidence_freeze_failed=d.get("block_on_board_evidence_freeze_failed", True),
        block_on_dry_admission_assertion_failed=d.get("block_on_dry_admission_assertion_failed", True),
        block_on_secret_risk=d.get("block_on_secret_risk", True)
    )

def load_dry_admission_gate_notifications_config(data: dict):
    d = data.get("dry_admission_gate_notifications", {})
    return DryAdmissionGateNotificationsConfig(
        enabled=d.get("enabled", True),
        dry_run=d.get("dry_run", True),
        notify_dry_admission_gate_report=d.get("notify_dry_admission_gate_report", True),
        notify_shadow_replay_warning=d.get("notify_shadow_replay_warning", True),
        notify_board_evidence_freeze_warning=d.get("notify_board_evidence_freeze_warning", True),
        default_channel=d.get("default_channel", "dry_run"),
        warn_no_real_send_default=d.get("warn_no_real_send_default", True)
    )

# add parsing to `config.py` near other configurations
# using sed
