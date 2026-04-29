from abc import ABC, abstractmethod
from usa_signal_bot.data.provider_capabilities import ProviderCapability
from usa_signal_bot.data.provider_policies import DataProviderPolicy
from usa_signal_bot.data.models import MarketDataRequest, MarketDataResponse, ProviderStatus, ProviderFetchPlan
from usa_signal_bot.core.exceptions import WebScrapingForbiddenError, BrokerRoutingForbiddenError, ProviderCapabilityError
from usa_signal_bot.data.provider_guards import (
    assert_provider_is_free,
    assert_provider_does_not_scrape,
    assert_provider_requires_no_paid_api,
    assert_no_forbidden_provider_name
)

class MarketDataProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def capability(self) -> ProviderCapability:
        pass

    @property
    @abstractmethod
    def policy(self) -> DataProviderPolicy:
        pass

    @abstractmethod
    def validate_request(self, request: MarketDataRequest) -> None:
        pass

    @abstractmethod
    def build_fetch_plan(self, request: MarketDataRequest) -> ProviderFetchPlan:
        pass

    @abstractmethod
    def fetch_ohlcv(self, request: MarketDataRequest) -> MarketDataResponse:
        pass

    @abstractmethod
    def check_status(self) -> ProviderStatus:
        pass

    def assert_no_scraping(self) -> None:
        if self.capability.allows_scraping:
            raise WebScrapingForbiddenError(f"Provider {self.name} uses forbidden web scraping.")

    def assert_free_provider(self) -> None:
        if not self.capability.free_only:
            raise ProviderCapabilityError(f"Provider {self.name} is not a free provider.")

    def assert_no_broker_routing(self) -> None:
        assert_no_forbidden_provider_name(self.name)
