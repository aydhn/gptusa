import json
from typing import Any, Dict
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLFoundationIngestionResult,
    MLDatasetSourceReference,
    MLMatrixAssemblySpec,
    MLMatrixAssemblyResult,
    MLAssembledDatasetManifest,
    MLSplitPolicy,
    MLSplitAssignment,
    MLLeakageAuditResult,
    MLDatasetQualityProfile,
    MLSplitQualityProfile,
    MLDatasetAssemblyReadinessGate,
    MLDatasetAssemblyContext,
    MLDatasetAssemblyFullReview,
    ml_foundation_ingestion_result_to_dict,
    ml_dataset_source_reference_to_dict,
    ml_matrix_assembly_spec_to_dict,
    ml_matrix_assembly_result_to_dict,
    ml_assembled_dataset_manifest_to_dict,
    ml_split_policy_to_dict,
    ml_split_assignment_to_dict,
    ml_leakage_audit_result_to_dict,
    ml_dataset_quality_profile_to_dict,
    ml_split_quality_profile_to_dict,
    ml_dataset_assembly_readiness_gate_to_dict,
    ml_dataset_assembly_context_to_dict,
    ml_dataset_assembly_full_review_to_dict
)

def _trim(s: str, limit: int) -> str:
    if len(s) > limit:
        return s[:limit] + "..."
    return s

def ml_foundation_ingestion_result_to_text(item: MLFoundationIngestionResult) -> str:
    return json.dumps(ml_foundation_ingestion_result_to_dict(item), indent=2)

def dataset_source_reference_to_text(item: MLDatasetSourceReference) -> str:
    return json.dumps(ml_dataset_source_reference_to_dict(item), indent=2)

def matrix_assembly_spec_to_text(item: MLMatrixAssemblySpec, limit: int = 200) -> str:
    return _trim(json.dumps(ml_matrix_assembly_spec_to_dict(item), indent=2), limit)

def matrix_assembly_result_to_text(item: MLMatrixAssemblyResult, limit: int = 300) -> str:
    return _trim(json.dumps(ml_matrix_assembly_result_to_dict(item), indent=2), limit)

def assembled_dataset_manifest_to_text(item: MLAssembledDatasetManifest, limit: int = 300) -> str:
    return _trim(json.dumps(ml_assembled_dataset_manifest_to_dict(item), indent=2), limit)

def split_policy_to_text(item: MLSplitPolicy, limit: int = 300) -> str:
    return _trim(json.dumps(ml_split_policy_to_dict(item), indent=2), limit)

def split_assignment_to_text(item: MLSplitAssignment, limit: int = 300) -> str:
    return _trim(json.dumps(ml_split_assignment_to_dict(item), indent=2), limit)

def leakage_audit_result_to_text(item: MLLeakageAuditResult, limit: int = 300) -> str:
    return _trim(json.dumps(ml_leakage_audit_result_to_dict(item), indent=2), limit)

def dataset_quality_profile_to_text(item: MLDatasetQualityProfile) -> str:
    return json.dumps(ml_dataset_quality_profile_to_dict(item), indent=2)

def split_quality_profile_to_text(item: MLSplitQualityProfile, limit: int = 300) -> str:
    return _trim(json.dumps(ml_split_quality_profile_to_dict(item), indent=2), limit)

def dataset_assembly_readiness_gate_to_text(item: MLDatasetAssemblyReadinessGate, limit: int = 300) -> str:
    return _trim(json.dumps(ml_dataset_assembly_readiness_gate_to_dict(item), indent=2), limit)

def dataset_assembly_context_to_text(item: MLDatasetAssemblyContext, limit: int = 300) -> str:
    return _trim(json.dumps(ml_dataset_assembly_context_to_dict(item), indent=2), limit)

def dataset_assembly_full_review_to_text(item: MLDatasetAssemblyFullReview, limit: int = 300) -> str:
    return _trim(json.dumps(ml_dataset_assembly_full_review_to_dict(item), indent=2), limit)

def dataset_assembly_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return json.dumps(summary, indent=2)

def dataset_assembly_limitations_text() -> str:
    from usa_signal_bot.ml_research.dataset_assembly.dataset_assembly_report import dataset_assembly_limitations_text as original_limitations
    return original_limitations()
