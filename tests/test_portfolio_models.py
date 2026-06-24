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
