"""Metadata-only implementations for skeleton market-data adapters (no network, no I/O)."""
from typing import Any, Dict


class MetadataOnlySkeletonMixin:
    skeleton_only = True

    def adapter_spec(self) -> Dict[str, Any]:
        return {
            "provider_name": getattr(getattr(self, "provider_name", None), "value", None),
            "skeleton_only": True,
            "network_calls": False,
        }

    def validate_contract(self) -> list[str]:
        return []

    def build_daily_ohlcv_plan(self, symbol: str, start_date: str | None = None, end_date: str | None = None) -> Any:
        return {"symbol": symbol, "start_date": start_date, "end_date": end_date, "metadata_only": True}

    def execute_metadata_only(self, request_or_plan: Any) -> Dict[str, Any]:
        return {"executed": False, "metadata_only": True, "plan": request_or_plan}

    def normalize_sample(self, payload: Any | None = None) -> Dict[str, Any]:
        return {"normalized": False, "metadata_only": True, "payload": payload}
