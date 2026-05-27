import json
from pathlib import Path
from typing import Any
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorValidationContext,
    FactorValidationFullReview,
    FactorValidationResult,
    FactorDriftBaseline,
    FactorDriftReport,
    FactorSchemaSignature,
    FactorVersionMetadata,
    FactorArtifactManifest,
    FactorStoreSnapshot,
    FactorStoreHardeningResult,
    factor_validation_context_to_dict,
    factor_validation_full_review_to_dict,
    factor_validation_result_to_dict,
    factor_drift_baseline_to_dict,
    factor_drift_report_to_dict,
    factor_schema_signature_to_dict,
    factor_version_metadata_to_dict,
    factor_artifact_manifest_to_dict,
    factor_store_snapshot_to_dict,
    factor_store_hardening_result_to_dict
)

def _mkdir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def factor_validation_store_dir(data_root: Path) -> Path:
    return _mkdir(data_root / "feature_engine" / "factor_validation")

def factor_validation_contexts_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "contexts")

def factor_validation_reviews_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "reviews")

def factor_validation_results_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "validation_results")

def factor_drift_baselines_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "drift_baselines")

def factor_drift_reports_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "drift_reports")

def factor_schema_signatures_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "schema_signatures")

def factor_versions_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "versions")

def factor_manifests_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "manifests")

def factor_snapshots_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "snapshots")

def factor_hardening_dir(data_root: Path) -> Path:
    return _mkdir(factor_validation_store_dir(data_root) / "hardening")

def write_factor_validation_context_json(path: Path, item: FactorValidationContext) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_validation_context_to_dict(item), f, indent=2)
    return path

def write_factor_validation_full_review_json(path: Path, item: FactorValidationFullReview) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_validation_full_review_to_dict(item), f, indent=2)
    return path

def write_factor_validation_results_jsonl(path: Path, items: list[FactorValidationResult]) -> Path:
    with open(path, 'w') as f:
        for i in items:
            f.write(json.dumps(factor_validation_result_to_dict(i)) + '\n')
    return path

def write_factor_drift_baselines_jsonl(path: Path, items: list[FactorDriftBaseline]) -> Path:
    with open(path, 'w') as f:
        for i in items:
            f.write(json.dumps(factor_drift_baseline_to_dict(i)) + '\n')
    return path

def write_factor_drift_reports_jsonl(path: Path, items: list[FactorDriftReport]) -> Path:
    with open(path, 'w') as f:
        for i in items:
            f.write(json.dumps(factor_drift_report_to_dict(i)) + '\n')
    return path

def write_factor_schema_signatures_jsonl(path: Path, items: list[FactorSchemaSignature]) -> Path:
    with open(path, 'w') as f:
        for i in items:
            f.write(json.dumps(factor_schema_signature_to_dict(i)) + '\n')
    return path

def write_factor_version_metadata_json(path: Path, item: FactorVersionMetadata) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_version_metadata_to_dict(item), f, indent=2)
    return path

def write_factor_artifact_manifest_json(path: Path, item: FactorArtifactManifest) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_artifact_manifest_to_dict(item), f, indent=2)
    return path

def write_factor_store_snapshot_json(path: Path, item: FactorStoreSnapshot) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_store_snapshot_to_dict(item), f, indent=2)
    return path

def write_factor_store_hardening_json(path: Path, item: FactorStoreHardeningResult) -> Path:
    with open(path, 'w') as f:
        json.dump(factor_store_hardening_result_to_dict(item), f, indent=2)
    return path

def read_factor_validation_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def list_factor_validation_reviews(data_root: Path) -> list[Path]:
    d = factor_validation_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_factor_validation_review(data_root: Path) -> Path | None:
    l = list_factor_validation_reviews(data_root)
    if not l: return None
    return sorted(l, key=lambda x: x.stat().st_mtime)[-1]

def factor_validation_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews": len(list_factor_validation_reviews(data_root))}
