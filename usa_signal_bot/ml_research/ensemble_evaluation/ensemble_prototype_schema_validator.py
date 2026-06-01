from typing import Any, Dict, List
import pandas as pd

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    BlendContributionDiagnostic,
    CandidateAgreementDiagnostic,
    EnsembleCandidateComparisonResult,
    OfflineEnsembleEvaluationReport,
    NonActivationEnsembleRegistry,
    EnsemblePrototypeContext
)

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch",
    "strategy_active", "deployment_enabled", "ensemble_trade", "calibrated_trade"
]

def validate_ensemble_prototype_spec_schema(item: EnsemblePrototypeSpec) -> List[str]: return []
def validate_offline_ensemble_prediction_artifact_schema(item: OfflineEnsemblePredictionArtifact) -> List[str]: return []
def validate_blend_contribution_diagnostic_schema(item: BlendContributionDiagnostic) -> List[str]: return []
def validate_candidate_agreement_diagnostic_schema(item: CandidateAgreementDiagnostic) -> List[str]: return []
def validate_ensemble_candidate_comparison_schema(item: EnsembleCandidateComparisonResult) -> List[str]: return []
def validate_offline_ensemble_evaluation_report_schema(item: OfflineEnsembleEvaluationReport) -> List[str]: return []
def validate_non_activation_ensemble_registry_schema(item: NonActivationEnsembleRegistry) -> List[str]: return []
def validate_ensemble_prototype_context_schema(context: EnsemblePrototypeContext) -> List[str]: return []

def validate_ensemble_evaluation_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_ensemble_evaluation_columns(columns)

def validate_no_forbidden_ensemble_evaluation_columns(columns: List[str]) -> List[str]:
    errors = []
    for c in columns:
        cl = c.lower()
        if "signal" in cl and "macd_signal_9" not in cl:
             errors.append(f"Forbidden fragment 'signal' in {c}")
        for f in FORBIDDEN_FRAGMENTS:
            if f in cl and f != "signal":
                errors.append(f"Forbidden fragment '{f}' in {c}")
    return errors

def ensemble_prototype_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def ensemble_prototype_schema_to_text(errors: List[str]) -> str:
    return str(ensemble_prototype_schema_summary(errors))
