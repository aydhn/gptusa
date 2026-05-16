from usa_signal_bot.portfolio_construction.portfolio_balancer import PortfolioBalancer
from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner

def test_balancer_build_plan():
    planner = PortfolioAllocationPlanner()
    cands = planner.build_candidates([{"symbol": "AAPL"}])
    balancer = PortfolioBalancer()
    plan = balancer.build_plan(cands, 1000)
    assert plan.approved_count == 1
    assert plan.total_allocated_notional_usd > 0
