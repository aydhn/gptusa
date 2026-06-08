from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerMethodKind

def build_score_maximizing_optimizer_results(candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    res = []
    for c in candidates:
        w = calculate_score_maximizing_weight(c, policy)
        r = OptimizerSandboxResult(
            symbol=c.symbol,
            method_kind=OptimizerMethodKind.SCORE_MAXIMIZING_SANDBOX_OPTIMIZER,
            method_name="score_maximizing",
            sandbox_optimizer_weight=w,
            optimization_research_sandbox=True,
            result_valid=True
        )
        res.append(r)
    return res

def calculate_score_maximizing_weight(candidate: OptimizerSandboxCandidate, policy: OptimizerPolicy) -> Optional[float]:
    if not candidate.sandbox_score or candidate.sandbox_score <= 0: return 0.0
    return candidate.sandbox_score

def validate_score_maximizing_optimizer_results(items: List[OptimizerSandboxResult]) -> List[str]:
    errs = []
    for i in items:
        if i.actual_target_weight is not None: errs.append(f"{i.symbol}: actual target weight present")
    return errs

def score_maximizing_optimizer_summary(items: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"count": len(items)}
