from usa_signal_bot.portfolio.allocation_methods import (
    allocate_equal_weight, allocate_rank_weighted, allocate_risk_score_weighted,
    allocate_volatility_adjusted, allocate_from_risk_decision_notional,
    AllocationConfig, default_allocation_config
)
from usa_signal_bot.portfolio.portfolio_models import AllocationRequest, PortfolioCandidate
from usa_signal_bot.core.enums import SignalAction, AllocationMethod, PortfolioCandidateStatus

def test_equal_weight():
    candidates = [
        PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 0, 0, price=100, status=PortfolioCandidateStatus.ELIGIBLE),
        PortfolioCandidate("2", "MSFT", "1d", SignalAction.LONG, 0, 0, price=200, status=PortfolioCandidateStatus.ELIGIBLE)
    ]
    req = AllocationRequest("r1", candidates, 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    config = default_allocation_config()
    config.max_candidate_weight = 1.0
    res = allocate_equal_weight(req, config)

    assert len(res) == 2
    assert res[0].target_weight == 0.4
    assert res[1].target_weight == 0.4

def test_rank_weighted():
    candidates = [
        PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 0, 0, price=100, rank_score=20, status=PortfolioCandidateStatus.ELIGIBLE),
        PortfolioCandidate("2", "MSFT", "1d", SignalAction.LONG, 0, 0, price=200, rank_score=80, status=PortfolioCandidateStatus.ELIGIBLE)
    ]
    req = AllocationRequest("r1", candidates, 100000, 100000, AllocationMethod.RANK_WEIGHTED, 0.8, "utc")
    config = default_allocation_config()
    config.max_candidate_weight = 1.0
    res = allocate_rank_weighted(req, config)

    assert len(res) == 2
    # AAPL = 20/100 * 0.8 = 0.16, MSFT = 80/100 * 0.8 = 0.64
    assert round(res[0].target_weight, 2) == 0.16
    assert round(res[1].target_weight, 2) == 0.64

def test_missing_price():
    candidates = [
        PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 0, 0, price=None, status=PortfolioCandidateStatus.ELIGIBLE)
    ]
    req = AllocationRequest("r1", candidates, 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    config = default_allocation_config()
    config.max_candidate_weight = 1.0
    res = allocate_equal_weight(req, config)
    assert res[0].target_weight == 0
    assert len(res[0].warnings) > 0
