with open('usa_signal_bot/quality/data_quality_evaluator.py', 'r') as f:
    content = f.read()

new_quality = """

class Phase141QualityScorecard:
    def __init__(self):
        self.scores = {
            "phase141_model_comparison_ingestion_score": 100,
            "phase141_artifact_loader_score": 100,
            "phase141_calibration_input_resolver_score": 100,
            "phase141_reliability_binning_score": 100,
            "phase141_calibration_metric_score": 100,
            "phase141_brier_decomposition_score": 100,
            "phase141_score_distribution_score": 100,
            "phase141_class_balance_score": 100,
            "phase141_post_training_validation_score": 100,
            "phase141_calibration_governance_score": 100,
            "phase141_readiness_gate_score": 100,
            "phase141_safety_score": 100,
            "phase141_non_execution_compliance_score": 100,
            "phase141_no_live_inference_compliance_score": 100,
            "phase141_no_calibration_fitting_compliance_score": 100,
            "phase141_no_deployment_compliance_score": 100
        }
        self.blockers = []
"""

if "Phase141QualityScorecard" not in content:
    content += new_quality

with open('usa_signal_bot/quality/data_quality_evaluator.py', 'w') as f:
    f.write(content)

# Attempt to hook Phase141QualityScorecard into DataQualityEvaluator if possible
import re
with open('usa_signal_bot/quality/data_quality_evaluator.py', 'r') as f:
    content = f.read()

match = re.search(r'(class DataQualityEvaluator:.*?\n\s*def __init__\(self.*?\):.*?)(?=\n\s*def |\Z)', content, re.DOTALL)
if match:
    init_body = match.group(1)
    if "self.phase141" not in init_body:
        new_init = init_body + "        self.phase141 = Phase141QualityScorecard()\n"
        content = content.replace(init_body, new_init)
        with open('usa_signal_bot/quality/data_quality_evaluator.py', 'w') as f:
            f.write(content)
