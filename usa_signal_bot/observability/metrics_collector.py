from typing import Any, Dict

class MetricsCollector:
    def __init__(self):
        self.metrics = {}

    def record_diagnostic_metrics(self, summary: Dict[str, Any]):
        self.metrics["latest_diagnostic_status"] = summary.get("diagnostic_status", "UNKNOWN")
        self.metrics["latest_failure_mode_count"] = summary.get("failure_mode_count", 0)
        self.metrics["latest_high_severity_failure_count"] = summary.get("high_severity_failure_count", 0)
        self.metrics["latest_critical_failure_count"] = summary.get("critical_severity_count", 0)
        self.metrics["latest_failure_cluster_count"] = len(summary.get("top_failure_clusters", []))
        self.metrics["latest_degraded_strategy_count"] = summary.get("degraded_strategy_count", 0)
        self.metrics["latest_remediation_hint_count"] = summary.get("remediation_hint_count", 0)
        self.metrics["latest_noisy_evidence_count"] = summary.get("noisy_evidence_count", 0)
        self.metrics["diagnostics_warning_count"] = len(summary.get("warnings", []))

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics

# Global instance for easy import if needed
collector = MetricsCollector()
