from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerMethodKind

def build_concentration_minimizing_optimizer_results(candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    res = []
    n = len(candidates)
    for c in candidates:
        w = calculate_concentration_minimizing_weight(c, n, policy)
        r = OptimizerSandboxResult(
            symbol=c.symbol,
            method_kind=OptimizerMethodKind.CONCENTRATION_MINIMIZING_SANDBOX_OPTIMIZER,
            method_name="concentration_minimizing",
            sandbox_optimizer_weight=w,
            optimization_research_sandbox=True,
            result_valid=True
        )
        res.append(r)
    return res

def calculate_concentration_minimizing_weight(candidate: OptimizerSandboxCandidate, candidate_count: int, policy: OptimizerPolicy) -> Optional[float]:
    if candidate_count == 0: return 0.0
    base = candidate.sandbox_score or 1.0
    return max(0.0, base * (1.0 / candidate_count))

def validate_concentration_minimizing_optimizer_results(items: List[OptimizerSandboxResult]) -> List[str]:
    return [f"{i.symbol}: target weight present" for i in items if i.actual_target_weight is not None]

def concentration_minimizing_optimizer_summary(items: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"count": len(items)}
