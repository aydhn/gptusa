
from usa_signal_bot.core.enums import DataProviderName, DataProviderCapability

def canonical_ohlcv_schema() -> list[str]:
    return ["symbol", "timestamp", "open", "high", "low", "close", "adjusted_close", "volume", "source", "fetched_at_utc", "quality_flags"]

def canonical_fundamental_schema() -> list[str]:
    return []

def canonical_macro_schema() -> list[str]:
    return []

def provider_schema_mapping(provider_name: DataProviderName, capability: DataProviderCapability) -> dict[str, str]:
    return {}

def validate_provider_schema_mapping(mapping: dict[str, str], canonical_schema: list[str]) -> list[str]:
    return []

def provider_schema_mapper_to_text(mapping: dict[str, str]) -> str:
    return str(mapping)
