from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerMethodKind

def build_equal_baseline_optimizer_results(candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    n = len(candidates)
    if n == 0: return []
    w = 1.0 / n
    res = []
    for c in candidates:
        r = OptimizerSandboxResult(
            symbol=c.symbol,
            method_kind=OptimizerMethodKind.EQUAL_BASELINE_SANDBOX_OPTIMIZER,
            method_name="equal_baseline",
            sandbox_optimizer_weight=w,
            normalized_sandbox_optimizer_weight=w,
            optimization_research_sandbox=True,
            result_valid=True
        )
        res.append(r)
    return res

def validate_equal_baseline_optimizer_results(items: List[OptimizerSandboxResult]) -> List[str]:
    errs = []
    for i in items:
        if i.actual_target_weight is not None: errs.append(f"{i.symbol}: actual target weight present")
        if not i.optimization_research_sandbox: errs.append(f"{i.symbol}: not research sandbox")
    return errs

def equal_baseline_optimizer_summary(items: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"count": len(items)}

def equal_baseline_optimizer_to_text(items: List[OptimizerSandboxResult], limit: int = 300) -> str:
    return str([i.to_dict() for i in items])[:limit]
