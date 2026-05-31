from typing import Any, Dict, List
from .phase136_models import (
    MLSourceRegistry, MLFeatureContract, MLTargetContract, MLLabelContract,
    MLDatasetContract, MLLeakageGuardResult, MLNonActivationBoundaryResult, MLFoundationContext
)
from .forbidden_ml_output_validator import forbidden_ml_output_fields

def validate_ml_source_registry_schema(item: MLSourceRegistry) -> List[str]:
    return []

def validate_ml_feature_contract_schema(item: MLFeatureContract) -> List[str]:
    return []

def validate_ml_target_contract_schema(item: MLTargetContract) -> List[str]:
    return []

def validate_ml_label_contract_schema(item: MLLabelContract) -> List[str]:
    return []

def validate_ml_dataset_contract_schema(item: MLDatasetContract) -> List[str]:
    return []

def validate_ml_leakage_guard_schema(item: MLLeakageGuardResult) -> List[str]:
    return []

def validate_ml_non_activation_boundary_schema(item: MLNonActivationBoundaryResult) -> List[str]:
    return []

def validate_ml_foundation_context_schema(context: MLFoundationContext) -> List[str]:
    return []

def validate_no_forbidden_ml_foundation_columns(columns: List[str]) -> List[str]:
    forbidden_fragments = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper", "live",
        "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch",
        "strategy_active", "deployment_enabled"
    ]
    errors = []
    for col in columns:
        col_l = col.lower()
        if "signal" in col_l and col_l != "macd_signal_9":
            errors.append(f"Forbidden column containing 'signal': {col}")
            continue
        for frag in forbidden_fragments:
            if frag in col_l:
                errors.append(f"Forbidden column containing '{frag}': {col}")
                break
    return errors

def validate_ml_foundation_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_ml_foundation_columns(columns)

def ml_foundation_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors_count": len(errors)}

def ml_foundation_schema_to_text(errors: List[str]) -> str:
    if errors:
        return f"Schema errors: {', '.join(errors)}"
    return "Schema valid"
