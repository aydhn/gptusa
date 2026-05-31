import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetAssemblyContext,
    MLDatasetAssemblyFullReview,
    MLDatasetSourceReference,
    MLMatrixAssemblyResult,
    MLAssembledDatasetManifest,
    MLSplitPolicy,
    MLSplitAssignment,
    MLLeakageAuditResult,
    MLDatasetQualityProfile,
    MLSplitQualityProfile,
    MLDatasetAssemblyReadinessGate,
    ml_dataset_assembly_context_to_dict,
    ml_dataset_assembly_full_review_to_dict,
    ml_dataset_source_reference_to_dict,
    ml_matrix_assembly_result_to_dict,
    ml_assembled_dataset_manifest_to_dict,
    ml_split_policy_to_dict,
    ml_split_assignment_to_dict,
    ml_leakage_audit_result_to_dict,
    ml_dataset_quality_profile_to_dict,
    ml_split_quality_profile_to_dict,
    ml_dataset_assembly_readiness_gate_to_dict
)

def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def dataset_assembly_store_dir(data_root: Path) -> Path:
    return _ensure_dir(data_root / "ml_research" / "dataset_assembly")

def dataset_assembly_contexts_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "contexts")

def dataset_assembly_reviews_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "reviews")

def dataset_source_refs_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "source_refs")

def matrix_results_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "matrix_results")

def dataset_manifests_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "manifests")

def split_policies_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "split_policies")

def split_assignments_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "split_assignments")

def leakage_audits_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "leakage_audits")

def dataset_quality_profiles_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "dataset_quality")

def split_quality_profiles_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "split_quality")

def dataset_assembly_gates_dir(data_root: Path) -> Path:
    return _ensure_dir(dataset_assembly_store_dir(data_root) / "readiness_gates")

def write_dataset_assembly_context_json(path: Path, item: MLDatasetAssemblyContext) -> Path:
    with open(path, "w") as f:
        json.dump(ml_dataset_assembly_context_to_dict(item), f, indent=2)
    return path

def write_dataset_assembly_full_review_json(path: Path, item: MLDatasetAssemblyFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(ml_dataset_assembly_full_review_to_dict(item), f, indent=2)
    return path

def write_dataset_source_refs_jsonl(path: Path, items: List[MLDatasetSourceReference]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(ml_dataset_source_reference_to_dict(item)) + "\n")
    return path

def write_matrix_assembly_result_json(path: Path, item: MLMatrixAssemblyResult) -> Path:
    with open(path, "w") as f:
        json.dump(ml_matrix_assembly_result_to_dict(item), f, indent=2)
    return path

def write_dataset_manifest_json(path: Path, item: MLAssembledDatasetManifest) -> Path:
    with open(path, "w") as f:
        json.dump(ml_assembled_dataset_manifest_to_dict(item), f, indent=2)
    return path

def write_split_policy_json(path: Path, item: MLSplitPolicy) -> Path:
    with open(path, "w") as f:
        json.dump(ml_split_policy_to_dict(item), f, indent=2)
    return path

def write_split_assignment_json(path: Path, item: MLSplitAssignment) -> Path:
    with open(path, "w") as f:
        json.dump(ml_split_assignment_to_dict(item), f, indent=2)
    return path

def write_leakage_audit_json(path: Path, item: MLLeakageAuditResult) -> Path:
    with open(path, "w") as f:
        json.dump(ml_leakage_audit_result_to_dict(item), f, indent=2)
    return path

def write_dataset_quality_profiles_jsonl(path: Path, items: List[MLDatasetQualityProfile]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(ml_dataset_quality_profile_to_dict(item)) + "\n")
    return path

def write_split_quality_profile_json(path: Path, item: MLSplitQualityProfile) -> Path:
    with open(path, "w") as f:
        json.dump(ml_split_quality_profile_to_dict(item), f, indent=2)
    return path

def write_dataset_assembly_readiness_gate_json(path: Path, item: MLDatasetAssemblyReadinessGate) -> Path:
    with open(path, "w") as f:
        json.dump(ml_dataset_assembly_readiness_gate_to_dict(item), f, indent=2)
    return path

def read_dataset_assembly_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_dataset_assembly_reviews(data_root: Path) -> List[Path]:
    d = dataset_assembly_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda x: x.stat().st_mtime, reverse=True)

def get_latest_dataset_assembly_review(data_root: Path) -> Optional[Path]:
    l = list_dataset_assembly_reviews(data_root)
    return l[0] if l else None

def dataset_assembly_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_dataset_assembly_reviews(data_root)),
        "contexts_count": len(list(dataset_assembly_contexts_dir(data_root).glob("*.json")))
    }
