from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioAllocation, PortfolioConstructionPlan
from usa_signal_bot.portfolio_construction.sector_cluster_resolver import SectorClusterResolver
from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
from usa_signal_bot.core.enums import PortfolioAllocationStatus
from typing import Any

def portfolio_candidate_from_signal(signal: dict[str, Any], resolver: SectorClusterResolver | None = None) -> PortfolioCandidate:
    planner = PortfolioAllocationPlanner()
    return planner.build_candidates([signal], resolver)[0]

def attach_portfolio_allocation_to_signal(signal: dict[str, Any], allocation: PortfolioAllocation) -> dict[str, Any]:
    res = dict(signal)
    res["portfolio_final_notional_usd"] = allocation.final_notional_usd
    res["portfolio_final_quantity"] = allocation.final_quantity
    res["portfolio_weight_pct_equity"] = allocation.weight_pct_equity
    res["portfolio_allocation_status"] = allocation.status.value if hasattr(allocation.status, 'value') else str(allocation.status)
    return res

def apply_portfolio_plan_to_signals(signals: list[dict[str, Any]], plan: PortfolioConstructionPlan) -> list[dict[str, Any]]:
    alloc_map = {a.symbol: a for a in plan.allocations}
    res = []
    for s in signals:
        sym = s.get("symbol")
        if sym in alloc_map:
            res.append(attach_portfolio_allocation_to_signal(s, alloc_map[sym]))
        else:
            res.append(s)
    return res

def suppress_signal_if_portfolio_blocked(signal: dict[str, Any], allocation: PortfolioAllocation) -> dict[str, Any]:
    res = attach_portfolio_allocation_to_signal(signal, allocation)
    if allocation.status in [PortfolioAllocationStatus.BLOCKED, PortfolioAllocationStatus.SUPPRESSED]:
        res["is_suppressed"] = True
        res["suppress_reason"] = "Blocked by portfolio construction guards"
    return res

def signal_portfolio_summary(signals: list[dict[str, Any]]) -> dict[str, Any]:
    approved = sum(1 for s in signals if s.get("portfolio_allocation_status") == "APPROVED")
    return {
        "approved_signals": approved,
        "total": len(signals)
    }
