import time
from pathlib import Path
from typing import Optional, List, Tuple
from usa_signal_bot.data.provider_registry import ProviderRegistry
from usa_signal_bot.storage.file_store import LocalFileStore
from usa_signal_bot.data.provider_policies import DataProviderPolicy, default_data_provider_policy
from usa_signal_bot.data.models import MarketDataRequest, MarketDataResponse, OHLCVBar
from usa_signal_bot.universe.models import UniverseDefinition
from usa_signal_bot.data.batches import build_symbol_batches
from usa_signal_bot.data.quality import run_full_ohlcv_quality_validation, write_quality_report_json, write_anomaly_report_json, DataQualityReport
from usa_signal_bot.data.cache import build_market_data_cache_path, write_ohlcv_bars_cache, is_cache_fresh, read_ohlcv_bars_cache
from usa_signal_bot.storage.manifest import Manifest
from usa_signal_bot.core.exceptions import DataProviderError
from usa_signal_bot.core.logging_config import get_logger
from usa_signal_bot.data.repair import repair_ohlcv_bars, write_repair_report_json
from usa_signal_bot.data.anomalies import has_blocking_anomalies

logger = get_logger(__name__)

class MarketDataDownloader:
    def __init__(self, provider_registry: ProviderRegistry, store: LocalFileStore, data_root: Path, policy: Optional[DataProviderPolicy] = None):
        self.registry = provider_registry
        self.store = store
        self.data_root = data_root
        self.policy = policy or default_data_provider_policy()

    def download(self, request: MarketDataRequest, write_cache: bool = True, repair_enabled: bool = True, validate_before_cache: bool = True) -> MarketDataResponse:
        """Executes a market data fetch, honoring cache, batches, and rate limits."""
        provider = self.registry.get(request.provider_name)
        plan = provider.build_fetch_plan(request)

        all_bars = []
        all_errors = []
        all_warnings = []

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

                # 2. Validation & Repair
                final_bars = resp.bars
                if validate_before_cache and final_bars:
                    q_report, a_report = run_full_ohlcv_quality_validation(final_bars, batch_symbols, provider.name, request.timeframe)

                    # Save initial reports
                    base_report_name = f"report_{provider.name}_{request.timeframe}_{idx}"
                    q_path = self.data_root / "reports" / f"quality_{base_report_name}.json"
                    a_path = self.data_root / "reports" / f"anomaly_{base_report_name}.json"
                    write_quality_report_json(q_path, q_report)
                    write_anomaly_report_json(a_path, a_report)

                    if has_blocking_anomalies(a_report):
                        if repair_enabled:
                            logger.info(f"Anomalies detected in batch {idx}. Running repair pipeline.")
                            final_bars, r_report = repair_ohlcv_bars(final_bars, batch_symbols, allow_drop_invalid=True)
                            r_path = self.data_root / "reports" / f"repair_{base_report_name}.json"
                            write_repair_report_json(r_path, r_report)
                            all_warnings.append(f"Batch {idx} repaired: {r_report.dropped_bar_count} dropped")

                            # Re-validate
                            q_report2, a_report2 = run_full_ohlcv_quality_validation(final_bars, batch_symbols, provider.name, request.timeframe)
                            if has_blocking_anomalies(a_report2):
                                all_errors.append(f"Batch {idx} still has critical errors after repair.")
                                final_bars = [] # Do not cache or use
                        else:
                            all_errors.append(f"Batch {idx} has blocking anomalies and repair is disabled.")
                            final_bars = []

                if final_bars:
                    all_bars.extend(final_bars)

                all_errors.extend(resp.errors)
                all_warnings.extend(resp.warnings)

                # Rate limiting sleep if not the last batch
                if idx < len(batches) - 1:
                    time.sleep(self.policy.rate_limit.min_seconds_between_requests)

            except Exception as e:
                all_errors.append(f"Batch {idx} failed: {e}")

        # 3. Cache the results if enabled
        if write_cache and all_bars and self.policy.cache.enabled:
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
            from_cache=False
        )

    def _cache_bars_by_symbol(self, bars: List[OHLCVBar], provider_name: str, timeframe: str, start_date: Optional[str], end_date: Optional[str]):
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

    def download_with_refresh_decision(self, request: MarketDataRequest, force_refresh: bool = False, use_cache: bool = True) -> MarketDataResponse:
        """
        A high-level method to download data utilizing cache decisions, without needing a full refresh plan.
        Mainly for convenience when orchestrating from higher levels.
        """
        if not use_cache or force_refresh:
            return self.download(request)

        from .cache import find_latest_cache_file, read_ohlcv_bars_cache
        from .models import OHLCVBar
        import datetime
        import logging

        logger = logging.getLogger(__name__)

        # Simplified logic: If we have a cache file for every symbol that is not stale, use it.
        # But MarketDataRequest can contain multiple symbols. It's often better to just build a mini-plan.
        # Since this is an adapter method, we can lean on the existing cache if requested.
        # If we just need to return a MarketDataResponse from cache:

        cached_bars = []
        symbols_to_fetch = []

        # Simplified TTL logic (24h default)
        ttl = 86400

        for sym in request.symbols:
            latest = find_latest_cache_file(self.data_root, request.provider_name, sym, request.timeframe)
            stale = True
            if latest:
                mtime = latest.stat().st_mtime
                age = datetime.datetime.now().timestamp() - mtime
                if age <= ttl:
                    stale = False

            if not stale and latest:
                try:
                    raw = read_ohlcv_bars_cache(latest)
                    for r in raw:
                        cached_bars.append(OHLCVBar(**r))
                except Exception:
                    symbols_to_fetch.append(sym)
            else:
                symbols_to_fetch.append(sym)

        if not symbols_to_fetch:
            return MarketDataResponse(
                request=request,
                bars=cached_bars,
                success=True,
                provider_name=request.provider_name,
                from_cache=True,
                fetched_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )

        # We need to fetch at least some
        req_to_fetch = MarketDataRequest(
            symbols=symbols_to_fetch,
            timeframe=request.timeframe,
            start_date=request.start_date,
            end_date=request.end_date,
            provider_name=request.provider_name,
            adjusted=request.adjusted,
            use_cache=False # Force fetch for these
        )

        resp = self.download(req_to_fetch)
        # Combine
        resp.bars.extend(cached_bars)
        # For simplicity, if we hit network, from_cache = False

        return resp
