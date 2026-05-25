from typing import Any, Dict, List, Optional
import pandas as pd

from usa_signal_bot.data_providers.interfaces.market_data import MarketDataProviderBase
from usa_signal_bot.data_provider_runtime.phase107_models import ProviderRuntimeAdapterSpec, ProviderFetchDryRunPlan
from usa_signal_bot.data_provider_runtime.fetch_dry_run_planner import build_fetch_dry_run_plan
from usa_signal_bot.core.enums import ProviderImplementationStatus, ProviderFetchMode

class StooqMarketDataAdapter(MarketDataProviderBase):
    def adapter_spec(self) -> Dict[str, Any]:
        from usa_signal_bot.data_provider_runtime.phase107_models import provider_runtime_adapter_spec_to_dict
        spec = ProviderRuntimeAdapterSpec(
            provider_name="STOOQ",
            adapter_module="usa_signal_bot.data_providers.adapters.stooq_adapter",
            adapter_class="StooqMarketDataAdapter",
            implementation_status=ProviderImplementationStatus.IMPLEMENTED_NETWORK_GUARDED,
            fetch_mode=ProviderFetchMode.NETWORK_GUARDED_DISABLED,
            supports_contract_tests=True,
            supports_cache_key=True,
            supports_cache_lookup_dry_run=True,
            supports_local_fixture=False,
            supports_ohlcv_schema=True,
            network_guarded=True,
            network_enabled_by_default=False,
            paid_api=False,
            scraping_required=False,
            html_parsing_required=False,
            credential_required_now=False,
            broker_related=False,
            order_related=False,
            paper_mutation_related=False
        )
        return provider_runtime_adapter_spec_to_dict(spec)

    def validate_contract(self) -> List[str]:
        return []

    def build_daily_ohlcv_plan(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> ProviderFetchDryRunPlan:
        return build_fetch_dry_run_plan(
            provider_name="STOOQ",
            capability="GET_DAILY_OHLCV",
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            allow_network=False
        )

    def execute_metadata_only(self, request_or_plan: Any) -> Dict[str, Any]:
        return {
            "metadata_only": True,
            "provider": "STOOQ",
            "message": "This is a metadata-only execution. No network call was made.",
            "network_used": False
        }

    def fetch_daily_ohlcv_guarded(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None, allow_network: bool = False) -> Dict[str, Any]:
        if not allow_network:
            return self.execute_metadata_only(None)

        return {
            "metadata_only": True,
            "provider": "STOOQ",
            "network_used": False,
            "warning": "Network fetch guarded and ignored in phase 107"
        }

    def normalize_sample(self, payload: Any | None = None) -> Dict[str, Any]:
        from datetime import datetime, timezone
        return {
            "symbol": "AAPL",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "open": 150.0,
            "high": 155.0,
            "low": 149.0,
            "close": 152.0,
            "adjusted_close": 152.0,
            "volume": 1000000,
            "source": "STOOQ",
            "fetched_at_utc": datetime.now(timezone.utc).isoformat()
        }
