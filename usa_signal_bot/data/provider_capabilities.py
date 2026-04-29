from dataclasses import dataclass, field
from typing import List, Dict, Any
from usa_signal_bot.core.exceptions import ProviderCapabilityError

@dataclass
class ProviderCapability:
    provider_name: str = ""
    supports_daily: bool = False
    supports_intraday: bool = False
    supports_adjusted: bool = False
    supports_batch: bool = False
    supports_stocks: bool = False
    supports_etfs: bool = False
    supports_fundamentals: bool = False
    supports_options: bool = False
    free_only: bool = True
    requires_api_key: bool = False
    allows_scraping: bool = False
    notes: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.notes is None:
            self.notes = []

def validate_provider_capability(capability: ProviderCapability) -> None:
    if not capability.provider_name:
        raise ProviderCapabilityError("Provider capability requires a provider_name.")
    if not capability.free_only:
        raise ProviderCapabilityError("Provider capability 'free_only' must be true.")
    if capability.allows_scraping:
        raise ProviderCapabilityError("Provider capability 'allows_scraping' must be false.")
    if capability.requires_api_key:
        raise ProviderCapabilityError("Provider capability 'requires_api_key' must be false in Phase 7.")

def capability_to_dict(capability: ProviderCapability) -> dict:
    return {
        "provider_name": capability.provider_name,
        "supports_daily": capability.supports_daily,
        "supports_intraday": capability.supports_intraday,
        "supports_adjusted": capability.supports_adjusted,
        "supports_batch": capability.supports_batch,
        "supports_stocks": capability.supports_stocks,
        "supports_etfs": capability.supports_etfs,
        "supports_fundamentals": capability.supports_fundamentals,
        "supports_options": capability.supports_options,
        "free_only": capability.free_only,
        "requires_api_key": capability.requires_api_key,
        "allows_scraping": capability.allows_scraping,
        "notes": capability.notes.copy()
    }

def default_mock_provider_capability() -> ProviderCapability:
    return ProviderCapability(
        provider_name="mock",
        supports_daily=True,
        supports_intraday=True,
        supports_adjusted=True,
        supports_batch=True,
        supports_stocks=True,
        supports_etfs=True,
        supports_fundamentals=False,
        supports_options=False,
        free_only=True,
        requires_api_key=False,
        allows_scraping=False,
        notes=["Mock provider for testing purposes only."]
    )

def yfinance_provider_capability() -> ProviderCapability:
    return ProviderCapability(
        provider_name="yfinance",
        supports_daily=True,
        supports_intraday=True,
        supports_adjusted=True,
        supports_batch=True,
        supports_stocks=True,
        supports_etfs=True,
        supports_fundamentals=False,
        supports_options=False,
        free_only=True,
        requires_api_key=False,
        allows_scraping=False,
        notes=[
            "Free yfinance library based provider",
            "Data availability and limits depend on Yahoo Finance/yfinance behavior",
            "No broker routing",
            "No direct HTML scraping in project code"
        ]
    )

def reserved_yfinance_provider_capability() -> ProviderCapability:
    return yfinance_provider_capability()
