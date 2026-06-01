with open('usa_signal_bot/observability/metrics_collector.py', 'r') as f:
    content = f.read()

new_metrics = """

class Phase141Metrics:
    def __init__(self):
        self.metrics = {
            "latest_calibration_diagnostics_context_count": 0,
            "latest_calibration_candidate_count": 0,
            "latest_calibration_input_profile_count": 0,
            "latest_reliability_bin_count": 0,
            "latest_calibration_metric_count": 0,
            "latest_ece_value": 0.0,
            "latest_mce_value": 0.0,
            "latest_brier_score": 0.0,
            "latest_brier_decomposition_count": 0,
            "latest_score_distribution_diagnostic_count": 0,
            "latest_class_balance_diagnostic_count": 0,
            "latest_post_training_validation_pass_count": 0,
            "latest_calibration_governance_pass_count": 0,
            "latest_calibration_readiness_gate_pass_count": 0,
            "latest_phase141_live_inference_violation_count": 0,
            "latest_phase141_calibration_fitting_violation_count": 0,
            "latest_phase141_calibrated_model_violation_count": 0,
            "latest_phase141_threshold_optimization_violation_count": 0,
            "latest_phase141_execution_violation_count": 0,
            "latest_phase141_activation_violation_count": 0,
            "latest_phase141_deployment_violation_count": 0
        }
"""

if "Phase141Metrics" not in content:
    content += new_metrics

with open('usa_signal_bot/observability/metrics_collector.py', 'w') as f:
    f.write(content)

# Attempt to hook Phase141Metrics into MetricsCollector if possible
import re
with open('usa_signal_bot/observability/metrics_collector.py', 'r') as f:
    content = f.read()

match = re.search(r'(class MetricsCollector:.*?\n\s*def __init__\(self.*?\):.*?)(?=\n\s*def |\Z)', content, re.DOTALL)
if match:
    init_body = match.group(1)
    if "self.phase141" not in init_body:
        new_init = init_body + "        self.phase141 = Phase141Metrics()\n"
        content = content.replace(init_body, new_init)
        with open('usa_signal_bot/observability/metrics_collector.py', 'w') as f:
            f.write(content)
