import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf

from usa_signal_bot.core.enums import (
    DataProviderName, ProviderRequestType, ProviderResponseStatus, ProviderQualityStatus
)
from usa_signal_bot.providers.provider_capabilities import yfinance_capability_profile
from usa_signal_bot.providers.provider_interface import (
    BaseDataProvider, build_empty_provider_response, measure_provider_latency_ms,
    normalize_provider_symbols
)
from usa_signal_bot.providers.provider_models import (
    ProviderCapabilityProfile, ProviderHealthResult, ProviderRequest, ProviderResponse,
    create_provider_response_id, create_provider_health_id
)

class YFinanceDataProvider(BaseDataProvider):
    def __init__(self, cache_dir: Path | None = None, allow_network: bool = True, timeout_seconds: int = 30):
        self.cache_dir = cache_dir
        self.allow_network = allow_network
        self.timeout_seconds = timeout_seconds

    def name(self) -> DataProviderName:
        return DataProviderName.YFINANCE

    def capability_profile(self) -> ProviderCapabilityProfile:
        return yfinance_capability_profile()

    def fetch(self, request: ProviderRequest) -> ProviderResponse:
        start_time = time.perf_counter()

        if not self.allow_network:
            return build_empty_provider_response(
                request, self.name(), ProviderResponseStatus.BLOCKED, "Network access is disabled for yfinance"
            )

        if not self.supports(request):
            return build_empty_provider_response(
                request, self.name(), ProviderResponseStatus.FAILED, f"Unsupported request type: {request.request_type}"
            )

        if request.request_type == ProviderRequestType.OHLCV:
            response = self.fetch_ohlcv(request)
        else:
            response = build_empty_provider_response(
                request, self.name(), ProviderResponseStatus.FAILED, f"Unimplemented request type: {request.request_type}"
            )

        response.latency_ms = measure_provider_latency_ms(start_time, time.perf_counter())
        return response

    def fetch_ohlcv(self, request: ProviderRequest) -> ProviderResponse:
        symbols = normalize_provider_symbols(request.symbols)
        if not symbols:
            return build_empty_provider_response(request, self.name(), ProviderResponseStatus.FAILED, "No valid symbols provided")

        now_utc = datetime.now(timezone.utc).isoformat()

        try:
            # Batch mode mapping
            data_dict = {}
            total_rows = 0

            kwargs = {
                "tickers": " ".join(symbols),
                "interval": request.interval,
                "auto_adjust": False, # We want raw open/high/low/close plus adj close if requested
                "group_by": "ticker",
                "threads": False # Avoid threading issues in some environments
            }
            if request.start_date:
                kwargs["start"] = request.start_date
            if request.end_date:
                kwargs["end"] = request.end_date
            else:
                kwargs["period"] = "1y" # Default

            df = yf.download(**kwargs)

            if df.empty:
                return build_empty_provider_response(request, self.name(), ProviderResponseStatus.EMPTY, "yfinance returned an empty dataframe")

            if len(symbols) == 1:
                # Single symbol returns flat columns
                symbol = symbols[0]
                df_symbol = df.dropna(how="all")
                if not df_symbol.empty:
                    df_symbol = df_symbol.reset_index()
                    df_symbol.columns = [c.lower() for c in df_symbol.columns]
                    # Rename date column
                    if "date" in df_symbol.columns:
                        df_symbol.rename(columns={"date": "datetime"}, inplace=True)
                    # Convert datetimes to isoformat string
                    if "datetime" in df_symbol.columns and pd.api.types.is_datetime64_any_dtype(df_symbol["datetime"]):
                        df_symbol["datetime"] = df_symbol["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S%z")

                    data_dict[symbol] = df_symbol.to_dict(orient="records")
                    total_rows += len(df_symbol)
            else:
                # Multi symbol returns MultiIndex columns
                for symbol in symbols:
                    if symbol in df.columns.levels[0]:
                        df_symbol = df[symbol].dropna(how="all")
                        if not df_symbol.empty:
                            df_symbol = df_symbol.reset_index()
                            df_symbol.columns = [c.lower() for c in df_symbol.columns]
                            if "date" in df_symbol.columns:
                                df_symbol.rename(columns={"date": "datetime"}, inplace=True)
                            if "datetime" in df_symbol.columns and pd.api.types.is_datetime64_any_dtype(df_symbol["datetime"]):
                                df_symbol["datetime"] = df_symbol["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S%z")
                            data_dict[symbol] = df_symbol.to_dict(orient="records")
                            total_rows += len(df_symbol)

            if total_rows == 0:
                return build_empty_provider_response(request, self.name(), ProviderResponseStatus.EMPTY, "yfinance returned empty data after cleaning")

            status = ProviderResponseStatus.SUCCESS if len(data_dict) == len(symbols) else ProviderResponseStatus.PARTIAL

            return ProviderResponse(
                response_id=create_provider_response_id(),
                request_id=request.request_id,
                provider_name=self.name(),
                status=status,
                created_at_utc=now_utc,
                symbol_count=len(data_dict),
                row_count=total_rows,
                data=data_dict,
                warnings=[] if status == ProviderResponseStatus.SUCCESS else ["Some symbols missing from response"],
                metadata={"yfinance_version": yf.__version__}
            )

        except Exception as e:
            return build_empty_provider_response(request, self.name(), ProviderResponseStatus.FAILED, f"yfinance fetch error: {str(e)}")

    def health_check(self) -> ProviderHealthResult:
        now_utc = datetime.now(timezone.utc).isoformat()
        if not self.allow_network:
            return ProviderHealthResult(
                health_id=create_provider_health_id(),
                provider_name=self.name(),
                checked_at_utc=now_utc,
                status=ProviderQualityStatus.DEGRADED,
                reachable=False,
                capability_status={c.value: False for c in self.capability_profile().capabilities},
                warnings=["Network access is disabled for yfinance"]
            )

        # In a real environment we might try to reach a well-known symbol or just say true.
        # But for health check we do not make actual internet calls to avoid rate limits
        return ProviderHealthResult(
            health_id=create_provider_health_id(),
            provider_name=self.name(),
            checked_at_utc=now_utc,
            status=ProviderQualityStatus.GOOD,
            reachable=True,
            capability_status={c.value: True for c in self.capability_profile().capabilities}
        )
