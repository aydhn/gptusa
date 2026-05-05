import pytest
from usa_signal_bot.portfolio.portfolio_validation import (
    validate_allocation_request_report, validate_allocation_results_report,
    validate_portfolio_basket_report, validate_no_portfolio_optimizer_behavior,
    validate_no_broker_execution_in_portfolio, validate_portfolio_construction_result,
    assert_portfolio_valid
)
from usa_signal_bot.portfolio.portfolio_models import AllocationRequest, AllocationResult, PortfolioBasket, PortfolioConstructionResult
from usa_signal_bot.core.enums import AllocationMethod, AllocationStatus, PortfolioReviewStatus, PortfolioConstructionStatus
from usa_signal_bot.core.exceptions import PortfolioValidationError

def test_validate_request():
    req = AllocationRequest("r1", [], -10, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    rep = validate_allocation_request_report(req)
    assert not rep.valid
    assert rep.error_count > 0

def test_validate_allocations():
    a = AllocationResult("1", "AAPL", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.1, -100, 10, 0.1, 100, False, [], [], [])
    rep = validate_allocation_results_report([a])
    assert not rep.valid
    assert rep.error_count > 0

def test_validate_no_optimizer():
    req = AllocationRequest("r1", [], 100, 100, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    res = PortfolioConstructionResult("run", "utc", PortfolioConstructionStatus.COMPLETED, req, {}, {}, [], [], [], [])
    res.output_paths = {"optimal_weights": "fake.json"} # Inject banned term

    rep = validate_no_portfolio_optimizer_behavior(res)
    assert not rep.valid

def test_validate_no_broker():
    req = AllocationRequest("r1", [], 100, 100, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    res = PortfolioConstructionResult("run", "utc", PortfolioConstructionStatus.COMPLETED, req, {}, {}, [], [], [], [])
    res.output_paths = {"broker_order": "fake.json"} # Inject banned term

    rep = validate_no_broker_execution_in_portfolio(res)
    assert not rep.valid

def test_assert_valid():
    req = AllocationRequest("r1", [], 100, 100, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    res = PortfolioConstructionResult("run", "utc", PortfolioConstructionStatus.COMPLETED, req, {}, {}, [], [], [], [])

    rep = validate_portfolio_construction_result(res)
    assert_portfolio_valid(rep)
