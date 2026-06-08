from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingMethodContract, SizingMethodKind, SizingPolicy

def build_sizing_method_contracts(policy: SizingPolicy) -> list[SizingMethodContract]:
    kinds = [
        SizingMethodKind.FIXED_FRACTIONAL_PROTOTYPE,
        SizingMethodKind.VOLATILITY_ADJUSTED_PROTOTYPE,
        SizingMethodKind.DRAWDOWN_ADJUSTED_PROTOTYPE,
        SizingMethodKind.COST_AWARE_PROTOTYPE,
        SizingMethodKind.LIQUIDITY_AWARE_PROTOTYPE,
        SizingMethodKind.ROBUSTNESS_ADJUSTED_PROTOTYPE
    ]
    contracts = []
    for k in kinds:
        contracts.append(SizingMethodContract(
            method_kind=k,
            method_name=k.value,
            enabled=True,
            deterministic=True,
            contract_only=True,
            produces_research_prototype_fraction=True,
            produces_actual_position_size=False,
            produces_target_weight=False,
            produces_allocation=False,
            produces_order_size=False,
            produces_capital_allocation=False,
            rationale="Deterministic research prototype sizing boundary."
        ))
    return contracts

def validate_sizing_method_contracts(items: list[SizingMethodContract]) -> list[str]:
    errors = []
    for i, c in enumerate(items):
        if c.produces_actual_position_size:
            errors.append(f"Contract {i} produces actual position size.")
        if c.produces_target_weight:
            errors.append(f"Contract {i} produces target weight.")
        if c.produces_allocation:
            errors.append(f"Contract {i} produces allocation.")
        if c.produces_order_size:
            errors.append(f"Contract {i} produces order size.")
        if c.produces_capital_allocation:
            errors.append(f"Contract {i} produces capital allocation.")
    return errors

def sizing_method_contracts_summary(items: list[SizingMethodContract]) -> dict[str, Any]:
    return {"contract_count": len(items), "valid": len(validate_sizing_method_contracts(items)) == 0}

def sizing_method_contracts_to_text(items: list[SizingMethodContract], limit: int = 300) -> str:
    return f"Built {len(items)} sizing method contracts."[:limit]
