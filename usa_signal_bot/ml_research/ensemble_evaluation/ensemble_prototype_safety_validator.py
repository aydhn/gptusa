from typing import Any, Dict, List
import pandas as pd

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeContext,
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    BlendContributionDiagnostic,
    OfflineEnsembleEvaluationReport,
    NonActivationEnsembleRegistry,
    EnsembleModelCardUpdate,
    EnsemblePrototypeBoundaryResult,
    EnsemblePrototypeReadinessGate,
    EnsemblePrototypeRiskFlag
)
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_schema_validator import validate_no_forbidden_ensemble_evaluation_columns

def validate_ensemble_prototype_context_safety(context: EnsemblePrototypeContext) -> List[str]:
    errors = []
    if context.activation_allowed: errors.append("Activation allowed")
    if context.deployment_allowed: errors.append("Deployment allowed")
    if context.live_inference_enabled: errors.append("Live inference enabled")
    return errors

def validate_ensemble_prototype_specs_safety(items: List[EnsemblePrototypeSpec]) -> List[str]: return []
def validate_offline_ensemble_predictions_safety(items: List[OfflineEnsemblePredictionArtifact]) -> List[str]: return []
def validate_blend_diagnostics_safety(items: List[BlendContributionDiagnostic]) -> List[str]: return []
def validate_ensemble_evaluation_reports_safety(items: List[OfflineEnsembleEvaluationReport]) -> List[str]: return []
def validate_non_activation_ensemble_registry_safety(registry: NonActivationEnsembleRegistry) -> List[str]: return []
def validate_ensemble_model_card_updates_safety(items: List[EnsembleModelCardUpdate]) -> List[str]: return []
def validate_ensemble_prototype_boundary_safety(result: EnsemblePrototypeBoundaryResult) -> List[str]: return []
def validate_ensemble_prototype_readiness_gate_safety(gate: EnsemblePrototypeReadinessGate) -> List[str]: return []

def validate_ensemble_prototype_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    return validate_no_forbidden_ensemble_evaluation_columns(list(df.columns))

def ensemble_prototype_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    unsafe = ["guaranteed profit", "best stock", "deploy", "portfolio allocation", "buy now"]
    return any(u in t for u in unsafe)

def collect_ensemble_prototype_risk_flags(context: EnsemblePrototypeContext | None = None) -> List[EnsemblePrototypeRiskFlag]:
    flags = []
    if context:
        flags.extend(context.risk_flags)
    return list(set(flags))

def ensemble_prototype_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safety_error_count": len(errors)}

def ensemble_prototype_safety_to_text(errors: List[str]) -> str:
    return str(ensemble_prototype_safety_summary(errors))
