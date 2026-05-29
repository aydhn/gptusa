with open("usa_signal_bot/observability/metrics_collector.py", "r") as f:
    content = f.read()

# Fix the syntax error in MetricsCollector
import re
content = re.sub(
    r'(class MetricsCollector:\n    def __init__\(self\):\n        self\.metrics = \{.*?)\n\s+self\.latest_market_behavior_context_count = 0',
    r'\1',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'\s+self\.latest_market_behavior_profile_count = 0.*?\s+self\.latest_phase130_activation_violation_count = 0',
    r'',
    content,
    flags=re.DOTALL
)

# And properly append to the dict
add_metrics = """
            "latest_market_behavior_context_count": 0,
            "latest_market_behavior_profile_count": 0,
            "latest_regime_behavior_summary_count": 0,
            "latest_diagnostics_interpretation_count": 0,
            "latest_behavior_report_document_count": 0,
            "latest_behavior_report_qa_pass_count": 0,
            "latest_behavior_report_qa_warning_count": 0,
            "latest_market_behavior_readiness_gate_pass_count": 0,
            "latest_behavior_report_language_risk_count": 0,
            "latest_phase130_model_training_violation_count": 0,
            "latest_phase130_model_prediction_violation_count": 0,
            "latest_phase130_execution_violation_count": 0,
            "latest_phase130_activation_violation_count": 0,
"""

content = content.replace('"latest_advanced_feature_context_count": 0,', add_metrics + '            "latest_advanced_feature_context_count": 0,')

with open("usa_signal_bot/observability/metrics_collector.py", "w") as f:
    f.write(content)
