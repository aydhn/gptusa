from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import hashlib
from .phase136_models import MLSourceArtifactReference, MLSourceRegistry, MLSourceArtifactKind, MLFoundationQuality, create_ml_source_registry_id, create_ml_source_artifact_reference_id

def required_ml_source_artifact_kinds() -> List[MLSourceArtifactKind]:
    return [
        MLSourceArtifactKind.FROZEN_FEATURE_TABLE,
        MLSourceArtifactKind.FACTOR_TABLE,
        MLSourceArtifactKind.REGIME_FEATURE_TABLE,
        MLSourceArtifactKind.REGIME_LABEL_TABLE,
        MLSourceArtifactKind.MARKET_DATA_TABLE,
        MLSourceArtifactKind.BENCHMARK_TABLE,
        MLSourceArtifactKind.TRANSITION_DIAGNOSTICS,
        MLSourceArtifactKind.MARKET_BEHAVIOR_PROFILE,
        MLSourceArtifactKind.ALIGNMENT_COMPATIBILITY_RESULT,
        MLSourceArtifactKind.CONTEXT_VALIDATION_RESULT,
        MLSourceArtifactKind.MONITORING_DRIFT_RESULT,
        MLSourceArtifactKind.RESEARCH_FREEZE_PACKAGE,
        MLSourceArtifactKind.FINAL_CLOSURE_SEAL
    ]

def build_ml_source_artifact_references(ml_input_contract_payload: Optional[Dict[str, Any]], final_closure_payload: Optional[Dict[str, Any]] = None) -> List[MLSourceArtifactReference]:
    refs = []
    now = datetime.now(timezone.utc).isoformat()
    for kind in required_ml_source_artifact_kinds():
        refs.append(MLSourceArtifactReference(
            reference_id=create_ml_source_artifact_reference_id(),
            created_at_utc=now,
            artifact_kind=kind,
            artifact_name=kind.value,
            source_phase=135,
            source_path=None,
            source_hash=None,
            schema_signature=None,
            lineage_reference=None,
            required=True,
            available=True,
            read_only=True,
            frozen=True,
            allowed_for_ml_research=True,
            contains_features=True if "FEATURE" in kind.value else False,
            contains_targets=False,
            contains_labels=True if "LABEL" in kind.value else False,
            contains_trade_signals=False,
            contains_order_decisions=False,
            contains_portfolio_weights=False,
            research_metadata_only=True
        ))
    return refs

def build_ml_source_registry(references: List[MLSourceArtifactReference]) -> MLSourceRegistry:
    now = datetime.now(timezone.utc).isoformat()
    req_count = len(required_ml_source_artifact_kinds())
    avail_count = len([r for r in references if r.available])
    missing = req_count - avail_count
    valid = missing == 0
    return MLSourceRegistry(
        registry_id=create_ml_source_registry_id(),
        created_at_utc=now,
        source_references=references,
        required_source_count=req_count,
        available_required_source_count=avail_count,
        missing_required_source_count=missing,
        registry_hash=None,
        registry_valid=valid,
        quality=MLFoundationQuality.HIGH if valid else MLFoundationQuality.INVALID,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

def validate_ml_source_artifact_references(references: List[MLSourceArtifactReference]) -> List[str]:
    return []

def validate_ml_source_registry(registry: MLSourceRegistry) -> List[str]:
    return []

def compute_ml_source_registry_hash(registry: MLSourceRegistry) -> str:
    return hashlib.sha256(registry.registry_id.encode()).hexdigest()

def ml_source_registry_summary(registry: MLSourceRegistry) -> Dict[str, Any]:
    return {"valid": registry.registry_valid}

def ml_source_registry_to_text(registry: MLSourceRegistry, limit: int = 300) -> str:
    return f"Registry {registry.registry_id} valid: {registry.registry_valid}"
