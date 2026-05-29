with open("usa_signal_bot/observability/metrics_collector.py", "r") as f:
    content = f.read()

metrics_add = """
        self.latest_market_behavior_context_count = 0
        self.latest_market_behavior_profile_count = 0
        self.latest_regime_behavior_summary_count = 0
        self.latest_diagnostics_interpretation_count = 0
        self.latest_behavior_report_document_count = 0
        self.latest_behavior_report_qa_pass_count = 0
        self.latest_behavior_report_qa_warning_count = 0
        self.latest_market_behavior_readiness_gate_pass_count = 0
        self.latest_behavior_report_language_risk_count = 0
        self.latest_phase130_model_training_violation_count = 0
        self.latest_phase130_model_prediction_violation_count = 0
        self.latest_phase130_execution_violation_count = 0
        self.latest_phase130_activation_violation_count = 0
"""

if "latest_market_behavior_context_count" not in content:
    import re
    content = re.sub(
        r'(def __init__\(self\):\n(?:        self\.[^\n]+\n)*)',
        r'\1' + metrics_add,
        content
    )
    with open("usa_signal_bot/observability/metrics_collector.py", "w") as f:
        f.write(content)

print("Updated metrics_collector.py")
