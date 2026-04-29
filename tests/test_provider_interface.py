import pytest
from usa_signal_bot.data.provider_interface import MarketDataProvider
from usa_signal_bot.data.mock_provider import MockMarketDataProvider
from usa_signal_bot.data.provider_capabilities import ProviderCapability

def test_interface_is_abstract():
    with pytest.raises(TypeError):
        MarketDataProvider()

def test_mock_provider_implements_interface():
    provider = MockMarketDataProvider()
    assert provider.name == "mock"

def test_assert_no_scraping_passes():
    provider = MockMarketDataProvider()
    provider.assert_no_scraping()

def test_assert_free_provider_passes():
    provider = MockMarketDataProvider()
    provider.assert_free_provider()
