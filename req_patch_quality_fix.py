with open("usa_signal_bot/quality/data_quality_evaluator.py", "r") as f:
    content = f.read()

import re
content = re.sub(
    r'(class DataQualityEvaluator:\n    def __init__\(self\):\n        self\.scores = \{.*?)\n\s+self\.phase130_regime_transition_ingestion_score = 0\.0',
    r'\1',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'\s+self\.phase130_market_behavior_profile_score = 0\.0.*?\s+self\.phase130_no_model_prediction_compliance_score = 0\.0',
    r'',
    content,
    flags=re.DOTALL
)

add_quality = """
            "phase130_regime_transition_ingestion_score": 0.0,
            "phase130_market_behavior_profile_score": 0.0,
            "phase130_regime_behavior_summary_score": 0.0,
            "phase130_diagnostics_interpretation_score": 0.0,
            "phase130_behavior_report_score": 0.0,
            "phase130_report_qa_score": 0.0,
            "phase130_readiness_gate_score": 0.0,
            "phase130_safety_score": 0.0,
            "phase130_non_execution_compliance_score": 0.0,
            "phase130_no_model_training_compliance_score": 0.0,
            "phase130_no_model_prediction_compliance_score": 0.0,
"""

if "phase130_regime_transition_ingestion_score" not in content:
    content = content.replace('"phase114_provider_freeze_score": 0.0,', add_quality + '            "phase114_provider_freeze_score": 0.0,')

with open("usa_signal_bot/quality/data_quality_evaluator.py", "w") as f:
    f.write(content)
