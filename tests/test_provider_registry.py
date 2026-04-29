import pytest
from usa_signal_bot.data.provider_registry import ProviderRegistry, create_default_provider_registry
from usa_signal_bot.data.mock_provider import MockMarketDataProvider
from usa_signal_bot.core.exceptions import ProviderRegistrationError, ProviderNotFoundError, ForbiddenProviderError

def test_default_registry_contains_mock():
    registry = create_default_provider_registry()
    assert registry.has_provider("mock")
    assert registry.get("mock").name == "mock"

def test_duplicate_registration_fails():
    registry = ProviderRegistry()
    registry.register(MockMarketDataProvider())
    with pytest.raises(ProviderRegistrationError):
        registry.register(MockMarketDataProvider())

def test_unknown_provider_get_fails():
    registry = ProviderRegistry()
    with pytest.raises(ProviderNotFoundError):
        registry.get("unknown")

def test_unregister_works():
    registry = create_default_provider_registry()
    registry.unregister("mock")
    assert not registry.has_provider("mock")

def test_forbidden_provider_name_registration_fails():
    class BadProvider(MockMarketDataProvider):
        @property
        def name(self):
            return "alpaca"

    registry = ProviderRegistry()
    with pytest.raises(ForbiddenProviderError):
        registry.register(BadProvider())
