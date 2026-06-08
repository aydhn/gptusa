from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerObjectiveContract, OptimizerPolicy, OptimizerObjectiveKind

def build_optimizer_objective_contracts(policy: OptimizerPolicy) -> List[OptimizerObjectiveContract]:
    return [
        OptimizerObjectiveContract(
            objective_kind=OptimizerObjectiveKind.MAXIMIZE_SANDBOX_SCORE,
            objective_name="Maximize Sandbox Score",
            enabled=True, deterministic=True, contract_only=True,
            weight_in_composite=policy.score_objective_weight,
            produces_objective_score=True, produces_actual_target_weight=False, produces_actual_allocation=False
        ),
        OptimizerObjectiveContract(
            objective_kind=OptimizerObjectiveKind.MINIMIZE_CONCENTRATION,
            objective_name="Minimize Concentration",
            enabled=True, deterministic=True, contract_only=True,
            weight_in_composite=policy.concentration_objective_weight,
            produces_objective_score=True, produces_actual_target_weight=False, produces_actual_allocation=False
        )
    ]

def validate_optimizer_objective_contracts(items: List[OptimizerObjectiveContract]) -> List[str]:
    errs = []
    for i in items:
        if i.produces_actual_target_weight: errs.append(f"{i.objective_kind}: produces target weight")
        if i.produces_actual_allocation: errs.append(f"{i.objective_kind}: produces allocation")
        if not i.produces_objective_score: errs.append(f"{i.objective_kind}: does not produce score")
    return errs

def optimizer_objective_contracts_summary(items: List[OptimizerObjectiveContract]) -> Dict[str, Any]:
    return {"count": len(items)}

def optimizer_objective_contracts_to_text(items: List[OptimizerObjectiveContract], limit: int = 300) -> str:
    return str([i.to_dict() for i in items])[:limit]
