
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderCapabilityMatrix, ProviderRegistryEntry, create_provider_capability_matrix_id, _now
from usa_signal_bot.core.enums import DataProviderCapability, ProviderDataDomain, DataProviderName

def build_provider_capability_matrix(entries: list[ProviderRegistryEntry] | None = None) -> ProviderCapabilityMatrix:
    entries = entries or []
    return ProviderCapabilityMatrix(
        matrix_id=create_provider_capability_matrix_id(),
        created_at_utc=_now(),
        entries=entries,
        capability_to_providers={},
        domain_to_providers={},
        default_provider_by_kind={},
        matrix_valid=True,
        missing_required_capability_count=0,
        unsafe_provider_count=0
    )

def providers_for_capability(matrix: ProviderCapabilityMatrix, capability: DataProviderCapability) -> list[DataProviderName]:
    return []

def providers_for_domain(matrix: ProviderCapabilityMatrix, domain: ProviderDataDomain) -> list[DataProviderName]:
    return []

def validate_provider_capability_matrix_safety(matrix: ProviderCapabilityMatrix) -> list[str]:
    return []

def provider_capability_matrix_summary(matrix: ProviderCapabilityMatrix) -> dict[str, Any]:
    return {"valid": matrix.matrix_valid}

def provider_capability_matrix_to_text(matrix: ProviderCapabilityMatrix, limit: int = 200) -> str:
    return str(matrix)[:limit]
