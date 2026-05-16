import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/candidate_adapter.py ---
cand_ad_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioAllocation, PortfolioConstructionPlan
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
"""
write_file("usa_signal_bot/portfolio_construction/candidate_adapter.py", cand_ad_code)


# --- portfolio_construction/signal_adapter.py ---
sig_ad_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioAllocation, PortfolioConstructionPlan
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
"""
write_file("usa_signal_bot/portfolio_construction/signal_adapter.py", sig_ad_code)


# --- portfolio_construction/backtest_adapter.py ---
bt_ad_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionReview, PortfolioConstructionPlan
from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
from typing import Any

def attach_portfolio_construction_to_backtest_result(result: dict[str, Any], review: PortfolioConstructionReview | None = None) -> dict[str, Any]:
    res = dict(result)
    if review and review.plan and review.plan.exposure_snapshot:
        res["portfolio_gross_exposure_usd"] = review.plan.exposure_snapshot.gross_exposure_usd
        res["portfolio_net_exposure_usd"] = review.plan.exposure_snapshot.net_exposure_usd
    return res

def build_portfolio_plan_from_backtest_trades(trades: list[dict[str, Any]], total_equity_usd: float | None = None) -> PortfolioConstructionPlan:
    planner = PortfolioAllocationPlanner()
    cands = planner.build_candidates(trades)
    from usa_signal_bot.portfolio_construction.portfolio_balancer import PortfolioBalancer
    balancer = PortfolioBalancer()
    return balancer.build_plan(cands, total_equity_usd)

def backtest_portfolio_construction_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "portfolio_gross_exposure_usd": result.get("portfolio_gross_exposure_usd"),
        "portfolio_net_exposure_usd": result.get("portfolio_net_exposure_usd"),
    }

def backtest_portfolio_construction_warnings(result: dict[str, Any]) -> list[str]:
    return []
"""
write_file("usa_signal_bot/portfolio_construction/backtest_adapter.py", bt_ad_code)

print("Generated step 7")
