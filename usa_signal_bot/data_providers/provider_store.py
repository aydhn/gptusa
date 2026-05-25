
from pathlib import Path
from typing import Any
from usa_signal_bot.data_providers.phase106_models import (
    ProviderAbstractionContext, ProviderAbstractionFullReview, ProviderRegistryEntry,
    ProviderAdapterSpec, ProviderCapabilityMatrix, ProviderSafetyPolicy,
    provider_abstraction_context_to_dict, provider_abstraction_full_review_to_dict,
    provider_registry_entry_to_dict, provider_adapter_spec_to_dict,
    provider_capability_matrix_to_dict, provider_safety_policy_to_dict
)
import json

def provider_store_dir(data_root: Path) -> Path: return data_root / "data_providers"
def provider_contexts_dir(data_root: Path) -> Path: return provider_store_dir(data_root) / "contexts"
def provider_reviews_dir(data_root: Path) -> Path: return provider_store_dir(data_root) / "reviews"
def provider_registry_dir(data_root: Path) -> Path: return provider_store_dir(data_root) / "registry"
def provider_specs_dir(data_root: Path) -> Path: return provider_store_dir(data_root) / "specs"
def provider_capability_matrix_dir(data_root: Path) -> Path: return provider_store_dir(data_root) / "capability_matrix"
def provider_safety_policy_dir(data_root: Path) -> Path: return provider_store_dir(data_root) / "safety_policy"

def write_provider_abstraction_context_json(path: Path, item: ProviderAbstractionContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: json.dump(provider_abstraction_context_to_dict(item), f, indent=2)
    return path

def write_provider_abstraction_full_review_json(path: Path, item: ProviderAbstractionFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: json.dump(provider_abstraction_full_review_to_dict(item), f, indent=2)
    return path

def write_provider_registry_jsonl(path: Path, items: list[ProviderRegistryEntry]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items: f.write(json.dumps(provider_registry_entry_to_dict(item)) + "\n")
    return path

def write_provider_adapter_specs_jsonl(path: Path, items: list[ProviderAdapterSpec]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items: f.write(json.dumps(provider_adapter_spec_to_dict(item)) + "\n")
    return path

def write_provider_capability_matrix_json(path: Path, item: ProviderCapabilityMatrix) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: json.dump(provider_capability_matrix_to_dict(item), f, indent=2)
    return path

def write_provider_safety_policy_json(path: Path, item: ProviderSafetyPolicy) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: json.dump(provider_safety_policy_to_dict(item), f, indent=2)
    return path

def read_provider_abstraction_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r") as f: return json.load(f)

def list_provider_abstraction_reviews(data_root: Path) -> list[Path]:
    d = provider_reviews_dir(data_root)
    if not d.exists(): return []
    return sorted(list(d.glob("*.json")))

def get_latest_provider_abstraction_review(data_root: Path) -> Path | None:
    lst = list_provider_abstraction_reviews(data_root)
    return lst[-1] if lst else None

def provider_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews": len(list_provider_abstraction_reviews(data_root))}
