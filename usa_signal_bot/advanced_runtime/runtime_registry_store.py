import json
from pathlib import Path
from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import (
    NormalizedRuntimeRegistry, RuntimeRegistryFullReview,
    ProviderCapabilityManifest, ProviderSafetyManifest, ConfigSurfaceRecord,
    normalized_runtime_registry_to_dict, runtime_registry_full_review_to_dict,
    provider_capability_manifest_to_dict, provider_safety_manifest_to_dict,
    config_surface_record_to_dict
)

def runtime_registry_store_dir(data_root: Path) -> Path:
    d = data_root / "advanced_runtime"
    d.mkdir(parents=True, exist_ok=True)
    return d

def normalized_registries_dir(data_root: Path) -> Path:
    d = runtime_registry_store_dir(data_root) / "registries"
    d.mkdir(parents=True, exist_ok=True)
    return d

def runtime_registry_reviews_dir(data_root: Path) -> Path:
    d = runtime_registry_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_manifests_dir(data_root: Path) -> Path:
    d = runtime_registry_store_dir(data_root) / "provider_manifests"
    d.mkdir(parents=True, exist_ok=True)
    return d

def config_surface_reports_dir(data_root: Path) -> Path:
    d = runtime_registry_store_dir(data_root) / "config_surface"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_normalized_runtime_registry_json(path: Path, item: NormalizedRuntimeRegistry) -> Path:
    fpath = path / f"{item.registry_id}.json"
    with open(fpath, "w") as f:
        json.dump(normalized_runtime_registry_to_dict(item), f, indent=2)
    return fpath

def write_runtime_registry_full_review_json(path: Path, item: RuntimeRegistryFullReview) -> Path:
    fpath = path / f"{item.review_id}.json"
    with open(fpath, "w") as f:
        json.dump(runtime_registry_full_review_to_dict(item), f, indent=2)
    return fpath

def write_provider_capability_manifests_jsonl(path: Path, items: list[ProviderCapabilityManifest]) -> Path:
    fpath = path / f"capabilities_{items[0].manifest_id if items else 'empty'}.jsonl"
    with open(fpath, "w") as f:
        for item in items:
            f.write(json.dumps(provider_capability_manifest_to_dict(item)) + "\n")
    return fpath

def write_provider_safety_manifests_jsonl(path: Path, items: list[ProviderSafetyManifest]) -> Path:
    fpath = path / f"safeties_{items[0].manifest_id if items else 'empty'}.jsonl"
    with open(fpath, "w") as f:
        for item in items:
            f.write(json.dumps(provider_safety_manifest_to_dict(item)) + "\n")
    return fpath

def write_config_surface_jsonl(path: Path, items: list[ConfigSurfaceRecord]) -> Path:
    fpath = path / "config_surface.jsonl"
    with open(fpath, "w") as f:
        for item in items:
            f.write(json.dumps(config_surface_record_to_dict(item)) + "\n")
    return fpath

def read_runtime_registry_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_runtime_registry_reviews(data_root: Path) -> list[Path]:
    d = runtime_registry_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_runtime_registry_review(data_root: Path) -> Path | None:
    files = list_runtime_registry_reviews(data_root)
    if not files: return None
    return max(files, key=lambda f: f.stat().st_mtime)

def runtime_registry_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "registries": len(list(normalized_registries_dir(data_root).glob("*.json"))),
        "reviews": len(list(runtime_registry_reviews_dir(data_root).glob("*.json")))
    }
