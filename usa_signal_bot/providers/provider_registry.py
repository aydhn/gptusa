from typing import Optional
from pathlib import Path

from usa_signal_bot.core.enums import DataProviderName
from usa_signal_bot.providers.provider_models import ProviderRequest, ProviderCapabilityProfile
from usa_signal_bot.providers.provider_interface import BaseDataProvider

class ProviderRegistryError(Exception):
    pass

class ProviderRegistry:
    def __init__(self, providers: Optional[list[BaseDataProvider]] = None):
        self._providers: dict[DataProviderName, BaseDataProvider] = {}
        if providers:
            for p in providers:
                self.register(p)

    def register(self, provider: BaseDataProvider) -> None:
        if not isinstance(provider, BaseDataProvider):
            raise TypeError("Provider must inherit from BaseDataProvider")
        self._providers[provider.name()] = provider

    def unregister(self, name: DataProviderName) -> None:
        if name in self._providers:
            del self._providers[name]

    def get(self, name: DataProviderName) -> Optional[BaseDataProvider]:
        return self._providers.get(name)

    def list_providers(self) -> list[BaseDataProvider]:
        return list(self._providers.values())

    def providers_supporting(self, request: ProviderRequest) -> list[BaseDataProvider]:
        return [p for p in self._providers.values() if p.supports(request)]

    def capability_profiles(self) -> list[ProviderCapabilityProfile]:
        return [p.capability_profile() for p in self._providers.values()]

def build_default_provider_registry(data_root: Path, allow_network: bool = True) -> ProviderRegistry:
    from usa_signal_bot.providers.yfinance_provider import YFinanceDataProvider
    from usa_signal_bot.providers.local_cache_provider import LocalCacheDataProvider
    from usa_signal_bot.providers.local_fixture_provider import LocalFixtureDataProvider
    from usa_signal_bot.providers.manual_file_provider import ManualFileDataProvider

    registry = ProviderRegistry()
    registry.register(LocalCacheDataProvider(cache_root=data_root / "cache"))
    registry.register(YFinanceDataProvider(cache_dir=data_root / "cache", allow_network=allow_network))
    registry.register(ManualFileDataProvider(manual_data_root=data_root / "manual"))
    registry.register(LocalFixtureDataProvider(fixture_root=data_root / "regression" / "golden"))
    return registry
