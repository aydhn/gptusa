from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingCandidate, SizingPolicy, SizingPrototypeResult, SizingMethodKind

def build_fixed_fractional_sizing_results(candidates: list[SizingCandidate], policy: SizingPolicy) -> list[SizingPrototypeResult]:
    results = []
    for c in candidates:
        r = SizingPrototypeResult(
            symbol=c.symbol,
            method_kind=SizingMethodKind.FIXED_FRACTIONAL_PROTOTYPE,
            method_name="Fixed Fractional Prototype",
            raw_prototype_fraction=calculate_fixed_fractional_prototype(c, policy),
            prototype_valid=True,
            research_prototype_only=True,
            actual_position_size=None,
            target_weight=None,
            allocation=None,
            order_size=None,
            capital_allocation=None,
            live_signal=False,
            order_decision=False,
            not_investment_advice=True
        )
        results.append(r)
    return results

def calculate_fixed_fractional_prototype(candidate: SizingCandidate, policy: SizingPolicy) -> float | None:
    if not candidate.eligible_for_research_prototype:
        return 0.0
    return policy.base_prototype_fraction

def validate_fixed_fractional_sizing_results(items: list[SizingPrototypeResult]) -> list[str]:
    errors = []
    for i, r in enumerate(items):
        if not r.research_prototype_only:
            errors.append(f"Result {i} not research_prototype_only.")
        if r.actual_position_size is not None:
            errors.append(f"Result {i} produces actual position size.")
        if r.target_weight is not None:
            errors.append(f"Result {i} produces target weight.")
        if r.allocation is not None:
            errors.append(f"Result {i} produces allocation.")
    return errors

def fixed_fractional_sizing_summary(items: list[SizingPrototypeResult]) -> dict[str, Any]:
    return {"count": len(items), "valid": len(validate_fixed_fractional_sizing_results(items)) == 0}

def fixed_fractional_sizing_to_text(items: list[SizingPrototypeResult], limit: int = 300) -> str:
    return f"Fixed Fractional Sizing Results: {len(items)}"[:limit]
