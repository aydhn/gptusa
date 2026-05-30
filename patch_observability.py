import re

file_path = "usa_signal_bot/observability/metrics_collector.py"

try:
    with open(file_path, "r") as f:
        content = f.read()

    new_metrics = """
        latest_research_freeze_context_count: int = 0
        latest_monitoring_validation_result_count: int = 0
        latest_drift_report_document_count: int = 0
        latest_drift_report_qa_pass_count: int = 0
        latest_drift_report_qa_warning_count: int = 0
        latest_research_freeze_package_count: int = 0
        latest_research_freeze_artifact_reference_count: int = 0
        latest_research_freeze_readiness_gate_pass_count: int = 0
        latest_research_freeze_missing_required_artifact_count: int = 0
        latest_phase134_model_training_violation_count: int = 0
        latest_phase134_model_prediction_violation_count: int = 0
        latest_phase134_execution_violation_count: int = 0
        latest_phase134_activation_violation_count: int = 0
        latest_phase134_daemon_violation_count: int = 0
"""

    if "latest_research_freeze_context_count" not in content:
        if "class SystemMetrics:" in content:
            content = content.replace("class SystemMetrics:", "class SystemMetrics:\n" + new_metrics)
        else:
            content += "\n" + new_metrics

    with open(file_path, "w") as f:
        f.write(content)
except FileNotFoundError:
    print("usa_signal_bot/observability/metrics_collector.py not found. Skipping...")
