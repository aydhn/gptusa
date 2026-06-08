from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerMethodKind

def build_risk_budget_optimizer_results(candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    res = []
    for c in candidates:
        w = calculate_risk_budget_adjusted_weight(c, policy)
        r = OptimizerSandboxResult(
            symbol=c.symbol,
            method_kind=OptimizerMethodKind.RISK_BUDGET_AWARE_SANDBOX_OPTIMIZER,
            method_name="risk_budget_aware",
            sandbox_optimizer_weight=w,
            optimization_research_sandbox=True,
            result_valid=True
        )
        res.append(r)
    return res

def calculate_risk_budget_adjusted_weight(candidate: OptimizerSandboxCandidate, policy: OptimizerPolicy) -> Optional[float]:
    base = candidate.sandbox_score or 1.0
    risk = candidate.risk_budget_score or 1.0
    if risk <= 0: return 0.0
    return max(0.0, base / risk)

def validate_risk_budget_optimizer_results(items: List[OptimizerSandboxResult]) -> List[str]:
    return [f"{i.symbol}: target weight present" for i in items if i.actual_target_weight is not None]

def risk_budget_optimizer_summary(items: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"count": len(items)}
