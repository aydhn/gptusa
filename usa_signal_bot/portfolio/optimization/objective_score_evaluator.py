from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerObjectiveScore, OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerObjectiveKind, OptimizerMethodKind

def build_optimizer_objective_scores(results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerObjectiveScore]:
    methods = {r.method_kind for r in results}
    scores = []
    for mk in methods:
        res_m = [r for r in results if r.method_kind == mk]
        score_dict = calculate_objective_score_for_method(mk, res_m, candidates, policy)
        for okind, val in score_dict.items():
            scores.append(OptimizerObjectiveScore(
                method_kind=mk,
                objective_kind=okind,
                value=val,
                score_valid=True,
                research_sandbox_only=True,
                not_investment_advice=True
            ))
    return scores

def calculate_objective_score_for_method(method_kind: OptimizerMethodKind, results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> Dict[OptimizerObjectiveKind, Any]:
    return {
        OptimizerObjectiveKind.MAXIMIZE_SANDBOX_SCORE: sum(r.normalized_sandbox_optimizer_weight or 0.0 for r in results) * 10.0,
        OptimizerObjectiveKind.MINIMIZE_CONCENTRATION: calculate_herfindahl_from_optimizer_results(results) or 1.0,
        OptimizerObjectiveKind.MAXIMIZE_ROBUSTNESS_SCORE: sum(r.normalized_sandbox_optimizer_weight or 0.0 for r in results) * 5.0
    }

def calculate_effective_name_count_from_optimizer_results(results: List[OptimizerSandboxResult]) -> float:
    h = calculate_herfindahl_from_optimizer_results(results)
    if not h or h == 0: return 0.0
    return 1.0 / h

def calculate_herfindahl_from_optimizer_results(results: List[OptimizerSandboxResult]) -> float:
    return sum((r.normalized_sandbox_optimizer_weight or 0.0)**2 for r in results)

def validate_optimizer_objective_scores(items: List[OptimizerObjectiveScore]) -> List[str]:
    return ["Score missing research_sandbox_only flag"] if any(not i.research_sandbox_only for i in items) else []

def optimizer_objective_scores_summary(items: List[OptimizerObjectiveScore]) -> Dict[str, Any]:
    return {"count": len(items)}
