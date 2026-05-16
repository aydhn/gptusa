import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/walk_forward_adapter.py ---
wf_ad_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionReview
from typing import Any

def attach_portfolio_construction_to_walk_forward_result(result: dict[str, Any], reviews_by_window: dict[str, PortfolioConstructionReview] | None = None) -> dict[str, Any]:
    res = dict(result)
    res["portfolio_construction"] = {}
    if reviews_by_window:
        for w, r in reviews_by_window.items():
            if r.plan and r.plan.exposure_snapshot:
                res["portfolio_construction"][w] = {
                    "gross": r.plan.exposure_snapshot.gross_exposure_usd,
                    "net": r.plan.exposure_snapshot.net_exposure_usd
                }
    return res

def walk_forward_portfolio_construction_summary(result: dict[str, Any]) -> dict[str, Any]:
    return result.get("portfolio_construction", {})

def walk_forward_exposure_stability(result: dict[str, Any]) -> dict[str, Any]:
    pc = result.get("portfolio_construction", {})
    if not pc: return {"stability": "UNKNOWN"}
    grosses = [v.get("gross", 0) for v in pc.values()]
    if not grosses: return {"stability": "UNKNOWN"}

    max_g = max(grosses)
    min_g = min(grosses)
    return {
        "stability": "STABLE" if (max_g - min_g) / (max_g + 1) < 0.2 else "UNSTABLE",
        "max_gross": max_g,
        "min_gross": min_g
    }

def walk_forward_portfolio_construction_warnings(result: dict[str, Any]) -> list[str]:
    stab = walk_forward_exposure_stability(result)
    if stab.get("stability") == "UNSTABLE":
        return ["Walk-forward portfolio exposure is unstable across windows."]
    return []
"""
write_file("usa_signal_bot/portfolio_construction/walk_forward_adapter.py", wf_ad_code)


# --- portfolio_construction/paper_adapter.py ---
pa_ad_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionPlan, PortfolioAllocation
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
"""
write_file("usa_signal_bot/portfolio_construction/paper_adapter.py", pa_ad_code)


# --- portfolio_construction/allocation_adapter.py ---
al_ad_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioConstructionPlan, PortfolioAllocation
from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
from usa_signal_bot.portfolio_construction.portfolio_balancer import PortfolioBalancer
from typing import Any

def portfolio_candidate_from_position_size_result(result: Any, source_payload: dict[str, Any] | None = None) -> PortfolioCandidate:
    # Handle object or dict
    if isinstance(result, dict):
        sym = result.get("symbol", "UNKNOWN")
        notional = result.get("final_notional_usd")
        quant = result.get("final_quantity")
        conf = result.get("confidence")
    else:
        sym = getattr(result, "symbol", "UNKNOWN")
        notional = getattr(result, "final_notional_usd", None)
        quant = getattr(result, "final_quantity", None)
        conf = getattr(result, "confidence", None)

    src = source_payload or {}
    planner = PortfolioAllocationPlanner()
    return planner.build_candidates([{
        "symbol": sym,
        "final_notional_usd": notional,
        "final_quantity": quant,
        "confidence": conf,
        "sector": src.get("sector"),
        "cluster": src.get("cluster")
    }])[0]

def adjust_position_size_result_with_portfolio_allocation(size_result_payload: dict[str, Any], allocation: PortfolioAllocation) -> dict[str, Any]:
    res = dict(size_result_payload)
    if allocation.final_notional_usd is not None:
        res["final_notional_usd"] = allocation.final_notional_usd
    if allocation.final_quantity is not None:
        res["final_quantity"] = allocation.final_quantity
    res["portfolio_status"] = allocation.status.value if hasattr(allocation.status, 'value') else str(allocation.status)
    return res

def portfolio_plan_from_sizing_results(size_results: list[Any], total_equity_usd: float | None = None) -> PortfolioConstructionPlan:
    cands = [portfolio_candidate_from_position_size_result(r) for r in size_results]
    balancer = PortfolioBalancer()
    return balancer.build_plan(cands, total_equity_usd)

def allocation_adapter_summary_to_text(payload: dict[str, Any]) -> str:
    return f"Allocation Adapter: {payload.get('portfolio_status', 'UNKNOWN')} -> ${payload.get('final_notional_usd', 0):.2f}"
"""
write_file("usa_signal_bot/portfolio_construction/allocation_adapter.py", al_ad_code)


# --- portfolio_construction/risk_adapter.py ---
risk_ad_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionPlan
from typing import Any

def portfolio_construction_risk_summary(plan: PortfolioConstructionPlan) -> dict[str, Any]:
    if not plan.exposure_snapshot: return {}
    return {
        "gross_exposure_usd": plan.exposure_snapshot.gross_exposure_usd,
        "net_exposure_usd": plan.exposure_snapshot.net_exposure_usd,
        "long_exposure_usd": plan.exposure_snapshot.long_exposure_usd,
        "short_exposure_usd": plan.exposure_snapshot.short_exposure_usd,
        "concentration_assessments": len(plan.concentration_assessments),
        "blocked_allocations": plan.blocked_count + plan.suppressed_count
    }

def portfolio_construction_risk_warnings(plan: PortfolioConstructionPlan) -> list[str]:
    warns = []
    for a in plan.concentration_assessments:
        warns.extend(a.warnings)
    return warns

def attach_portfolio_construction_to_risk_report(report: dict[str, Any], plan: PortfolioConstructionPlan) -> dict[str, Any]:
    res = dict(report)
    res["portfolio_risk"] = portfolio_construction_risk_summary(plan)
    res["portfolio_warnings"] = portfolio_construction_risk_warnings(plan)
    return res

def risk_adapter_summary_to_text(payload: dict[str, Any]) -> str:
    risk = payload.get("portfolio_risk", {})
    return f"Portfolio Risk: Gross ${risk.get('gross_exposure_usd', 0):.2f}, Blocked: {risk.get('blocked_allocations', 0)}"
"""
write_file("usa_signal_bot/portfolio_construction/risk_adapter.py", risk_ad_code)

print("Generated step 8")
