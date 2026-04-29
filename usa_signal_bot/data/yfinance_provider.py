import yfinance as yf
from datetime import datetime, timezone

from usa_signal_bot.data.provider_interface import MarketDataProvider
from usa_signal_bot.data.provider_capabilities import ProviderCapability, yfinance_provider_capability
from usa_signal_bot.data.provider_policies import DataProviderPolicy, default_data_provider_policy
from usa_signal_bot.data.models import (
    MarketDataRequest, MarketDataResponse, ProviderStatus, ProviderFetchPlan
)
from usa_signal_bot.data.provider_guards import assert_request_is_safe
from usa_signal_bot.data.batches import estimate_batch_count
from usa_signal_bot.data.timeframes import timeframe_to_yfinance_interval, validate_timeframe_for_yfinance
from usa_signal_bot.data.normalizer import normalize_yfinance_dataframe

class YFinanceMarketDataProvider(MarketDataProvider):
    def __init__(self, policy: DataProviderPolicy | None = None, threads: bool = True, progress: bool = False):
        self._policy = policy or default_data_provider_policy()
        self._threads = threads
        self._progress = progress

    @property
    def name(self) -> str:
        return "yfinance"

    @property
    def capability(self) -> ProviderCapability:
        return yfinance_provider_capability()

    @property
    def policy(self) -> DataProviderPolicy:
        return self._policy

    def validate_request(self, request: MarketDataRequest) -> None:
        assert_request_is_safe(request)
        if request.provider_name.lower() != self.name:
             raise ValueError(f"Provider mismatch: expected {self.name}, got {request.provider_name}")
        validate_timeframe_for_yfinance(request.timeframe)
        self.assert_no_scraping()
        self.assert_free_provider()
        self.assert_no_broker_routing()

    def build_fetch_plan(self, request: MarketDataRequest) -> ProviderFetchPlan:
        self.validate_request(request)
        batch_size = self.policy.rate_limit.max_symbols_per_batch
        num_symbols = len(request.symbols)
        batch_count = estimate_batch_count(request.symbols, batch_size)

        return ProviderFetchPlan(
            provider_name=self.name,
            symbols=request.symbols,
            timeframe=request.timeframe,
            batch_count=batch_count,
            estimated_requests=batch_count,
            cache_enabled=request.use_cache and self.policy.cache.enabled,
            notes=["yfinance provider fetch plan"]
        )

    def fetch_ohlcv(self, request: MarketDataRequest) -> MarketDataResponse:
        self.validate_request(request)
        now_utc = datetime.now(timezone.utc).isoformat()

        interval = timeframe_to_yfinance_interval(request.timeframe)

        errors = []
        warnings = []
        bars = []
        success = False

        try:
            # Prepare arguments for yf.download
            # We don't batch here, the downloader should batch calls to this function,
            # or we let yfinance handle it if the list is small.
            # In Phase 8, yfinance handles bulk nicely, but we will rely on external batching.
            # Thus, we fetch whatever is in request.symbols in one go here.

            kwargs = {
                "tickers": request.symbols,
                "interval": interval,
                "auto_adjust": request.adjusted, # controlled by config request
                "threads": self._threads,
                "progress": self._progress
            }
            if request.start_date:
                 kwargs["start"] = request.start_date
            if request.end_date:
                 kwargs["end"] = request.end_date

            df = yf.download(**kwargs)

            if df.empty:
                 warnings.append("No data returned from yfinance.")
            else:
                 bars = normalize_yfinance_dataframe(df, request.symbols, request.timeframe, source=self.name)

                 if not bars:
                     warnings.append("Dataframe was not empty but no valid OHLCV bars could be extracted.")
                 else:
                     success = True

        except Exception as e:
            errors.append(f"yfinance fetch failed: {str(e)}")
            success = False

        return MarketDataResponse(
            request=request,
            bars=bars,
            success=success,
            provider_name=self.name,
            errors=errors,
            warnings=warnings,
            fetched_at_utc=now_utc,
            from_cache=False
        )

    def check_status(self) -> ProviderStatus:
        """
        In Phase 8, we avoid making an actual HTTP request in health checks to save limits.
        We just check configuration and assume available if the module loaded.
        """
        return ProviderStatus(
            provider_name=self.name,
            available=True,
            message="yfinance module is loaded and provider is configured.",
            checked_at_utc=datetime.now(timezone.utc).isoformat()
        )
