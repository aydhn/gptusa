from usa_signal_bot.portfolio.portfolio_engine import PortfolioConstructionEngine
from usa_signal_bot.portfolio.portfolio_models import AllocationRequest, PortfolioCandidate
from usa_signal_bot.core.enums import SignalAction, AllocationMethod, PortfolioCandidateStatus, PortfolioConstructionStatus

def test_portfolio_engine_empty():
    engine = PortfolioConstructionEngine()
    req = AllocationRequest("r1", [], 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    res = engine.construct_portfolio(req)

    assert res.status == PortfolioConstructionStatus.EMPTY
    assert len(res.approved_allocations) == 0

def test_portfolio_engine_valid():
    engine = PortfolioConstructionEngine()
    candidates = [
        PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 0, 0, price=100, status=PortfolioCandidateStatus.ELIGIBLE),
        PortfolioCandidate("2", "MSFT", "1d", SignalAction.LONG, 0, 0, price=200, status=PortfolioCandidateStatus.ELIGIBLE)
    ]
    req = AllocationRequest("r1", candidates, 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    res = engine.construct_portfolio(req)

    assert res.status == PortfolioConstructionStatus.COMPLETED
    assert len(res.approved_allocations) == 2
    assert res.basket is not None
    assert res.basket.portfolio_equity == 100000

def test_run_from_risk_decisions():
    engine = PortfolioConstructionEngine()
    # We tested the adapter in candidates tests, so here we can just supply an empty list and ensure it doesn't crash
    res = engine.run_from_risk_decisions([], 100000, 100000)
    assert res.status == PortfolioConstructionStatus.EMPTY
