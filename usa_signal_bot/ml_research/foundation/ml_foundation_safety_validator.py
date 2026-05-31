from typing import Any, Dict, List, Optional
from .phase136_models import (
    MLFoundationContext, MLSourceRegistry, MLDatasetContract, MLLeakageGuardResult,
    MLNonActivationBoundaryResult, MLResearchGovernanceResult, MLFoundationReadinessGate,
    MLFoundationRiskFlag
)
try:
    import pandas
except ImportError:
    pass

def validate_ml_foundation_context_safety(context: MLFoundationContext) -> List[str]:
    errors = []
    if context.activation_allowed: errors.append("activation_allowed is true")
    if context.deployment_allowed: errors.append("deployment_allowed is true")
    if context.model_training_used: errors.append("model_training_used is true")
    return errors

def validate_ml_source_registry_safety(registry: MLSourceRegistry) -> List[str]:
    errors = []
    if registry.activation_allowed: errors.append("activation_allowed is true")
    return errors

def validate_ml_dataset_contract_safety(contract: MLDatasetContract) -> List[str]:
    errors = []
    if contract.activation_allowed: errors.append("activation_allowed is true")
    return errors

def validate_ml_leakage_guard_safety(result: MLLeakageGuardResult) -> List[str]:
    errors = []
    if result.activation_allowed: errors.append("activation_allowed is true")
    return errors

def validate_ml_non_activation_boundary_safety(result: MLNonActivationBoundaryResult) -> List[str]:
    errors = []
    if not result.no_model_training_in_phase136: errors.append("Model training in Phase 136")
    return errors

def validate_ml_governance_safety(result: MLResearchGovernanceResult) -> List[str]:
    errors = []
    if not result.local_only: errors.append("Not local only")
    return errors

def validate_ml_foundation_readiness_gate_safety(gate: MLFoundationReadinessGate) -> List[str]:
    errors = []
    if gate.activation_allowed: errors.append("activation_allowed is true")
    return errors

def validate_ml_foundation_dataframe_output_safety(df: Any) -> List[str]:
    return []

def ml_foundation_text_has_trade_or_execution_language(text: str) -> bool:
    text_l = text.lower()
    forbidden = ["buy_signal", "sell_signal", "kesin al", "kesin sat", "garanti kâr", "emir gönderildi"]
    return any(f in text_l for f in forbidden)

def collect_ml_foundation_risk_flags(context: Optional[MLFoundationContext] = None) -> List[MLFoundationRiskFlag]:
    return []

def ml_foundation_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors_count": len(errors)}

def ml_foundation_safety_to_text(errors: List[str]) -> str:
    if errors:
        return f"Safety errors: {', '.join(errors)}"
    return "Safety valid"
