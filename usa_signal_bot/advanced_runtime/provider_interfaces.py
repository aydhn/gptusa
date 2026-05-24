from typing import Protocol, Any
from usa_signal_bot.advanced_runtime.phase102_models import (
    ProviderDataRequest, ProviderDataResponse, ProviderCapabilityManifest, ProviderSafetyManifest,
    ProviderInterfaceKind
)

class BaseProviderInterface(Protocol):
    @property
    def provider_name(self) -> str:
        ...

    @property
    def interface_kind(self) -> ProviderInterfaceKind:
        ...

    def capability_manifest(self) -> ProviderCapabilityManifest:
        ...

    def safety_manifest(self) -> ProviderSafetyManifest:
        ...

    def validate_request(self, request: ProviderDataRequest) -> list[str]:
        ...

    def execute_metadata_only(self, request: ProviderDataRequest) -> ProviderDataResponse:
        ...

class MarketDataProviderInterface(BaseProviderInterface, Protocol):
    def get_daily_bars_request(self, symbol: str, start_date: str, end_date: str) -> ProviderDataResponse:
        ...

    def get_intraday_bars_request(self, symbol: str, start_date: str, end_date: str) -> ProviderDataResponse:
        ...

    def get_provider_status_request(self) -> ProviderDataResponse:
        ...

class FundamentalDataProviderInterface(BaseProviderInterface, Protocol):
    pass

class MacroDataProviderInterface(BaseProviderInterface, Protocol):
    pass

class CalendarDataProviderInterface(BaseProviderInterface, Protocol):
    pass

class NewsMetadataProviderInterface(BaseProviderInterface, Protocol):
    pass

class SymbolUniverseProviderInterface(BaseProviderInterface, Protocol):
    pass
