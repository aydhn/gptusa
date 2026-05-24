from typing import Any

def normalize_storage_registry(registry: dict[str, str]) -> dict[str, str]:
    return registry.copy()

def validate_normalized_storage_registry(registry: dict[str, str]) -> list[str]:
    return []

def storage_registry_normalizer_summary(registry: dict[str, str]) -> dict[str, Any]:
    return {"paths": len(registry)}

def storage_registry_normalizer_to_text(registry: dict[str, str]) -> str:
    return "Storage registry normalized."
