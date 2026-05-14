import os

file_path = "usa_signal_bot/quality/data_quality_evaluator.py"

content = """
# Data Quality Evaluator extension for Cost Robustness
def evaluate_cost_robustness_dimensions(score: float, slippage_score: float, impact_score: float, sensitivity_score: float, fragility_score: float) -> dict:
    return {
        "cost_robustness_score": score,
        "slippage_stress_score": slippage_score,
        "market_impact_stress_score": impact_score,
        "execution_sensitivity_score": sensitivity_score,
        "cost_fragility_score": fragility_score
    }
"""

if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
else:
    with open(file_path, "a") as f:
        f.write("\n" + content)
