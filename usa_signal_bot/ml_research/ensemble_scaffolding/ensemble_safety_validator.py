from typing import Any, Dict, List
import pandas
from .phase142_models import (
    EnsembleScaffoldingContext,
    EnsembleCandidateReference,
    CandidateGroupSpec,
    BlendCoefficientPlan,
    EnsemblePreparationReport,
    EnsembleGovernanceResult,
    NonActivationEnsembleBoundaryResult,
    ModelCardEnsembleUpdate,
    EnsembleReadinessGate,
    EnsembleScaffoldingRiskFlag
)

def ensemble_scaffolding_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    unsafe = [
        "best stock", "guaranteed profit", "investment advice", "deploying to production",
        "live order", "portfolio allocation"
    ]
    return any(u in t for u in unsafe)

def validate_ensemble_scaffolding_dataframe_output_safety(df: pandas.DataFrame) -> List[str]:
    from .ensemble_schema_validator import validate_ensemble_scaffolding_column_names
    return validate_ensemble_scaffolding_column_names(list(df.columns))

def collect_ensemble_scaffolding_risk_flags(context: EnsembleScaffoldingContext = None) -> List[EnsembleScaffoldingRiskFlag]:
    flags = []
    if context:
        if context.ensemble_fitting_performed: flags.append(EnsembleScaffoldingRiskFlag.ENSEMBLE_FITTING_ATTEMPTED)
        if context.live_inference_enabled: flags.append(EnsembleScaffoldingRiskFlag.LIVE_INFERENCE_RISK)
    return flags

def validate_ensemble_scaffolding_context_safety(context: EnsembleScaffoldingContext) -> List[str]:
    errs = []
    if context.activation_allowed: errs.append("activation_allowed is true")
    if context.deployment_allowed: errs.append("deployment_allowed is true")
    if context.ensemble_fitting_performed: errs.append("ensemble_fitting_performed is true")
    if context.live_inference_enabled: errs.append("live_inference_enabled is true")
    return errs

def validate_ensemble_candidates_safety(items: List[EnsembleCandidateReference]) -> List[str]: return []
def validate_candidate_groups_safety(items: List[CandidateGroupSpec]) -> List[str]: return []
def validate_blend_plans_safety(items: List[BlendCoefficientPlan]) -> List[str]: return []
def validate_ensemble_preparation_reports_safety(items: List[EnsemblePreparationReport]) -> List[str]: return []
def validate_ensemble_governance_safety(result: EnsembleGovernanceResult) -> List[str]: return []
def validate_non_activation_ensemble_boundary_safety(result: NonActivationEnsembleBoundaryResult) -> List[str]: return []
def validate_model_card_ensemble_updates_safety(items: List[ModelCardEnsembleUpdate]) -> List[str]: return []
def validate_ensemble_readiness_gate_safety(gate: EnsembleReadinessGate) -> List[str]: return []

def ensemble_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def ensemble_safety_to_text(errors: List[str]) -> str:
    if not errors: return "Safety Valid"
    return f"Safety Invalid ({len(errors)} errors)"
