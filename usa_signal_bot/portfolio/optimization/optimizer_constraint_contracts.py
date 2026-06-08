from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerConstraintContract, OptimizerPolicy, OptimizerConstraintKind

def build_optimizer_constraint_contracts(policy: OptimizerPolicy) -> List[OptimizerConstraintContract]:
    return [
        OptimizerConstraintContract(
            constraint_kind=OptimizerConstraintKind.MAX_SANDBOX_OPTIMIZER_WEIGHT,
            constraint_name="Max Sandbox Weight",
            enabled=True, deterministic=True, contract_only=True,
            limit_value=policy.max_sandbox_optimizer_weight,
            produces_actual_target_weight=False, produces_actual_allocation=False, produces_order_size=False
        ),
        OptimizerConstraintContract(
            constraint_kind=OptimizerConstraintKind.NO_ACTUAL_TARGET_WEIGHT,
            constraint_name="No Actual Target Weight",
            enabled=True, deterministic=True, contract_only=True,
            limit_value=True,
            produces_actual_target_weight=False, produces_actual_allocation=False, produces_order_size=False
        )
    ]

def validate_optimizer_constraint_contracts(items: List[OptimizerConstraintContract]) -> List[str]:
    errs = []
    for i in items:
        if i.produces_actual_target_weight: errs.append(f"{i.constraint_kind}: produces target weight")
        if i.produces_actual_allocation: errs.append(f"{i.constraint_kind}: produces allocation")
        if i.produces_order_size: errs.append(f"{i.constraint_kind}: produces order size")
        if not i.contract_only: errs.append(f"{i.constraint_kind}: not contract only")
    return errs

def optimizer_constraint_contracts_summary(items: List[OptimizerConstraintContract]) -> Dict[str, Any]:
    return {"count": len(items)}

def optimizer_constraint_contracts_to_text(items: List[OptimizerConstraintContract], limit: int = 300) -> str:
    return str([i.to_dict() for i in items])[:limit]
