from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLAssembledDatasetManifest,
    MLMatrixAssemblyResult,
    MLDatasetSourceReference,
    MLDatasetAssemblyQuality,
    create_ml_assembled_dataset_manifest_id,
    ml_assembled_dataset_manifest_to_dict
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def infer_common_time_range(results: List[MLMatrixAssemblyResult]) -> Dict[str, Any]:
    return {"min_time": "unknown", "max_time": "unknown"}

def infer_common_symbol_count(results: List[MLMatrixAssemblyResult]) -> int:
    return 0

def compute_dataset_manifest_hash(manifest: MLAssembledDatasetManifest) -> str:
    d = ml_assembled_dataset_manifest_to_dict(manifest)
    d.pop("manifest_hash", None)
    s = json.dumps(d, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def build_assembled_dataset_manifest(
    feature_result: MLMatrixAssemblyResult,
    target_result: MLMatrixAssemblyResult,
    label_result: MLMatrixAssemblyResult,
    source_refs: List[MLDatasetSourceReference],
    dataset_contract_payload: Optional[Dict[str, Any]] = None
) -> MLAssembledDatasetManifest:

    manifest = MLAssembledDatasetManifest(
        manifest_id=create_ml_assembled_dataset_manifest_id(),
        created_at_utc=_now(),
        manifest_version="1.0.0",
        feature_matrix=feature_result,
        target_matrix=target_result,
        label_matrix=label_result,
        source_refs=source_refs,
        total_row_count=max(feature_result.row_count, target_result.row_count, label_result.row_count),
        feature_count=feature_result.column_count,
        target_count=target_result.column_count,
        label_count=label_result.column_count,
        common_time_range=infer_common_time_range([feature_result, target_result, label_result]),
        common_symbol_count=infer_common_symbol_count([feature_result, target_result, label_result])
    )

    if dataset_contract_payload:
        s = json.dumps(dataset_contract_payload, sort_keys=True)
        manifest.dataset_contract_hash = hashlib.sha256(s.encode('utf-8')).hexdigest()

    errors = validate_dataset_manifest(manifest)
    if not errors:
        manifest.manifest_valid = True
        manifest.quality = MLDatasetAssemblyQuality.ACCEPTABLE
    else:
        manifest.errors.extend(errors)

    manifest.manifest_hash = compute_dataset_manifest_hash(manifest)

    return manifest

def validate_dataset_manifest(manifest: MLAssembledDatasetManifest) -> List[str]:
    errors = []
    if not manifest.feature_matrix.assembly_valid:
        errors.append("Feature matrix is invalid")
    if not manifest.target_matrix.assembly_valid:
        errors.append("Target matrix is invalid")
    if not manifest.label_matrix.assembly_valid:
        errors.append("Label matrix is invalid")

    if manifest.activation_allowed or manifest.strategy_activation_allowed or manifest.deployment_allowed:
        errors.append("Manifest contains forbidden deployment flags")
    return errors

def dataset_manifest_summary(manifest: MLAssembledDatasetManifest) -> Dict[str, Any]:
    return {
        "manifest_id": manifest.manifest_id,
        "valid": manifest.manifest_valid,
        "total_row_count": manifest.total_row_count,
        "feature_count": manifest.feature_count,
        "target_count": manifest.target_count,
        "label_count": manifest.label_count,
        "errors": manifest.errors
    }

def dataset_manifest_to_text(manifest: MLAssembledDatasetManifest, limit: int = 300) -> str:
    s = json.dumps(dataset_manifest_summary(manifest), indent=2)
    if len(s) > limit:
        return s[:limit] + "..."
    return s
