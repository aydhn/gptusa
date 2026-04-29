from typing import Dict, List
from usa_signal_bot.data.provider_interface import MarketDataProvider
from usa_signal_bot.data.provider_capabilities import ProviderCapability, validate_provider_capability
from usa_signal_bot.data.provider_guards import assert_no_forbidden_provider_name
from usa_signal_bot.core.exceptions import ProviderRegistrationError, ProviderNotFoundError
from usa_signal_bot.data.mock_provider import MockMarketDataProvider
from usa_signal_bot.data.yfinance_provider import YFinanceMarketDataProvider

class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, MarketDataProvider] = {}

    def register(self, provider: MarketDataProvider) -> None:
        name = provider.name
        assert_no_forbidden_provider_name(name)
        validate_provider_capability(provider.capability)

        if name in self._providers:
            raise ProviderRegistrationError(f"Provider '{name}' is already registered.")

        self._providers[name] = provider

    def get(self, name: str) -> MarketDataProvider:
        if name not in self._providers:
            raise ProviderNotFoundError(f"Provider '{name}' not found in registry.")
        return self._providers[name]

    def list_names(self) -> List[str]:
        return list(self._providers.keys())

    def list_capabilities(self) -> List[ProviderCapability]:
        return [p.capability for p in self._providers.values()]

    def has_provider(self, name: str) -> bool:
        return name in self._providers

    def unregister(self, name: str) -> None:
        if name in self._providers:
            del self._providers[name]

def create_default_provider_registry(include_yfinance: bool = True) -> ProviderRegistry:
    registry = ProviderRegistry()
    return register_default_providers(registry, include_yfinance=include_yfinance)

def register_default_providers(registry: ProviderRegistry, include_yfinance: bool = True) -> ProviderRegistry:
    registry.register(MockMarketDataProvider())
    if include_yfinance:
        registry.register(YFinanceMarketDataProvider())
    return registry
