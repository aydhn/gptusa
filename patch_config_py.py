with open("usa_signal_bot/core/config.py", "r") as f:
    config_py = f.read()

if "regime_monitoring=RegimeMonitoringConfig(**cfg" not in config_py:
    new_parsing = """            regime_monitoring=RegimeMonitoringConfig(**cfg.get("regime_monitoring", {})),
            phase133_monitoring_policy=Phase133MonitoringPolicyConfig(**cfg.get("phase133_monitoring_policy", {})),
            phase133_drift_tracking=Phase133DriftTrackingConfig(**cfg.get("phase133_drift_tracking", {})),
            phase133_degradation_diagnostics=Phase133DegradationDiagnosticsConfig(**cfg.get("phase133_degradation_diagnostics", {})),
            phase133_notifications=Phase133NotificationsConfig(**cfg.get("phase133_notifications", {})),"""

    config_py = config_py.replace("phase132_notifications=Phase132NotificationsConfig(**cfg.get(\"phase132_notifications\", {}))", "phase132_notifications=Phase132NotificationsConfig(**cfg.get(\"phase132_notifications\", {})),\n" + new_parsing)

    with open("usa_signal_bot/core/config.py", "w") as f:
        f.write(config_py)
