from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingCandidate, SizingPolicy, SizingPrototypeResult, SizingMethodKind

def build_liquidity_aware_sizing_results(candidates: list[SizingCandidate], policy: SizingPolicy) -> list[SizingPrototypeResult]:
    results = []
    for c in candidates:
        r = SizingPrototypeResult(
            symbol=c.symbol,
            method_kind=SizingMethodKind.LIQUIDITY_AWARE_PROTOTYPE,
            method_name="Liquidity Aware Prototype",
            raw_prototype_fraction=calculate_liquidity_aware_prototype(c, policy),
            liquidity_penalty=calculate_liquidity_penalty(c.liquidity_proxy) if policy.liquidity_penalty_enabled else 0.0,
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

def calculate_liquidity_penalty(liquidity_proxy: float | None) -> float:
    if liquidity_proxy is None or liquidity_proxy >= 1.0:
        return 0.0
    return min(1.0, (1.0 - liquidity_proxy) * 2.0)

def calculate_liquidity_aware_prototype(candidate: SizingCandidate, policy: SizingPolicy) -> float | None:
    if not candidate.eligible_for_research_prototype:
        return 0.0
    base = policy.base_prototype_fraction
    penalty = calculate_liquidity_penalty(candidate.liquidity_proxy) if policy.liquidity_penalty_enabled else 0.0
    return max(0.0, base * (1.0 - penalty))

def validate_liquidity_aware_sizing_results(items: list[SizingPrototypeResult]) -> list[str]:
    errors = []
    for i, r in enumerate(items):
        if not r.research_prototype_only:
            errors.append(f"Result {i} not research_prototype_only.")
        if r.actual_position_size is not None:
            errors.append(f"Result {i} produces actual position size.")
    return errors

def liquidity_aware_sizing_summary(items: list[SizingPrototypeResult]) -> dict[str, Any]:
    return {"count": len(items), "valid": len(validate_liquidity_aware_sizing_results(items)) == 0}

def liquidity_aware_sizing_to_text(items: list[SizingPrototypeResult], limit: int = 300) -> str:
    return f"Liquidity Aware Sizing Results: {len(items)}"[:limit]
