import pytest
from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioAllocation, PortfolioConstructionPlan
from usa_signal_bot.core.enums import PortfolioAllocationStatus, PortfolioConstructionMode

def test_candidate_adapter():
    from usa_signal_bot.portfolio_construction.candidate_adapter import portfolio_candidate_from_candidate, attach_portfolio_allocation_to_candidate
    cand = {"symbol": "AAPL", "score": 80}
    p_cand = portfolio_candidate_from_candidate(cand)
    assert p_cand.symbol == "AAPL"

    alloc = PortfolioAllocation("a1", "AAPL", None, "LONG", 100, 100, 1, 10.0, PortfolioAllocationStatus.APPROVED, [], [], [], [])
    res = attach_portfolio_allocation_to_candidate(cand, alloc)
    assert res["portfolio_allocation_status"] == "APPROVED"

def test_signal_adapter():
    from usa_signal_bot.portfolio_construction.signal_adapter import portfolio_candidate_from_signal, attach_portfolio_allocation_to_signal
    sig = {"symbol": "MSFT", "side": "LONG"}
    p_cand = portfolio_candidate_from_signal(sig)
    assert p_cand.symbol == "MSFT"

    alloc = PortfolioAllocation("a2", "MSFT", None, "LONG", 100, 100, 1, 10.0, PortfolioAllocationStatus.SUPPRESSED, [], [], [], [])
    res = attach_portfolio_allocation_to_signal(sig, alloc)
    assert res["portfolio_allocation_status"] == "SUPPRESSED"

def test_backtest_adapter():
    from usa_signal_bot.portfolio_construction.backtest_adapter import attach_portfolio_construction_to_backtest_result
    from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionReview, ExposureSnapshot

    snap = ExposureSnapshot("s1", "time", 1000, 500, 500, 500, 0, {}, {}, {}, {}, {}, {}, {}, [], [], {})
    plan = PortfolioConstructionPlan("p1", "time", PortfolioConstructionMode.HYBRID, [], [], snap, [], [], 0, 0, 0, 0, 0, 0, [], [], {})
    review = PortfolioConstructionReview("r1", "time", "ALLOCATION_PLAN", plan, snap, [], [], {}, [], [])

    res = attach_portfolio_construction_to_backtest_result({"trades": []}, review)
    assert res["portfolio_gross_exposure_usd"] == 500

def test_paper_adapter():
    from usa_signal_bot.portfolio_construction.paper_adapter import paper_order_allowed_by_portfolio_allocation
    alloc = PortfolioAllocation("a1", "AAPL", None, "LONG", 100, 100, 1, 10.0, PortfolioAllocationStatus.BLOCKED, [], [], [], [])
    assert not paper_order_allowed_by_portfolio_allocation(alloc)

def test_allocation_adapter():
    from usa_signal_bot.portfolio_construction.allocation_adapter import adjust_position_size_result_with_portfolio_allocation
    alloc = PortfolioAllocation("a1", "AAPL", None, "LONG", 100, 100, 1, 10.0, PortfolioAllocationStatus.APPROVED, [], [], [], [])
    res = adjust_position_size_result_with_portfolio_allocation({"final_notional_usd": 200}, alloc)
    assert res["final_notional_usd"] == 100

def test_risk_adapter():
    from usa_signal_bot.portfolio_construction.risk_adapter import portfolio_construction_risk_summary
    from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot
    snap = ExposureSnapshot("s1", "time", 1000, 500, 500, 500, 0, {}, {}, {}, {}, {}, {}, {}, [], [], {})
    plan = PortfolioConstructionPlan("p1", "time", PortfolioConstructionMode.HYBRID, [], [], snap, [], [], 0, 0, 0, 0, 0, 0, [], [], {})
    res = portfolio_construction_risk_summary(plan)
    assert res["gross_exposure_usd"] == 500
