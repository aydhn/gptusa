import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeContext,
    ProviderFreezeFullReview,
    ProviderExpansionFreezeBundle,
    MultiProviderFinalReviewReport,
    DataLayerRehearsalReport,
    DataLayerOutputContract,
    ProviderFreezeArtifactManifest,
    provider_freeze_context_to_dict,
    provider_freeze_full_review_to_dict,
    provider_expansion_freeze_bundle_to_dict,
    multi_provider_final_review_report_to_dict,
    data_layer_rehearsal_report_to_dict,
    data_layer_output_contract_to_dict,
    provider_freeze_artifact_manifest_to_dict
)

def provider_freeze_store_dir(data_root: Path) -> Path:
    return data_root / "provider_freeze"

def provider_freeze_contexts_dir(data_root: Path) -> Path:
    d = provider_freeze_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_freeze_reviews_dir(data_root: Path) -> Path:
    d = provider_freeze_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_bundles_dir(data_root: Path) -> Path:
    d = provider_freeze_store_dir(data_root) / "freeze_bundles"
    d.mkdir(parents=True, exist_ok=True)
    return d

def multi_provider_reviews_dir(data_root: Path) -> Path:
    d = provider_freeze_store_dir(data_root) / "multi_provider_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def rehearsal_reports_dir(data_root: Path) -> Path:
    d = provider_freeze_store_dir(data_root) / "rehearsal_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def output_contracts_dir(data_root: Path) -> Path:
    d = provider_freeze_store_dir(data_root) / "output_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_manifests_dir(data_root: Path) -> Path:
    d = provider_freeze_store_dir(data_root) / "manifests"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_json(path: Path, data: dict) -> Path:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def write_provider_freeze_context_json(path: Path, item: ProviderFreezeContext) -> Path:
    return _write_json(path, provider_freeze_context_to_dict(item))

def write_provider_freeze_full_review_json(path: Path, item: ProviderFreezeFullReview) -> Path:
    return _write_json(path, provider_freeze_full_review_to_dict(item))

def write_provider_expansion_freeze_bundle_json(path: Path, item: ProviderExpansionFreezeBundle) -> Path:
    return _write_json(path, provider_expansion_freeze_bundle_to_dict(item))

def write_multi_provider_final_review_json(path: Path, item: MultiProviderFinalReviewReport) -> Path:
    return _write_json(path, multi_provider_final_review_report_to_dict(item))

def write_data_layer_rehearsal_report_json(path: Path, item: DataLayerRehearsalReport) -> Path:
    return _write_json(path, data_layer_rehearsal_report_to_dict(item))

def write_data_layer_output_contract_json(path: Path, item: DataLayerOutputContract) -> Path:
    return _write_json(path, data_layer_output_contract_to_dict(item))

def write_provider_freeze_artifact_manifest_json(path: Path, item: ProviderFreezeArtifactManifest) -> Path:
    return _write_json(path, provider_freeze_artifact_manifest_to_dict(item))

def read_provider_freeze_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_provider_freeze_reviews(data_root: Path) -> List[Path]:
    d = provider_freeze_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_provider_freeze_review(data_root: Path) -> Optional[Path]:
    files = list_provider_freeze_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

def provider_freeze_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "contexts": len(list(provider_freeze_contexts_dir(data_root).glob("*.json"))),
        "reviews": len(list(provider_freeze_reviews_dir(data_root).glob("*.json"))),
        "bundles": len(list(freeze_bundles_dir(data_root).glob("*.json"))),
        "multi_provider_reviews": len(list(multi_provider_reviews_dir(data_root).glob("*.json"))),
        "rehearsals": len(list(rehearsal_reports_dir(data_root).glob("*.json"))),
        "contracts": len(list(output_contracts_dir(data_root).glob("*.json"))),
        "manifests": len(list(freeze_manifests_dir(data_root).glob("*.json")))
    }
