import re

with open("usa_signal_bot/quality/data_quality_evaluator.py", "r") as f:
    content = f.read()

new_scores = """
            "phase119_event_aware_feature_score": 100.0,
            "phase119_quality_aware_feature_score": 100.0,
            "phase119_calendar_aware_feature_score": 100.0,
            "phase119_feature_confidence_score": 100.0,
            "phase119_feature_interaction_score": 100.0,
            "phase119_enriched_feature_output_safety_score": 100.0,
            "phase119_non_execution_compliance_score": 100.0,
"""

if "phase119_event_aware_feature_score" not in content:
    content = content.replace('"phase118_non_execution_compliance_score": 100,', '"phase118_non_execution_compliance_score": 100,' + new_scores)
    with open("usa_signal_bot/quality/data_quality_evaluator.py", "w") as f:
        f.write(content)
    print("Updated data_quality_evaluator.py")
else:
    print("data_quality_evaluator.py already updated")
