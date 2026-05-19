from pathlib import Path
import json
from typing import Any, Dict, List, Optional
from usa_signal_bot.release_packaging.packaging_models import FrozenArtifact, BundleManifest, BundleValidationResult, VersionedCandidateBundle, ReleasePackagingReview
from usa_signal_bot.release_packaging.packaging_models import release_packaging_review_to_dict

def packaging_store_dir(data_root: Path) -> Path:
    return data_root / "release_packaging"

def bundles_dir(data_root: Path) -> Path:
    return packaging_store_dir(data_root) / "bundles"

def manifests_dir(data_root: Path) -> Path:
    return packaging_store_dir(data_root) / "manifests"

def frozen_artifacts_dir(data_root: Path) -> Path:
    return packaging_store_dir(data_root) / "frozen_artifacts"

def validation_results_dir(data_root: Path) -> Path:
    return packaging_store_dir(data_root) / "validation_results"

def packaging_reviews_dir(data_root: Path) -> Path:
    return packaging_store_dir(data_root) / "reviews"

def write_frozen_artifacts_jsonl(path: Path, items: List[FrozenArtifact]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for i in items:
            f.write(json.dumps({"id": i.artifact_id}) + "\n") # Simplified for test mock
    return path

def write_bundle_manifest_json(path: Path, item: BundleManifest) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"id": item.manifest_id}, f)
    return path

def write_bundle_validation_result_json(path: Path, item: BundleValidationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"id": item.validation_id}, f)
    return path

def write_versioned_candidate_bundle_json(path: Path, item: VersionedCandidateBundle) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"id": item.bundle_id}, f)
    return path

def write_release_packaging_review_json(path: Path, item: ReleasePackagingReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(release_packaging_review_to_dict(item), f, indent=2)
    return path

def read_release_packaging_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_release_packaging_reviews(data_root: Path) -> List[Path]:
    d = packaging_reviews_dir(data_root)
    if not d.exists():
        return []
    return list(d.glob("*.json"))

def get_latest_release_packaging_review(data_root: Path) -> Optional[Path]:
    files = list_release_packaging_reviews(data_root)
    if not files:
        return None
    return sorted(files)[-1]

def packaging_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_release_packaging_reviews(data_root))}
