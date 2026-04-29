from datetime import datetime, timezone
import math

from usa_signal_bot.data.provider_interface import MarketDataProvider
from usa_signal_bot.data.provider_capabilities import ProviderCapability, default_mock_provider_capability
from usa_signal_bot.data.provider_policies import DataProviderPolicy, default_data_provider_policy
from usa_signal_bot.data.models import (
    MarketDataRequest, MarketDataResponse, ProviderStatus, ProviderFetchPlan, OHLCVBar
)
from usa_signal_bot.data.provider_guards import assert_request_is_safe

class MockMarketDataProvider(MarketDataProvider):
    @property
    def name(self) -> str:
        return "mock"

    @property
    def capability(self) -> ProviderCapability:
        return default_mock_provider_capability()

    @property
    def policy(self) -> DataProviderPolicy:
        return default_data_provider_policy()

    def validate_request(self, request: MarketDataRequest) -> None:
        assert_request_is_safe(request)

    def build_fetch_plan(self, request: MarketDataRequest) -> ProviderFetchPlan:
        self.validate_request(request)
        batch_size = self.policy.rate_limit.max_symbols_per_batch
        num_symbols = len(request.symbols)
        batch_count = math.ceil(num_symbols / batch_size) if batch_size > 0 else 1

        return ProviderFetchPlan(
            provider_name=self.name,
            symbols=request.symbols,
            timeframe=request.timeframe,
            batch_count=batch_count,
            estimated_requests=batch_count,
            cache_enabled=request.use_cache and self.policy.cache.enabled,
            notes=["Mock provider plan created."]
        )

    def fetch_ohlcv(self, request: MarketDataRequest) -> MarketDataResponse:
        self.validate_request(request)
        now = datetime.now(timezone.utc).isoformat()
        bars = []
        for sym in request.symbols:
            # Deterministic mock data
            bars.append(OHLCVBar(
                symbol=sym,
                timestamp_utc=now,
                timeframe=request.timeframe,
                open=100.0,
                high=105.0,
                low=95.0,
                close=101.0,
                volume=10000,
                adjusted_close=101.0,
                source=self.name
            ))

        return MarketDataResponse(
            request=request,
            bars=bars,
            success=True,
            provider_name=self.name,
            fetched_at_utc=now,
            from_cache=False
        )

    def check_status(self) -> ProviderStatus:
        return ProviderStatus(
            provider_name=self.name,
            available=True,
            message="Mock provider is available.",
            checked_at_utc=datetime.now(timezone.utc).isoformat()
        )
