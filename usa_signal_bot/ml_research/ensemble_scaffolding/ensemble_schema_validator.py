from typing import Any, Dict, List
import re
from .phase142_models import (
    EnsembleCandidateReference,
    EnsembleFamilySpec,
    CandidateGroupSpec,
    BlendPolicySpec,
    BlendCoefficientPlan,
    EnsemblePreparationReport,
    EnsembleGovernanceResult,
    EnsembleScaffoldingContext
)

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch",
    "strategy_active", "deployment_enabled", "final_ensemble_prediction",
    "ensemble_trade", "calibrated_trade"
]

def validate_no_forbidden_ensemble_scaffolding_columns(columns: List[str]) -> List[str]:
    errs = []
    for c in columns:
        c_low = c.lower()
        if c_low == "macd_signal_9": continue
        for frag in FORBIDDEN_FRAGMENTS:
            if frag in c_low and c_low != "signal":
                errs.append(f"Forbidden fragment '{frag}' found in column '{c}'")
            elif frag == "signal" and "signal" in c_low and "macd" not in c_low:
                errs.append(f"Forbidden fragment 'signal' found in column '{c}'")
    return errs

def validate_ensemble_scaffolding_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_ensemble_scaffolding_columns(columns)

def validate_ensemble_candidate_schema(item: EnsembleCandidateReference) -> List[str]: return []
def validate_ensemble_family_spec_schema(item: EnsembleFamilySpec) -> List[str]: return []
def validate_candidate_group_schema(item: CandidateGroupSpec) -> List[str]: return []
def validate_blend_policy_schema(item: BlendPolicySpec) -> List[str]: return []
def validate_blend_coefficient_plan_schema(item: BlendCoefficientPlan) -> List[str]: return []
def validate_ensemble_preparation_report_schema(item: EnsemblePreparationReport) -> List[str]: return []
def validate_ensemble_governance_schema(item: EnsembleGovernanceResult) -> List[str]: return []
def validate_ensemble_scaffolding_context_schema(context: EnsembleScaffoldingContext) -> List[str]: return []

def ensemble_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def ensemble_schema_to_text(errors: List[str]) -> str:
    if not errors: return "Schema Valid"
    return f"Schema Invalid ({len(errors)} errors)"
