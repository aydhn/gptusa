
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderRegistryEntry
from usa_signal_bot.core.enums import DataProviderName

def build_provider_registry_entries() -> list[ProviderRegistryEntry]:
    return []

def provider_registry_entry_for_name(provider_name: DataProviderName) -> ProviderRegistryEntry | None:
    for entry in build_provider_registry_entries():
        if entry.provider_name == provider_name:
            return entry
    return None

def enabled_provider_registry_entries(entries: list[ProviderRegistryEntry]) -> list[ProviderRegistryEntry]:
    return [e for e in entries if e.enabled]

def provider_registry_summary(entries: list[ProviderRegistryEntry]) -> dict[str, Any]:
    return {"total": len(entries), "enabled": len(enabled_provider_registry_entries(entries))}

def provider_registry_to_text(entries: list[ProviderRegistryEntry], limit: int = 200) -> str:
    return str(entries)[:limit]
