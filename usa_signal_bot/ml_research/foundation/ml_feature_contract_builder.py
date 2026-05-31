from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from .phase136_models import MLFeatureContract, MLSourceRegistry, MLSourceArtifactReference, MLFeatureRole, create_ml_feature_contract_id

def infer_feature_role_from_name(name: str) -> MLFeatureRole:
    name_l = name.lower()
    if "symbol" in name_l: return MLFeatureRole.IDENTIFIER
    if "date" in name_l or "time" in name_l: return MLFeatureRole.TIMESTAMP
    return MLFeatureRole.INPUT_FEATURE

def build_feature_contract_for_source(ref: MLSourceArtifactReference, feature_name: str, source_column: Optional[str] = None) -> MLFeatureContract:
    now = datetime.now(timezone.utc).isoformat()
    return MLFeatureContract(
        contract_id=create_ml_feature_contract_id(),
        created_at_utc=now,
        feature_name=feature_name,
        feature_role=infer_feature_role_from_name(feature_name),
        source_artifact_kind=ref.artifact_kind,
        source_column=source_column or feature_name,
        dtype_hint="float64",
        nullable_allowed=True,
        missing_value_policy="drop",
        scaling_allowed_later=True,
        feature_selection_allowed_later=True,
        read_only_source=True,
        leakage_sensitive=True,
        allowed_for_phase137_dataset_assembly=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_default_ml_feature_contracts(registry: MLSourceRegistry) -> List[MLFeatureContract]:
    contracts = []
    if registry.source_references:
        contracts.append(build_feature_contract_for_source(registry.source_references[0], "symbol"))
        contracts.append(build_feature_contract_for_source(registry.source_references[0], "timestamp"))
        contracts.append(build_feature_contract_for_source(registry.source_references[0], "close_price"))
    return contracts

def validate_ml_feature_contracts(items: List[MLFeatureContract]) -> List[str]:
    return []

def ml_feature_contracts_summary(items: List[MLFeatureContract]) -> Dict[str, Any]:
    return {"count": len(items)}

def ml_feature_contracts_to_text(items: List[MLFeatureContract], limit: int = 300) -> str:
    return f"{len(items)} feature contracts"
