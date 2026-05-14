
from typing import List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import CostRobustnessStatus, CostFragilityReason
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressedBacktestResult, ExecutionSensitivityMatrix, CostFragilityAssessment,
    create_cost_fragility_assessment_id
)

def fragility_reasons_for_result(result: CostStressedBacktestResult) -> List[CostFragilityReason]:
    reasons = []
    if result.profitable_after_costs is False:
        reasons.append(CostFragilityReason.PROFIT_ERASED_BY_COSTS)
    if result.gross_sharpe and result.stressed_sharpe:
        if result.stressed_sharpe < result.gross_sharpe * 0.5:
            reasons.append(CostFragilityReason.SHARPE_COLLAPSE)
    return reasons

def fragility_score_from_results(stressed_results: List[CostStressedBacktestResult]) -> Optional[float]:
    if not stressed_results:
        return None
    passed = sum(1 for r in stressed_results if r.profitable_after_costs is True)
    return (passed / len(stressed_results)) * 100.0

def classify_cost_robustness_from_fragility_score(score: Optional[float]) -> CostRobustnessStatus:
    if score is None:
        return CostRobustnessStatus.INSUFFICIENT_DATA
    if score >= 80:
        return CostRobustnessStatus.ROBUST
    if score >= 50:
        return CostRobustnessStatus.ACCEPTABLE
    return CostRobustnessStatus.FRAGILE

def detect_cost_fragility(stressed_results: List[CostStressedBacktestResult], matrix: Optional[ExecutionSensitivityMatrix] = None) -> CostFragilityAssessment:
    reasons = set()
    for r in stressed_results:
        reasons.update(fragility_reasons_for_result(r))

    score = fragility_score_from_results(stressed_results)
    status = classify_cost_robustness_from_fragility_score(score)

    return CostFragilityAssessment(
        assessment_id=create_cost_fragility_assessment_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        fragility_score=score,
        reasons=list(reasons),
        breakeven_cost_bps=None,
        breakeven_slippage_bps=None,
        breakeven_impact_bps=None,
        evidence={},
        warnings=[],
        errors=[]
    )

def cost_fragility_assessment_to_text(assessment: CostFragilityAssessment) -> str:
    lines = [
        f"--- Cost Fragility Assessment ---",
        f"Status: {assessment.status.value}",
        f"Score: {assessment.fragility_score}",
        f"Reasons: {[r.value for r in assessment.reasons]}"
    ]
    return "\n".join(lines)
