
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderRegistryEntry

def validate_provider_registry(entries: list[ProviderRegistryEntry]) -> list[str]:
    return []

def validate_provider_registry_priorities(entries: list[ProviderRegistryEntry]) -> list[str]:
    return []

def validate_provider_registry_defaults(entries: list[ProviderRegistryEntry]) -> list[str]:
    return []

def provider_registry_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"errors": len(errors)}

def provider_registry_validator_to_text(errors: list[str]) -> str:
    return str(errors)
