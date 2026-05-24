from typing import Any
from dataclasses import dataclass

@dataclass
class ProviderRateLimitMetadata:
    provider_name: str
    known: bool
    requests_per_minute: int | None
    requests_per_day: int | None
    burst_allowed: bool | None
    source: str
    warnings: list[str]
    metadata: dict[str, Any]

def build_unknown_rate_limit_metadata(provider_name: str) -> ProviderRateLimitMetadata:
    return ProviderRateLimitMetadata(
        provider_name=provider_name,
        known=False,
        requests_per_minute=None,
        requests_per_day=None,
        burst_allowed=None,
        source="SYSTEM_DEFAULT",
        warnings=["Rate limits are unknown for this provider"],
        metadata={}
    )

def validate_rate_limit_metadata(item: ProviderRateLimitMetadata) -> list[str]:
    return []

def rate_limit_metadata_to_dict(item: ProviderRateLimitMetadata) -> dict[str, Any]:
    return {
        "provider_name": item.provider_name,
        "known": item.known,
        "requests_per_minute": item.requests_per_minute,
        "requests_per_day": item.requests_per_day,
        "burst_allowed": item.burst_allowed,
        "source": item.source,
        "warnings": item.warnings,
        "metadata": item.metadata
    }

def rate_limit_metadata_to_text(item: ProviderRateLimitMetadata) -> str:
    return f"Rate Limit Metadata [{item.provider_name}] - Known: {item.known}"
