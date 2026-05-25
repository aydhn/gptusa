
from typing import Any
from usa_signal_bot.core.enums import DataProviderName, DataProviderCapability

def normalize_provider_response(provider_name: DataProviderName, payload: Any, capability: DataProviderCapability) -> dict[str, Any]:
    return {}

def normalize_ohlcv_response_skeleton(provider_name: DataProviderName, payload: Any) -> dict[str, Any]:
    return {}

def normalize_fundamental_response_skeleton(provider_name: DataProviderName, payload: Any) -> dict[str, Any]:
    return {}

def normalize_macro_response_skeleton(provider_name: DataProviderName, payload: Any) -> dict[str, Any]:
    return {}

def validate_normalized_response_schema(payload: dict[str, Any]) -> list[str]:
    return []

def provider_response_normalizer_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
