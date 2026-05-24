from typing import Any
from dataclasses import dataclass

@dataclass
class ProviderQualityHint:
    provider_name: str
    field_name: str
    hint_type: str
    severity: str
    message: str
    metadata: dict[str, Any]

def build_provider_quality_hint(provider_name: str, field_name: str, hint_type: str, severity: str, message: str) -> ProviderQualityHint:
    return ProviderQualityHint(
        provider_name=provider_name,
        field_name=field_name,
        hint_type=hint_type,
        severity=severity,
        message=message,
        metadata={}
    )

def default_provider_quality_hints(provider_name: str) -> list[ProviderQualityHint]:
    return []

def provider_quality_hint_to_dict(item: ProviderQualityHint) -> dict[str, Any]:
    return {
        "provider_name": item.provider_name,
        "field_name": item.field_name,
        "hint_type": item.hint_type,
        "severity": item.severity,
        "message": item.message,
        "metadata": item.metadata
    }

def provider_quality_hints_to_text(items: list[ProviderQualityHint]) -> str:
    return f"{len(items)} Quality Hints"
