from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionPlan, PortfolioAllocation
from usa_signal_bot.core.enums import PortfolioAllocationStatus
from usa_signal_bot.portfolio_construction.candidate_adapter import attach_portfolio_allocation_to_candidate
from typing import Any

def apply_portfolio_plan_to_paper_candidates(candidates: list[dict[str, Any]], plan: PortfolioConstructionPlan) -> list[dict[str, Any]]:
    alloc_map = {a.symbol: a for a in plan.allocations}
    res = []
    for c in candidates:
        sym = c.get("symbol")
        if sym in alloc_map:
            res.append(attach_portfolio_allocation_to_candidate(c, alloc_map[sym]))
        else:
            res.append(c)
    return res

def apply_portfolio_allocation_to_paper_order(order: dict[str, Any], allocation: PortfolioAllocation) -> dict[str, Any]:
    res = dict(order)
    res["portfolio_allocation_status"] = allocation.status.value if hasattr(allocation.status, 'value') else str(allocation.status)
    res["portfolio_final_notional_usd"] = allocation.final_notional_usd
    return res

def paper_order_allowed_by_portfolio_allocation(allocation: PortfolioAllocation) -> bool:
    return allocation.status not in [PortfolioAllocationStatus.BLOCKED, PortfolioAllocationStatus.SUPPRESSED]

def paper_portfolio_construction_summary(orders_or_candidates: list[dict[str, Any]]) -> dict[str, Any]:
    allowed = 0
    blocked = 0
    for o in orders_or_candidates:
        if o.get("portfolio_allocation_status") in ["BLOCKED", "SUPPRESSED"]:
            blocked += 1
        else:
            allowed += 1
    return {
        "allowed": allowed,
        "blocked_or_suppressed": blocked
    }
