from typing import Any
import math
from usa_signal_bot.portfolio.sizing.phase154_models import SizingCandidate, SizingPolicy, SizingPrototypeResult, SizingMethodKind

def build_volatility_adjusted_sizing_results(candidates: list[SizingCandidate], policy: SizingPolicy) -> list[SizingPrototypeResult]:
    results = []
    for c in candidates:
        r = SizingPrototypeResult(
            symbol=c.symbol,
            method_kind=SizingMethodKind.VOLATILITY_ADJUSTED_PROTOTYPE,
            method_name="Volatility Adjusted Prototype",
            raw_prototype_fraction=calculate_volatility_adjusted_prototype(c, policy),
            volatility_penalty=calculate_volatility_penalty(c.volatility_proxy) if policy.volatility_penalty_enabled else 0.0,
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

def calculate_volatility_penalty(volatility_proxy: float | None) -> float:
    if volatility_proxy is None or volatility_proxy <= 0:
        return 0.0
    return min(1.0, math.sqrt(volatility_proxy) / 10.0)

def calculate_volatility_adjusted_prototype(candidate: SizingCandidate, policy: SizingPolicy) -> float | None:
    if not candidate.eligible_for_research_prototype:
        return 0.0
    base = policy.base_prototype_fraction
    penalty = calculate_volatility_penalty(candidate.volatility_proxy) if policy.volatility_penalty_enabled else 0.0
    return max(0.0, base * (1.0 - penalty))

def validate_volatility_adjusted_sizing_results(items: list[SizingPrototypeResult]) -> list[str]:
    errors = []
    for i, r in enumerate(items):
        if not r.research_prototype_only:
            errors.append(f"Result {i} not research_prototype_only.")
        if r.actual_position_size is not None:
            errors.append(f"Result {i} produces actual position size.")
    return errors

def volatility_adjusted_sizing_summary(items: list[SizingPrototypeResult]) -> dict[str, Any]:
    return {"count": len(items), "valid": len(validate_volatility_adjusted_sizing_results(items)) == 0}

def volatility_adjusted_sizing_to_text(items: list[SizingPrototypeResult], limit: int = 300) -> str:
    return f"Volatility Adjusted Sizing Results: {len(items)}"[:limit]
