from typing import Any
from dataclasses import dataclass

@dataclass
class ProviderCachePolicy:
    provider_name: str
    cache_enabled: bool
    read_only_default: bool
    write_allowed_future: bool
    ttl_seconds: int | None
    cache_namespace: str
    warnings: list[str]
    metadata: dict[str, Any]

def build_default_provider_cache_policy(provider_name: str) -> ProviderCachePolicy:
    return ProviderCachePolicy(
        provider_name=provider_name,
        cache_enabled=True,
        read_only_default=True,
        write_allowed_future=True,
        ttl_seconds=86400,
        cache_namespace=f"provider_{provider_name}",
        warnings=[],
        metadata={}
    )

def validate_provider_cache_policy(item: ProviderCachePolicy) -> list[str]:
    errors = []
    if not item.read_only_default:
        errors.append("read_only_default must be True in Phase 102")
    return errors

def provider_cache_policy_to_dict(item: ProviderCachePolicy) -> dict[str, Any]:
    return {
        "provider_name": item.provider_name,
        "cache_enabled": item.cache_enabled,
        "read_only_default": item.read_only_default,
        "write_allowed_future": item.write_allowed_future,
        "ttl_seconds": item.ttl_seconds,
        "cache_namespace": item.cache_namespace,
        "warnings": item.warnings,
        "metadata": item.metadata
    }

def provider_cache_policy_to_text(item: ProviderCachePolicy) -> str:
    return f"Cache Policy [{item.provider_name}] - Enabled: {item.cache_enabled}"
