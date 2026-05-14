from typing import Any
from usa_signal_bot.transaction_costs.cost_models import TransactionCostBreakdown

def attach_cost_estimate_to_signal(signal: dict[str, Any], cost_breakdown: TransactionCostBreakdown) -> dict[str, Any]:
    signal["estimated_cost_bps"] = cost_breakdown.total_cost_bps
    signal["estimated_cost_usd"] = cost_breakdown.total_cost_usd
    return signal

def attach_cost_estimate_to_candidate(candidate: dict[str, Any], cost_breakdown: TransactionCostBreakdown) -> dict[str, Any]:
    candidate["estimated_cost_bps"] = cost_breakdown.total_cost_bps
    candidate["estimated_cost_usd"] = cost_breakdown.total_cost_usd
    return candidate

def cost_penalty_from_breakdown(cost_breakdown: TransactionCostBreakdown) -> float:
    bps = cost_breakdown.total_cost_bps
    if not bps:
        return 0.0
    # Penalty is 0.05 for every 100 bps
    return (bps / 100.0) * 0.05

def suppress_candidate_if_cost_too_high(
    candidate: dict[str, Any],
    cost_breakdown: TransactionCostBreakdown,
    max_cost_bps: float = 250.0
) -> dict[str, Any]:
    bps = cost_breakdown.total_cost_bps
    if bps and bps > max_cost_bps:
        candidate["suppressed_by_transaction_cost"] = True
        candidate["suppression_reason"] = f"Estimated cost {bps:.1f} bps exceeds max {max_cost_bps} bps"
    return candidate

def candidate_cost_summary(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    suppressed = sum(1 for c in candidates if c.get("suppressed_by_transaction_cost"))
    return {
        "total_candidates": len(candidates),
        "suppressed_by_cost_count": suppressed
    }
