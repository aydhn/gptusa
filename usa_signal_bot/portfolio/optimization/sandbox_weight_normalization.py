from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy

def normalize_optimizer_results(results: List[OptimizerSandboxResult], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    total_w = sum(r.sandbox_optimizer_weight or 0.0 for r in results)
    if total_w <= 0:
        for r in results: r.normalized_sandbox_optimizer_weight = 0.0
        return results

    for r in results:
        r.normalized_sandbox_optimizer_weight = (r.sandbox_optimizer_weight or 0.0) / total_w
    return results

def apply_optimizer_weight_cap(results: List[OptimizerSandboxResult], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    cap = policy.max_sandbox_optimizer_weight
    for r in results:
        w = r.normalized_sandbox_optimizer_weight or 0.0
        if w > cap:
            r.normalized_sandbox_optimizer_weight = cap
            r.cap_applied = True
    return results

def apply_optimizer_group_cap(results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerSandboxResult]:
    c_map = {c.symbol: c for c in candidates}
    groups = {}
    for r in results:
        g = c_map.get(r.symbol, OptimizerSandboxCandidate()).concentration_group or "DEFAULT"
        groups[g] = groups.get(g, 0.0) + (r.normalized_sandbox_optimizer_weight or 0.0)

    cap = policy.max_group_sandbox_optimizer_weight
    for r in results:
        g = c_map.get(r.symbol, OptimizerSandboxCandidate()).concentration_group or "DEFAULT"
        if groups.get(g, 0.0) > cap:
            ratio = cap / groups[g]
            r.normalized_sandbox_optimizer_weight = (r.normalized_sandbox_optimizer_weight or 0.0) * ratio
            r.group_sandbox_optimizer_weight = groups[g]
    return results

def zero_ineligible_optimizer_candidates(results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate]) -> List[OptimizerSandboxResult]:
    c_map = {c.symbol: c for c in candidates}
    for r in results:
        c = c_map.get(r.symbol)
        if not c or not c.eligible_for_optimizer_sandbox:
            r.normalized_sandbox_optimizer_weight = 0.0
            r.zeroed_by_constraint = True
    return results

def validate_normalized_optimizer_results(results: List[OptimizerSandboxResult]) -> List[str]:
    errs = []
    for r in results:
        if r.actual_target_weight is not None: errs.append(f"{r.symbol}: actual_target_weight not None")
    return errs

def sandbox_weight_normalization_summary(results: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"count": len(results)}
