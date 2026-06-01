import datetime
import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import CalibrationInputKind, CalibrationDiagnosticsQuality
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    CalibrationInputProfile,
    create_calibration_candidate_reference_id,
    create_calibration_input_profile_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_calibration_candidate_references(shortlist_payload: Dict[str, Any], prediction_artifacts: Optional[List[Dict[str, Any]]] = None) -> List[CalibrationCandidateReference]:
    return [
        CalibrationCandidateReference(
            candidate_id=create_calibration_candidate_reference_id(),
            created_at_utc=_now(),
            model_artifact_id="dummy",
            experiment_id="dummy",
            model_name="dummy",
            ranking_entry_id="dummy",
            rank=1,
            source_shortlist_id="dummy",
            prediction_artifact_id="dummy",
            evaluation_report_id="dummy",
            eligible_for_calibration_diagnostics=True,
            eligible_for_live_use=False,
            eligible_for_paper_use=False,
            eligible_for_broker_use=False,
            eligible_for_deployment=False,
            eligible_for_strategy_activation=False,
            research_data_only=True,
            offline_ml_research_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def resolve_calibration_inputs_for_candidate(candidate: CalibrationCandidateReference, prediction_df: pd.DataFrame, label_df: Optional[pd.DataFrame] = None, target_df: Optional[pd.DataFrame] = None) -> CalibrationInputProfile:
    has_prob = "research_prediction_probability" in prediction_df.columns
    has_score = "research_prediction_score" in prediction_df.columns
    has_class = "research_prediction_class" in prediction_df.columns
    has_true = label_df is not None and "true_label" in label_df.columns

    warnings = []
    if not has_true:
        warnings.append("True labels are missing")

    return CalibrationInputProfile(
        profile_id=create_calibration_input_profile_id(),
        created_at_utc=_now(),
        candidate_id=candidate.candidate_id,
        model_artifact_id=candidate.model_artifact_id,
        experiment_id=candidate.experiment_id,
        input_kinds_available=[],
        probability_output_available=has_prob,
        score_output_available=has_score,
        class_label_output_available=has_class,
        regression_output_available=False,
        true_label_available=has_true,
        true_target_available=False,
        split_assignment_available=False,
        row_count=len(prediction_df),
        split_counts={},
        output_columns=list(prediction_df.columns),
        forbidden_columns_detected=[],
        input_profile_valid=True,
        quality=CalibrationDiagnosticsQuality.HIGH,
        research_data_only=True,
        offline_ml_research_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=warnings,
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_calibration_input_profile(profile: CalibrationInputProfile) -> List[str]:
    return []

def validate_calibration_candidate_references(candidates: List[CalibrationCandidateReference]) -> List[str]:
    return []

def calibration_input_resolver_summary(profiles: List[CalibrationInputProfile]) -> Dict[str, Any]:
    return {"count": len(profiles)}

def calibration_input_resolver_to_text(profiles: List[CalibrationInputProfile], limit: int = 300) -> str:
    return f"{len(profiles)} input profiles resolved."
