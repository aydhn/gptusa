import pytest
from usa_signal_bot.data.provider_capabilities import ProviderCapability
from usa_signal_bot.data.models import MarketDataRequest
from usa_signal_bot.core.exceptions import (
    ProviderCapabilityError, ForbiddenProviderError, ProviderRequestError
)
from usa_signal_bot.data.provider_guards import (
    assert_provider_is_free, assert_provider_does_not_scrape,
    assert_provider_requires_no_paid_api, assert_no_forbidden_provider_name,
    assert_request_is_safe
)

def test_paid_provider_capability_fails():
    cap = ProviderCapability(provider_name="test", free_only=False)
    with pytest.raises(ProviderCapabilityError):
        assert_provider_is_free(cap)

def test_scraping_provider_capability_fails():
    cap = ProviderCapability(provider_name="test", allows_scraping=True)
    with pytest.raises(ProviderCapabilityError):
        assert_provider_does_not_scrape(cap)

def test_forbidden_provider_name_fails():
    with pytest.raises(ForbiddenProviderError):
        assert_no_forbidden_provider_name("alpaca")
    with pytest.raises(ForbiddenProviderError):
        assert_no_forbidden_provider_name("ibkr")

def test_yfinance_is_not_forbidden():
    assert_no_forbidden_provider_name("yfinance")

def test_safe_request_passes():
    req = MarketDataRequest(symbols=["AAPL"], provider_name="mock", timeframe="1d")
    assert_request_is_safe(req)

def test_empty_symbols_fails():
    with pytest.raises(ValueError):
        MarketDataRequest(symbols=[], provider_name="mock", timeframe="1d")
