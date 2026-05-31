from typing import Any, Dict
from .phase136_models import (
    RegimeFinalClosureIngestionResult, MLSourceArtifactReference, MLSourceRegistry,
    MLFeatureContract, MLTargetContract, MLLabelContract, MLDatasetContract,
    MLLeakageGuardResult, MLNonActivationBoundaryResult, MLResearchGovernanceResult,
    MLFoundationReadinessGate, MLFoundationContext, MLFoundationFullReview
)

def regime_final_closure_ingestion_result_to_text(item: RegimeFinalClosureIngestionResult) -> str:
    return f"Ingestion ID: {item.ingestion_id}\nValid: {item.valid_for_phase136}"

def ml_source_artifact_reference_to_text(item: MLSourceArtifactReference) -> str:
    return f"Ref: {item.artifact_name} - Available: {item.available}"

def ml_source_registry_to_text(item: MLSourceRegistry, limit: int = 300) -> str:
    return f"Registry ID: {item.registry_id}\nValid: {item.registry_valid}"

def ml_feature_contract_to_text(item: MLFeatureContract) -> str:
    return f"Feature: {item.feature_name} - Role: {item.feature_role.value}"

def ml_target_contract_to_text(item: MLTargetContract) -> str:
    return f"Target: {item.target_name} - Kind: {item.target_kind.value}"

def ml_label_contract_to_text(item: MLLabelContract) -> str:
    return f"Label: {item.label_name} - Kind: {item.label_kind.value}"

def ml_dataset_contract_to_text(item: MLDatasetContract, limit: int = 300) -> str:
    return f"Dataset Contract ID: {item.dataset_contract_id}\nValid: {item.contract_valid}"

def ml_leakage_guard_result_to_text(item: MLLeakageGuardResult, limit: int = 300) -> str:
    return f"Leakage Guard Passed: {item.leakage_guard_passed}"

def ml_non_activation_boundary_result_to_text(item: MLNonActivationBoundaryResult, limit: int = 300) -> str:
    return f"Non-Activation Boundary Passed: {item.boundary_passed}"

def ml_research_governance_result_to_text(item: MLResearchGovernanceResult, limit: int = 300) -> str:
    return f"Governance Passed: {item.governance_passed}"

def ml_foundation_readiness_gate_to_text(item: MLFoundationReadinessGate, limit: int = 300) -> str:
    return f"Readiness Gate Status: {item.status.value}"

def ml_foundation_context_to_text(item: MLFoundationContext, limit: int = 300) -> str:
    return f"Context ID: {item.context_id}\nReady for Phase 137: {item.ready_for_phase137}"

def ml_foundation_full_review_to_text(item: MLFoundationFullReview, limit: int = 300) -> str:
    return f"Review ID: {item.review_id}\nReady for Phase 137: {item.readiness_gate.ready_for_phase137}"

def ml_foundation_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Reviews: {summary.get('reviews_count', 0)}"

def ml_foundation_limitations_text() -> str:
    return "Phase 136 is for ML dataset contract and governance boundary only. It performs no model training, prediction, or trading."
