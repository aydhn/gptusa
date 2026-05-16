from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioConstructionPlan, PortfolioAllocation
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
