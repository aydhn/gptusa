from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionReview, PortfolioConstructionPlan
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
