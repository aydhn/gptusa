
from typing import List, Optional, Dict
from usa_signal_bot.core.enums import CostRobustnessStatus
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressedBacktestResult, ExecutionSensitivityMatrix, WalkForwardCostRobustnessResult
)

def classify_cost_robustness_status(score: Optional[float]) -> CostRobustnessStatus:
    if score is None:
        return CostRobustnessStatus.INSUFFICIENT_DATA
    if score >= 80:
        return CostRobustnessStatus.ROBUST
    if score >= 50:
        return CostRobustnessStatus.ACCEPTABLE
    return CostRobustnessStatus.FRAGILE

def calculate_cost_robustness_score(stressed_results: List[CostStressedBacktestResult], matrix: Optional[ExecutionSensitivityMatrix] = None, wf_result: Optional[WalkForwardCostRobustnessResult] = None) -> Optional[float]:
    if not stressed_results:
        return None
    passed = sum(1 for r in stressed_results if r.profitable_after_costs is True)
    return (passed / len(stressed_results)) * 100.0

def component_scores_from_cost_robustness(stressed_results: List[CostStressedBacktestResult], matrix: Optional[ExecutionSensitivityMatrix] = None) -> Dict[str, Optional[float]]:
    score = calculate_cost_robustness_score(stressed_results)
    return {
        "net_profitability_survival": score,
        "sharpe_survival": score * 0.9 if score else None
    }

def cost_robustness_score_to_text(score: Optional[float], status: CostRobustnessStatus) -> str:
    return f"Robustness Score: {score} | Status: {status.value}"
