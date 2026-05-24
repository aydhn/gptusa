from pathlib import Path
from typing import Dict, List

def required_storage_registry_keys() -> List[str]:
    return [
        "data_root", "logs", "reports", "metadata", "advanced_transition",
        "phase101", "handoff_freeze", "validation", "observability",
        "quality", "cache", "tests"
    ]

def build_storage_registry(data_root: Path) -> Dict[str, str]:
    return {k: str(data_root / k) for k in required_storage_registry_keys()}

def validate_storage_registry(registry: Dict[str, str]) -> List[str]:
    errors = []
    for k in required_storage_registry_keys():
        if k not in registry:
            errors.append(f"Missing key: {k}")
    return errors

def storage_registry_to_text(registry: Dict[str, str]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in registry.items()])
