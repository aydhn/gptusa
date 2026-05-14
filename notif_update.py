import os

file_path = "usa_signal_bot/notifications/notification_templates.py"

content = """
from typing import Any, Dict, List
from usa_signal_bot.cost_robustness.robustness_models import CostRobustnessReview, CostFragilityAssessment, ExecutionSensitivityMatrix

def format_cost_robustness_report_message(review: CostRobustnessReview) -> Dict[str, Any]:
    return {"message": "Cost Robustness Report", "review_id": review.review_id}

def format_cost_fragility_warning_message(assessment: CostFragilityAssessment) -> Dict[str, Any]:
    return {"message": "Cost Fragility Warning", "score": assessment.fragility_score}

def format_execution_sensitivity_warning_message(matrix: ExecutionSensitivityMatrix) -> Dict[str, Any]:
    return {"message": "Execution Sensitivity Warning", "status": matrix.robustness_status}

def notifications_from_cost_robustness_review(review: CostRobustnessReview) -> List[Dict[str, Any]]:
    return [format_cost_robustness_report_message(review)]
"""

if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
else:
    with open(file_path, "a") as f:
        f.write("\n" + content)
