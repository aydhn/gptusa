import pytest
from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord, PortfolioCandidate, validate_sector_cluster_record
from usa_signal_bot.core.enums import SectorClusterSource

def test_sector_cluster_record_valid():
    rec = SectorClusterRecord("id1", "AAPL", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0)
    assert rec.symbol == "AAPL"

def test_sector_cluster_record_invalid():
    rec = SectorClusterRecord("id1", "", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0)
    with pytest.raises(ValueError):
        validate_sector_cluster_record(rec)


from usa_signal_bot.portfolio.portfolio_models import PortfolioBasket, validate_portfolio_basket

def test_validate_portfolio_basket_valid():
    from unittest.mock import MagicMock
    basket = MagicMock()
    basket.basket_id = "b1"
    basket.portfolio_equity = 100.0
    basket.available_cash = 50.0
    basket.total_target_notional = 80.0
    basket.total_target_weight = 0.8
    # Should not raise
    validate_portfolio_basket(basket)

def test_validate_portfolio_basket_empty_id():
    from unittest.mock import MagicMock
    basket = MagicMock()
    basket.basket_id = ""
    basket.portfolio_equity = 100.0
    basket.available_cash = 50.0
    basket.total_target_notional = 80.0
    basket.total_target_weight = 0.8
    with pytest.raises(Exception, match="basket_id is empty"):
        validate_portfolio_basket(basket)

def test_validate_portfolio_basket_negative_equity():
    from unittest.mock import MagicMock
    basket = MagicMock()
    basket.basket_id = "b1"
    basket.portfolio_equity = -10.0
    basket.available_cash = 50.0
    basket.total_target_notional = 80.0
    basket.total_target_weight = 0.8
    with pytest.raises(Exception, match="portfolio_equity must be greater than 0"):
        validate_portfolio_basket(basket)

def test_validate_portfolio_basket_zero_equity():
    from unittest.mock import MagicMock
    basket = MagicMock()
    basket.basket_id = "b1"
    basket.portfolio_equity = 0.0
    basket.available_cash = 50.0
    basket.total_target_notional = 80.0
    basket.total_target_weight = 0.8
    with pytest.raises(Exception, match="portfolio_equity must be greater than 0"):
        validate_portfolio_basket(basket)

def test_validate_portfolio_basket_negative_cash():
    from unittest.mock import MagicMock
    basket = MagicMock()
    basket.basket_id = "b1"
    basket.portfolio_equity = 100.0
    basket.available_cash = -10.0
    basket.total_target_notional = 80.0
    basket.total_target_weight = 0.8
    with pytest.raises(Exception, match="available_cash cannot be negative"):
        validate_portfolio_basket(basket)

def test_validate_portfolio_basket_negative_notional():
    from unittest.mock import MagicMock
    basket = MagicMock()
    basket.basket_id = "b1"
    basket.portfolio_equity = 100.0
    basket.available_cash = 50.0
    basket.total_target_notional = -10.0
    basket.total_target_weight = 0.8
    with pytest.raises(Exception, match="total_target_notional cannot be negative"):
        validate_portfolio_basket(basket)

def test_validate_portfolio_basket_negative_weight():
    from unittest.mock import MagicMock
    basket = MagicMock()
    basket.basket_id = "b1"
    basket.portfolio_equity = 100.0
    basket.available_cash = 50.0
    basket.total_target_notional = 80.0
    basket.total_target_weight = -10.0
    with pytest.raises(Exception, match="total_target_weight cannot be negative"):
        validate_portfolio_basket(basket)

from usa_signal_bot.portfolio.portfolio_models import AllocationResult, validate_allocation_result
from usa_signal_bot.core.exceptions import PortfolioValidationError

class DummyEnum:
    def __init__(self, value):
        self.value = value

def test_validate_allocation_result_valid():
    result = AllocationResult(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=0.1,
        target_notional=100.0,
        target_quantity=1.0,
        raw_weight=0.15,
        raw_notional=150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    validate_allocation_result(result)

def test_validate_allocation_result_empty_candidate_id():
    result = AllocationResult(
        candidate_id="",
        symbol="AAPL",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=0.1,
        target_notional=100.0,
        target_quantity=1.0,
        raw_weight=0.15,
        raw_notional=150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(PortfolioValidationError, match="candidate_id is empty."):
        validate_allocation_result(result)

def test_validate_allocation_result_empty_symbol():
    result = AllocationResult(
        candidate_id="c1",
        symbol="",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=0.1,
        target_notional=100.0,
        target_quantity=1.0,
        raw_weight=0.15,
        raw_notional=150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(PortfolioValidationError, match="symbol is empty."):
        validate_allocation_result(result)

def test_validate_allocation_result_negative_target_weight():
    result = AllocationResult(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=-0.1,
        target_notional=100.0,
        target_quantity=1.0,
        raw_weight=0.15,
        raw_notional=150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(PortfolioValidationError, match="target_weight cannot be negative."):
        validate_allocation_result(result)

def test_validate_allocation_result_negative_target_notional():
    result = AllocationResult(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=0.1,
        target_notional=-100.0,
        target_quantity=1.0,
        raw_weight=0.15,
        raw_notional=150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(PortfolioValidationError, match="target_notional cannot be negative."):
        validate_allocation_result(result)

def test_validate_allocation_result_negative_target_quantity():
    result = AllocationResult(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=0.1,
        target_notional=100.0,
        target_quantity=-1.0,
        raw_weight=0.15,
        raw_notional=150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(PortfolioValidationError, match="target_quantity cannot be negative."):
        validate_allocation_result(result)

def test_validate_allocation_result_negative_raw_weight():
    result = AllocationResult(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=0.1,
        target_notional=100.0,
        target_quantity=1.0,
        raw_weight=-0.15,
        raw_notional=150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(PortfolioValidationError, match="raw_weight cannot be negative."):
        validate_allocation_result(result)

def test_validate_allocation_result_negative_raw_notional():
    result = AllocationResult(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1D",
        method=DummyEnum("EQUAL_WEIGHT"),
        status=DummyEnum("APPROVED"),
        target_weight=0.1,
        target_notional=100.0,
        target_quantity=1.0,
        raw_weight=0.15,
        raw_notional=-150.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(PortfolioValidationError, match="raw_notional cannot be negative."):
        validate_allocation_result(result)
