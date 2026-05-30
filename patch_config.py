import re

with open("usa_signal_bot/core/config.py", "r") as f:
    content = f.read()

# Make sure imports are there
if "RegimeMonitoringConfig" not in content:
    content = content.replace("from usa_signal_bot.core.config_schema import Config", "from usa_signal_bot.core.config_schema import Config, RegimeMonitoringConfig, Phase133MonitoringPolicyConfig, Phase133DriftTrackingConfig, Phase133DegradationDiagnosticsConfig, Phase133NotificationsConfig")

# Find the end of config instantiation
if "config.regime_monitoring" not in content:
    patch = """
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
"""
    content = content.replace("        return config", patch + "\n        return config")

with open("usa_signal_bot/core/config.py", "w") as f:
    f.write(content)
