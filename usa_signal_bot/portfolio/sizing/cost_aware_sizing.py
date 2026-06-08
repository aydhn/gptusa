from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingCandidate, SizingPolicy, SizingPrototypeResult, SizingMethodKind

def build_cost_aware_sizing_results(candidates: list[SizingCandidate], policy: SizingPolicy) -> list[SizingPrototypeResult]:
    results = []
    for c in candidates:
        r = SizingPrototypeResult(
            symbol=c.symbol,
            method_kind=SizingMethodKind.COST_AWARE_PROTOTYPE,
            method_name="Cost Aware Prototype",
            raw_prototype_fraction=calculate_cost_aware_prototype(c, policy),
            cost_penalty=calculate_cost_penalty(c.cost_proxy) if policy.cost_penalty_enabled else 0.0,
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

def calculate_cost_penalty(cost_proxy: float | None) -> float:
    if cost_proxy is None or cost_proxy <= 0:
        return 0.0
    return min(1.0, cost_proxy * 5.0)

def calculate_cost_aware_prototype(candidate: SizingCandidate, policy: SizingPolicy) -> float | None:
    if not candidate.eligible_for_research_prototype:
        return 0.0
    base = policy.base_prototype_fraction
    penalty = calculate_cost_penalty(candidate.cost_proxy) if policy.cost_penalty_enabled else 0.0
    return max(0.0, base * (1.0 - penalty))

def validate_cost_aware_sizing_results(items: list[SizingPrototypeResult]) -> list[str]:
    errors = []
    for i, r in enumerate(items):
        if not r.research_prototype_only:
            errors.append(f"Result {i} not research_prototype_only.")
        if r.actual_position_size is not None:
            errors.append(f"Result {i} produces actual position size.")
    return errors

def cost_aware_sizing_summary(items: list[SizingPrototypeResult]) -> dict[str, Any]:
    return {"count": len(items), "valid": len(validate_cost_aware_sizing_results(items)) == 0}

def cost_aware_sizing_to_text(items: list[SizingPrototypeResult], limit: int = 300) -> str:
    return f"Cost Aware Sizing Results: {len(items)}"[:limit]
