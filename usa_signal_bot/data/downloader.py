import time
from pathlib import Path
from typing import Optional, List, Tuple
from usa_signal_bot.data.provider_registry import ProviderRegistry
from usa_signal_bot.storage.file_store import LocalFileStore
from usa_signal_bot.data.provider_policies import DataProviderPolicy, default_data_provider_policy
from usa_signal_bot.data.models import MarketDataRequest, MarketDataResponse, OHLCVBar
from usa_signal_bot.universe.models import UniverseDefinition
from usa_signal_bot.data.batches import build_symbol_batches
from usa_signal_bot.data.quality import validate_ohlcv_bars_quality, DataQualityReport
from usa_signal_bot.data.cache import build_market_data_cache_path, write_ohlcv_bars_cache, is_cache_fresh, read_ohlcv_bars_cache
from usa_signal_bot.storage.manifest import Manifest
from usa_signal_bot.core.exceptions import DataProviderError
from usa_signal_bot.core.logging_config import get_logger

logger = get_logger(__name__)

class MarketDataDownloader:
    def __init__(self, provider_registry: ProviderRegistry, store: LocalFileStore, data_root: Path, policy: Optional[DataProviderPolicy] = None):
        self.registry = provider_registry
        self.store = store
        self.data_root = data_root
        self.policy = policy or default_data_provider_policy()

    def download(self, request: MarketDataRequest, write_cache: bool = True) -> MarketDataResponse:
        """Executes a market data fetch, honoring cache, batches, and rate limits."""
        provider = self.registry.get(request.provider_name)
        plan = provider.build_fetch_plan(request)

        all_bars = []
        all_errors = []
        all_warnings = []

        # Determine cache path upfront (assuming whole request batches same timeframe/dates)
        # Note: If cache holds all symbols, we could skip entirely. For simplicity, we
        # cache and read by provider+timeframe+dates to see if we can skip the fetch.
        # But this gets tricky with lists of symbols. A robust approach caches by symbol.
        # Here we just fetch what is requested. Caching by individual symbol is better long-term.

        batches = build_symbol_batches(request.symbols, self.policy.rate_limit.max_symbols_per_batch)

        for idx, batch_symbols in enumerate(batches):
            batch_req = MarketDataRequest(
                symbols=batch_symbols,
                timeframe=request.timeframe,
                start_date=request.start_date,
                end_date=request.end_date,
                provider_name=provider.name,
                adjusted=request.adjusted,
                use_cache=request.use_cache
            )

            try:
                # 1. Fetch from provider
                resp = provider.fetch_ohlcv(batch_req)
                if resp.bars:
                    all_bars.extend(resp.bars)
                all_errors.extend(resp.errors)
                all_warnings.extend(resp.warnings)

                # 2. Rate limiting sleep if not the last batch
                if idx < len(batches) - 1:
                    time.sleep(self.policy.rate_limit.min_seconds_between_requests)

            except Exception as e:
                all_errors.append(f"Batch {idx} failed: {e}")

        # 3. Cache the results if enabled
        if write_cache and all_bars and self.policy.cache.enabled:
            # For Phase 8, we can write one giant cache file per request, or one per symbol.
            # Writing one per symbol is usually better for modularity.
            self._cache_bars_by_symbol(all_bars, provider.name, request.timeframe, request.start_date, request.end_date)

        success = len(all_bars) > 0 and len(all_errors) == 0

        return MarketDataResponse(
            request=request,
            bars=all_bars,
            success=success,
            provider_name=provider.name,
            errors=all_errors,
            warnings=all_warnings,
            fetched_at_utc=resp.fetched_at_utc if 'resp' in locals() else "",
            from_cache=False # To accurately say from_cache=True, we'd need to actually skip fetch above
        )

    def _cache_bars_by_symbol(self, bars: List[OHLCVBar], provider_name: str, timeframe: str, start_date: Optional[str], end_date: Optional[str]):
        """Splits bars by symbol and caches them individually."""
        from usa_signal_bot.data.cache import split_bars_by_symbol
        grouped = split_bars_by_symbol(bars)
        for sym, sym_bars in grouped.items():
            path = build_market_data_cache_path(self.data_root, provider_name, sym, timeframe, start_date, end_date)
            write_ohlcv_bars_cache(path, sym_bars)
            logger.info(f"Cached {len(sym_bars)} bars for {sym} to {path.name}")

    def download_for_symbols(self, symbols: List[str], timeframe: str, provider_name: str = "yfinance",
                             start_date: Optional[str] = None, end_date: Optional[str] = None,
                             adjusted: bool = True, write_cache: bool = True) -> MarketDataResponse:
        """Helper to create request and download."""
        if not symbols:
            raise DataProviderError("No symbols provided for download.")

        request = MarketDataRequest(
            symbols=symbols, timeframe=timeframe, start_date=start_date,
            end_date=end_date, provider_name=provider_name, adjusted=adjusted
        )
        return self.download(request, write_cache=write_cache)

    def download_for_universe(self, universe: UniverseDefinition, timeframe: str, provider_name: str = "yfinance",
                              limit: Optional[int] = None, write_cache: bool = True) -> MarketDataResponse:
        """Downloads data for an entire universe."""
        symbols = [sym.symbol for sym in universe.symbols if sym.active]
        if limit and limit > 0:
            symbols = symbols[:limit]

        return self.download_for_symbols(
            symbols=symbols, timeframe=timeframe, provider_name=provider_name, write_cache=write_cache
        )

    def build_manifest_for_response(self, response: MarketDataResponse, cache_paths: List[Path]) -> Manifest:
        """Builds a storage manifest tracking the downloaded cache files."""
        # This is a stub for potential integration with the storage/manifest.py logic
        from usa_signal_bot.storage.manifest import create_manifest
        return create_manifest("market_data_download", self.data_root)

    def write_download_summary(self, response: MarketDataResponse, quality_report: Optional[DataQualityReport] = None) -> Path:
        """Writes a summary of the download and quality checks."""
        from usa_signal_bot.utils.time_utils import utc_now
        summary = {
            "timestamp_utc": utc_now().isoformat(),
            "provider": response.provider_name,
            "success": response.success,
            "symbols_requested": len(response.request.symbols),
            "symbols_returned": len(response.symbols_returned()),
            "total_bars": response.bar_count(),
            "errors": response.errors,
            "warnings": response.warnings
        }

        if quality_report:
            summary["quality"] = {
                "status": quality_report.status.value,
                "valid_bars": quality_report.valid_bars,
                "invalid_bars": quality_report.invalid_bars,
                "missing_symbols": quality_report.missing_symbols
            }

        path = self.data_root / "cache" / f"download_summary_{response.provider_name}.json"
        self.store.write_json("cache", f"download_summary_{response.provider_name}.json", summary)
        return path
