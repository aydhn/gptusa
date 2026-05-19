from pathlib import Path
import json
from typing import Any, Dict, List
from usa_signal_bot.release_packaging.packaging_models import BundleManifest, FrozenArtifact, BundleValidationResult, VersionedCandidateBundle, bundle_manifest_to_dict, frozen_artifact_to_dict, bundle_validation_result_to_dict, versioned_candidate_bundle_to_dict

def bundle_root_dir(data_root: Path) -> Path:
    return data_root / "release_bundles"

def bundle_dir(data_root: Path, bundle_id: str, bundle_version: str) -> Path:
    return bundle_root_dir(data_root) / bundle_id / bundle_version

def write_bundle_manifest(path: Path, manifest: BundleManifest) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bundle_manifest_to_dict(manifest), f, indent=2)
    return path

def write_frozen_artifacts(path: Path, artifacts: List[FrozenArtifact]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for a in artifacts:
            f.write(json.dumps(frozen_artifact_to_dict(a)) + "\n")
    return path

def write_bundle_validation(path: Path, validation: BundleValidationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bundle_validation_result_to_dict(validation), f, indent=2)
    return path

def write_bundle_readme(path: Path, readme_text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(readme_text)
    return path

def write_versioned_candidate_bundle(data_root: Path, bundle: VersionedCandidateBundle) -> VersionedCandidateBundle:
    bdir = bundle_dir(data_root, bundle.bundle_id, bundle.bundle_version)
    bdir.mkdir(parents=True, exist_ok=True)

    if bundle.manifest:
        write_bundle_manifest(bdir / "manifest.json", bundle.manifest)
        write_frozen_artifacts(bdir / "artifacts.jsonl", bundle.manifest.artifacts)

    if bundle.validation_result:
        write_bundle_validation(bdir / "validation.json", bundle.validation_result)

    from usa_signal_bot.release_packaging.bundle_readme import generate_bundle_readme
    readme = generate_bundle_readme(bundle)
    bundle.readme_path = str(write_bundle_readme(bdir / "README.md", readme))

    bpath = bdir / "bundle.json"
    bundle.bundle_path = str(bpath)
    with open(bpath, "w", encoding="utf-8") as f:
        json.dump(versioned_candidate_bundle_to_dict(bundle), f, indent=2)

    return bundle

def bundle_writer_summary(bundle: VersionedCandidateBundle) -> Dict[str, Any]:
    return {"bundle_id": bundle.bundle_id, "path": bundle.bundle_path}
