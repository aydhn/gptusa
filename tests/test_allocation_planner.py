from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
from usa_signal_bot.core.enums import PortfolioConstructionMode

def test_equal_weight():
    planner = PortfolioAllocationPlanner(mode=PortfolioConstructionMode.EQUAL_WEIGHT)
    cands = planner.build_candidates([{"symbol": "AAPL"}, {"symbol": "MSFT"}])
    allocs = planner.plan_allocations(cands, 1000)
    assert allocs[0].final_notional_usd == 500
    assert allocs[1].final_notional_usd == 500
