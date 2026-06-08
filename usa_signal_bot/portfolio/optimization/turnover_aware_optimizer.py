from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerMethodKind

def build_turnover_aware_optimizer_results(candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    res = []
    for c in candidates:
        w = calculate_turnover_aware_weight(c, policy)
        r = OptimizerSandboxResult(
            symbol=c.symbol,
            method_kind=OptimizerMethodKind.TURNOVER_AWARE_SANDBOX_OPTIMIZER,
            method_name="turnover_aware",
            sandbox_optimizer_weight=w,
            optimization_research_sandbox=True,
            result_valid=True
        )
        res.append(r)
    return res

def calculate_turnover_aware_weight(candidate: OptimizerSandboxCandidate, policy: OptimizerPolicy) -> Optional[float]:
    prev = candidate.previous_sandbox_weight or 0.0
    score = candidate.sandbox_score or 0.0
    # Toy prototype logic for turnover awareness
    return prev + (score * 0.1)

def validate_turnover_aware_optimizer_results(items: List[OptimizerSandboxResult]) -> List[str]:
    return [f"{i.symbol}: target weight present" for i in items if i.actual_target_weight is not None]

def turnover_aware_optimizer_summary(items: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"count": len(items)}
