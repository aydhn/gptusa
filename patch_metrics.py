import re

with open("usa_signal_bot/observability/metrics_collector.py", "r") as f:
    content = f.read()

# Insert new metrics into __init__
metrics_patch = """
        self.metrics["latest_final_closure_context_count"] = 0
        self.metrics["latest_final_closure_artifact_count"] = 0
        self.metrics["latest_final_closure_manifest_count"] = 0
        self.metrics["latest_freeze_seal_count"] = 0
        self.metrics["latest_engine_certificate_count"] = 0
        self.metrics["latest_phase126_kickoff_gate_count"] = 0
        self.metrics["latest_final_closure_pass_count"] = 0
        self.metrics["latest_feature_factor_engine_final_closed_count"] = 0
        self.metrics["latest_phase126_ready_count"] = 0
        self.metrics["latest_final_closure_safety_violation_count"] = 0
        self.metrics["latest_phase125_execution_violation_count"] = 0
        self.metrics["latest_phase125_deployment_violation_count"] = 0
"""

content = re.sub(
    r'(self\.metrics\["latest_phase119_execution_violation_count"\] = 0)',
    r'\1\n' + metrics_patch,
    content
)

with open("usa_signal_bot/observability/metrics_collector.py", "w") as f:
    f.write(content)
