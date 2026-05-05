import pytest
from usa_signal_bot.portfolio.portfolio_models import (
    PortfolioCandidate, AllocationRequest, AllocationResult, PortfolioBasket,
    PortfolioConstructionResult, validate_portfolio_candidate,
    validate_allocation_request, validate_allocation_result, validate_portfolio_basket,
    create_allocation_request_id
)
from usa_signal_bot.core.enums import SignalAction, PortfolioCandidateStatus, AllocationMethod, AllocationStatus, PortfolioReviewStatus, PortfolioConstructionStatus
from usa_signal_bot.core.exceptions import PortfolioCandidateError, PortfolioValidationError

def test_portfolio_candidate_validation():
    c = PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 10, 1000)
    validate_portfolio_candidate(c)

    with pytest.raises(PortfolioCandidateError):
        validate_portfolio_candidate(PortfolioCandidate("", "AAPL", "1d", SignalAction.LONG, 10, 1000))

    with pytest.raises(PortfolioCandidateError):
        validate_portfolio_candidate(PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, -10, 1000))

def test_allocation_request_validation():
    r = AllocationRequest("r1", [], 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    validate_allocation_request(r)

    with pytest.raises(PortfolioValidationError):
        validate_allocation_request(AllocationRequest("", [], 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc"))

    with pytest.raises(PortfolioValidationError):
        validate_allocation_request(AllocationRequest("r1", [], 0, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc"))

def test_allocation_result_validation():
    r = AllocationResult("1", "AAPL", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.1, 1000, 10, 0.1, 1000, False, [], [], [])
    validate_allocation_result(r)

    with pytest.raises(PortfolioValidationError):
        validate_allocation_result(AllocationResult("", "AAPL", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.1, 1000, 10, 0.1, 1000, False, [], [], []))

def test_portfolio_basket_validation():
    b = PortfolioBasket("b1", "utc", AllocationMethod.EQUAL_WEIGHT, 100000, 100000, [], [], 1000, 0.1, 99000, PortfolioReviewStatus.ACCEPTABLE, [], [])
    validate_portfolio_basket(b)

    with pytest.raises(PortfolioValidationError):
        validate_portfolio_basket(PortfolioBasket("", "utc", AllocationMethod.EQUAL_WEIGHT, 100000, 100000, [], [], 1000, 0.1, 99000, PortfolioReviewStatus.ACCEPTABLE, [], []))
