import pytest
from unittest.mock import patch, MagicMock
from usa_signal_bot.portfolio.portfolio_models import AllocationRequest, validate_allocation_request
from usa_signal_bot.core.exceptions import PortfolioValidationError

class DummyEnum:
    def __init__(self, value):
        self.value = value

def test_validate_allocation_request_valid():
    request = AllocationRequest(
        request_id="req_123",
        candidates=[],
        portfolio_equity=10000.0,
        available_cash=5000.0,
        method=DummyEnum("EQUAL_WEIGHT"),
        max_total_allocation_pct=0.8,
        created_at_utc="2023-01-01T00:00:00Z"
    )
    # Should not raise any exception
    validate_allocation_request(request)

def test_validate_allocation_request_empty_request_id():
    request = AllocationRequest(
        request_id="",
        candidates=[],
        portfolio_equity=10000.0,
        available_cash=5000.0,
        method=DummyEnum("EQUAL_WEIGHT"),
        max_total_allocation_pct=0.8,
        created_at_utc="2023-01-01T00:00:00Z"
    )
    with pytest.raises(PortfolioValidationError, match="request_id is empty."):
        validate_allocation_request(request)

def test_validate_allocation_request_non_positive_equity():
    request = AllocationRequest(
        request_id="req_123",
        candidates=[],
        portfolio_equity=0.0,
        available_cash=5000.0,
        method=DummyEnum("EQUAL_WEIGHT"),
        max_total_allocation_pct=0.8,
        created_at_utc="2023-01-01T00:00:00Z"
    )
    with pytest.raises(PortfolioValidationError, match="portfolio_equity must be greater than 0."):
        validate_allocation_request(request)

    request.portfolio_equity = -100.0
    with pytest.raises(PortfolioValidationError, match="portfolio_equity must be greater than 0."):
        validate_allocation_request(request)

def test_validate_allocation_request_negative_available_cash():
    request = AllocationRequest(
        request_id="req_123",
        candidates=[],
        portfolio_equity=10000.0,
        available_cash=-1.0,
        method=DummyEnum("EQUAL_WEIGHT"),
        max_total_allocation_pct=0.8,
        created_at_utc="2023-01-01T00:00:00Z"
    )
    with pytest.raises(PortfolioValidationError, match="available_cash cannot be negative."):
        validate_allocation_request(request)

def test_validate_allocation_request_out_of_bounds_max_allocation_pct():
    # Test < 0
    request = AllocationRequest(
        request_id="req_123",
        candidates=[],
        portfolio_equity=10000.0,
        available_cash=5000.0,
        method=DummyEnum("EQUAL_WEIGHT"),
        max_total_allocation_pct=-0.1,
        created_at_utc="2023-01-01T00:00:00Z"
    )
    with pytest.raises(PortfolioValidationError, match="max_total_allocation_pct must be between 0 and 1."):
        validate_allocation_request(request)

    # Test > 1
    request.max_total_allocation_pct = 1.1
    with pytest.raises(PortfolioValidationError, match="max_total_allocation_pct must be between 0 and 1."):
        validate_allocation_request(request)
