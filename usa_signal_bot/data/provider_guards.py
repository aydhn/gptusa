from usa_signal_bot.data.provider_capabilities import ProviderCapability
from usa_signal_bot.data.models import MarketDataRequest
from usa_signal_bot.core.exceptions import (
    ProviderCapabilityError, ForbiddenProviderError, ProviderRequestError
)

FORBIDDEN_PROVIDERS = {
    "alpaca",
    "interactivebrokers",
    "ibkr",
    "robinhood",
    "tradier",
    "polygon_paid",
    "benzinga_paid",
    "bloomberg",
    "refinitiv"
}

def assert_provider_is_free(capability: ProviderCapability) -> None:
    if not capability.free_only:
        raise ProviderCapabilityError(f"Provider '{capability.provider_name}' violates free-only rule.")

def assert_provider_does_not_scrape(capability: ProviderCapability) -> None:
    if capability.allows_scraping:
        raise ProviderCapabilityError(f"Provider '{capability.provider_name}' violates web scraping prohibition.")

def assert_provider_requires_no_paid_api(capability: ProviderCapability) -> None:
    if capability.requires_api_key and not capability.free_only:
         raise ProviderCapabilityError(f"Provider '{capability.provider_name}' requires a paid API key which is forbidden.")

def assert_provider_has_no_broker_routing(provider_name: str) -> None:
    pass # Centralized check handles this via name currently. Can be expanded if capabilities get broker-routing flags.

def assert_no_forbidden_provider_name(provider_name: str) -> None:
    if provider_name.lower() in FORBIDDEN_PROVIDERS:
        raise ForbiddenProviderError(f"Provider '{provider_name}' is forbidden by project rules (broker/paid API).")

def assert_request_is_safe(request: MarketDataRequest) -> None:
    if not request.symbols:
        raise ProviderRequestError("MarketDataRequest cannot have empty symbols.")
