with open("usa_signal_bot/quality/data_quality_evaluator.py", "r") as f:
    content = f.read()

quality_add = """
        self.phase130_regime_transition_ingestion_score = 0.0
        self.phase130_market_behavior_profile_score = 0.0
        self.phase130_regime_behavior_summary_score = 0.0
        self.phase130_diagnostics_interpretation_score = 0.0
        self.phase130_behavior_report_score = 0.0
        self.phase130_report_qa_score = 0.0
        self.phase130_readiness_gate_score = 0.0
        self.phase130_safety_score = 0.0
        self.phase130_non_execution_compliance_score = 0.0
        self.phase130_no_model_training_compliance_score = 0.0
        self.phase130_no_model_prediction_compliance_score = 0.0
"""

if "phase130_regime_transition_ingestion_score" not in content:
    import re
    content = re.sub(
        r'(def __init__\(self\):\n(?:        self\.[^\n]+\n)*)',
        r'\1' + quality_add,
        content
    )
    with open("usa_signal_bot/quality/data_quality_evaluator.py", "w") as f:
        f.write(content)

print("Updated data_quality_evaluator.py")
