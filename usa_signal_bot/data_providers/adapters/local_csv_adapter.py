from typing import Any, Dict, List, Optional
import pandas as pd
from pathlib import Path
import os

from usa_signal_bot.data_providers.interfaces.base import DataProviderAdapterBase
from usa_signal_bot.data_provider_runtime.phase107_models import ProviderRuntimeAdapterSpec
from usa_signal_bot.core.enums import ProviderImplementationStatus, ProviderFetchMode

class LocalCsvMarketDataAdapter(DataProviderAdapterBase):
    def adapter_spec(self) -> Dict[str, Any]:
        from usa_signal_bot.data_provider_runtime.phase107_models import provider_runtime_adapter_spec_to_dict
        spec = ProviderRuntimeAdapterSpec(
            provider_name="LOCAL_CSV",
            adapter_module="usa_signal_bot.data_providers.adapters.local_csv_adapter",
            adapter_class="LocalCsvMarketDataAdapter",
            implementation_status=ProviderImplementationStatus.IMPLEMENTED_LOCAL_FIXTURE,
            fetch_mode=ProviderFetchMode.LOCAL_FIXTURE_ONLY,
            supports_contract_tests=True,
            supports_cache_key=False,
            supports_cache_lookup_dry_run=False,
            supports_local_fixture=True,
            supports_ohlcv_schema=True,
            network_guarded=False,
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

    def build_local_fixture_request(self, path: str | Path, symbol: Optional[str] = None) -> Dict[str, Any]:
        return {
            "provider": "LOCAL_CSV",
            "path": str(path),
            "symbol": symbol
        }

    def read_local_fixture(self, path: str | Path) -> Dict[str, Any]:
        p = Path(path)
        if not p.exists():
            return {"error": "Path does not exist"}

        # Path traversal guard
        try:
            p.resolve().relative_to(Path.cwd())
        except ValueError:
            return {"error": "Path traversal detected"}

        try:
            df = pd.read_csv(p)
            return {
                "metadata_only": False,
                "provider": "LOCAL_CSV",
                "rows_returned": len(df),
                "data": df.to_dict(orient="records"),
                "network_used": False
            }
        except Exception as e:
            return {"error": f"Failed to read CSV: {str(e)}"}

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
            "source": "LOCAL_CSV",
            "fetched_at_utc": datetime.now(timezone.utc).isoformat()
        }
