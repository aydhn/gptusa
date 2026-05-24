import re

with open("usa_signal_bot/observability/metrics_collector.py", "r") as f:
    content = f.read()

new_metrics = """
            "latest_runtime_registry_count": 0,
            "latest_runtime_registry_valid_count": 0,
            "latest_config_surface_record_count": 0,
            "latest_config_surface_conflict_count": 0,
            "latest_provider_capability_manifest_count": 0,
            "latest_provider_safety_manifest_count": 0,
            "latest_provider_safety_violation_count": 0,
            "latest_runtime_capability_policy_count": 0,
            "latest_phase102_execution_violation_count": 0,
"""

new_update_func = """
    def update_phase102_advanced_runtime_metrics(self, payload: dict):
        self.metrics["latest_runtime_registry_count"] = self.metrics.get("latest_runtime_registry_count", 0) + 1
        self.metrics["latest_runtime_registry_valid_count"] = self.metrics.get("latest_runtime_registry_valid_count", 0) + payload.get("valid_registry_count", 0)
        self.metrics["latest_config_surface_record_count"] = self.metrics.get("latest_config_surface_record_count", 0) + payload.get("config_surface_record_count", 0)
        self.metrics["latest_config_surface_conflict_count"] = self.metrics.get("latest_config_surface_conflict_count", 0) + payload.get("config_surface_conflict_count", 0)
        self.metrics["latest_provider_capability_manifest_count"] = self.metrics.get("latest_provider_capability_manifest_count", 0) + payload.get("provider_capability_manifest_count", 0)
        self.metrics["latest_provider_safety_manifest_count"] = self.metrics.get("latest_provider_safety_manifest_count", 0) + payload.get("provider_safety_manifest_count", 0)
        self.metrics["latest_provider_safety_violation_count"] = self.metrics.get("latest_provider_safety_violation_count", 0) + payload.get("provider_safety_violation_count", 0)
        self.metrics["latest_runtime_capability_policy_count"] = self.metrics.get("latest_runtime_capability_policy_count", 0) + payload.get("runtime_capability_policy_count", 0)
        self.metrics["latest_phase102_execution_violation_count"] = self.metrics.get("latest_phase102_execution_violation_count", 0) + payload.get("execution_violation_count", 0)
"""

if "latest_runtime_registry_count" not in content:
    content = content.replace("            \"board_dossier_warning_count\": 0\n        }", "            \"board_dossier_warning_count\": 0,\n" + new_metrics + "\n        }")
    content = content + "\n" + new_update_func + "\n"
    with open("usa_signal_bot/observability/metrics_collector.py", "w") as f:
        f.write(content)
