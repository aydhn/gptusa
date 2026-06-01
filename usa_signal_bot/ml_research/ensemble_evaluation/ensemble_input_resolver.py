import pandas as pd
import datetime
from typing import Any, Dict, List

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeInputReference,
    create_ensemble_prototype_input_reference_id,
    EnsemblePrototypeRiskFlag
)

def build_ensemble_prototype_input_references(
    preparation_reports: List[Dict[str, Any]],
    candidates: List[Dict[str, Any]],
    groups: List[Dict[str, Any]],
    blend_plans: List[Dict[str, Any]],
    prediction_artifacts: List[Dict[str, Any]]
) -> List[EnsemblePrototypeInputReference]:

    refs = []

    for plan in blend_plans:
        refs.append(EnsemblePrototypeInputReference(
            input_ref_id=create_ensemble_prototype_input_reference_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            source_artifact_name="blend_plan",
            source_artifact_kind="JSON",
            source_path=None,
            source_hash=None,
            candidate_ref_id=None,
            candidate_group_id=plan.get("candidate_group_id"),
            blend_plan_id=plan.get("blend_plan_id"),
            prediction_artifact_id=None,
            available=True,
            read_only=True,
            research_data_only=True,
            offline_ml_research_only=True,
            contains_forbidden_outputs=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    return refs

def resolve_prediction_frame_for_group(group_payload: Dict[str, Any], prediction_df: pd.DataFrame) -> pd.DataFrame:
    # Just a placeholder, returns original DF for now
    return prediction_df

def validate_ensemble_prototype_inputs(refs: List[EnsemblePrototypeInputReference]) -> List[str]:
    errors = []
    for ref in refs:
        if not ref.research_data_only:
             errors.append("Reference is not research data only.")
    return errors

def validate_prediction_frame_for_ensemble(df: pd.DataFrame) -> List[str]:
    errors = []
    required = ["symbol", "timestamp", "split_name"]
    # We skip strict validation if empty
    if not df.empty:
         for r in required:
             if r not in df.columns:
                 errors.append(f"Missing required column {r}")

         forbidden = ["buy", "sell", "order", "portfolio_weight", "allocation", "live_order"]
         for c in df.columns:
             for f in forbidden:
                 if f in c.lower():
                     errors.append(f"Forbidden column detected: {c}")

    return errors

def ensemble_input_resolver_summary(refs: List[EnsemblePrototypeInputReference]) -> Dict[str, Any]:
    return {"ref_count": len(refs)}

def ensemble_input_resolver_to_text(refs: List[EnsemblePrototypeInputReference], limit: int = 300) -> str:
    return str(ensemble_input_resolver_summary(refs))
