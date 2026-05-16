from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioAllocation, PortfolioConstructionPlan
from usa_signal_bot.portfolio_construction.sector_cluster_resolver import SectorClusterResolver
from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
from usa_signal_bot.core.enums import PortfolioAllocationStatus
from typing import Any

def portfolio_candidate_from_candidate(candidate: dict[str, Any], resolver: SectorClusterResolver | None = None) -> PortfolioCandidate:
    planner = PortfolioAllocationPlanner()
    return planner.build_candidates([candidate], resolver)[0]

def attach_portfolio_allocation_to_candidate(candidate: dict[str, Any], allocation: PortfolioAllocation) -> dict[str, Any]:
    res = dict(candidate)
    res["portfolio_final_notional_usd"] = allocation.final_notional_usd
    res["portfolio_final_quantity"] = allocation.final_quantity
    res["portfolio_weight_pct_equity"] = allocation.weight_pct_equity
    res["portfolio_allocation_status"] = allocation.status.value if hasattr(allocation.status, 'value') else str(allocation.status)
    res["portfolio_guard_decisions"] = [g.value if hasattr(g, 'value') else str(g) for g in allocation.guard_decisions]
    res["portfolio_concentration_warnings"] = allocation.warnings
    return res

def apply_portfolio_plan_to_candidates(candidates: list[dict[str, Any]], plan: PortfolioConstructionPlan) -> list[dict[str, Any]]:
    alloc_map = {a.symbol: a for a in plan.allocations}
    res = []
    for c in candidates:
        sym = c.get("symbol")
        if sym in alloc_map:
            res.append(attach_portfolio_allocation_to_candidate(c, alloc_map[sym]))
        else:
            res.append(c)
    return res

def suppress_candidate_if_portfolio_blocked(candidate: dict[str, Any], allocation: PortfolioAllocation) -> dict[str, Any]:
    res = attach_portfolio_allocation_to_candidate(candidate, allocation)
    if allocation.status in [PortfolioAllocationStatus.BLOCKED, PortfolioAllocationStatus.SUPPRESSED]:
        res["status"] = "SUPPRESSED"
        res["suppress_reason"] = "Blocked by portfolio construction guards"
    return res

def candidate_portfolio_summary(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    approved = 0
    suppressed = 0
    for c in candidates:
        status = c.get("portfolio_allocation_status")
        if status == "APPROVED": approved += 1
        elif status in ["SUPPRESSED", "BLOCKED"]: suppressed += 1
    return {
        "approved_candidates": approved,
        "suppressed_candidates": suppressed,
        "total": len(candidates)
    }
