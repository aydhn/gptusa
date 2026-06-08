from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerMethodKind

def build_robustness_first_optimizer_results(candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    res = []
    for c in candidates:
        w = calculate_robustness_first_weight(c, policy)
        r = OptimizerSandboxResult(
            symbol=c.symbol,
            method_kind=OptimizerMethodKind.ROBUSTNESS_FIRST_SANDBOX_OPTIMIZER,
            method_name="robustness_first",
            sandbox_optimizer_weight=w,
            optimization_research_sandbox=True,
            result_valid=True
        )
        res.append(r)
    return res

def calculate_robustness_first_weight(candidate: OptimizerSandboxCandidate, policy: OptimizerPolicy) -> Optional[float]:
    rob = candidate.robustness_score or 1.0
    return max(0.0, rob)

def validate_robustness_first_optimizer_results(items: List[OptimizerSandboxResult]) -> List[str]:
    return [f"{i.symbol}: target weight present" for i in items if i.actual_target_weight is not None]

def robustness_first_optimizer_summary(items: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"count": len(items)}
