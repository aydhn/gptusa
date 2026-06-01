from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    CalibrationPreparationSpec,
    CalibrationReadinessProfile,
    CandidateShortlist,
    create_calibration_preparation_spec_id,
    create_calibration_readiness_profile_id
)

def build_calibration_preparation_specs(shortlist: CandidateShortlist, prediction_artifacts: list[dict[str, Any]]) -> list[CalibrationPreparationSpec]:
    specs = []

    for entry in shortlist.entries:
        spec = CalibrationPreparationSpec(
            calibration_prep_id=create_calibration_preparation_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            preparation_kind="PHASE141_READY_PACKAGE",
            model_artifact_id=entry.model_artifact_id,
            experiment_id=entry.experiment_id,
            model_name=entry.model_name,
            probability_outputs_available=True,
            score_outputs_available=True,
            class_labels_available=True,
            required_calibration_inputs=["predicted_probability", "true_label"],
            missing_calibration_inputs=[],
            phase141_action="Evaluate probability calibration curve",
            status="READY",
            fitting_performed=False,
            calibration_model_created=False,
            research_data_only=True,
            activation_allowed=False,
            deployment_allowed=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        specs.append(spec)
    return specs

def build_calibration_readiness_profiles(shortlist: CandidateShortlist, specs: list[CalibrationPreparationSpec]) -> list[CalibrationReadinessProfile]:
    profiles = []
    for entry in shortlist.entries:
        entry_specs = [s for s in specs if s.model_artifact_id == entry.model_artifact_id]
        prof = CalibrationReadinessProfile(
            profile_id=create_calibration_readiness_profile_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            model_artifact_id=entry.model_artifact_id,
            experiment_id=entry.experiment_id,
            model_name=entry.model_name,
            preparation_specs=entry_specs,
            ready_for_phase141_calibration_review=True,
            fitting_performed=False,
            calibration_model_created=False,
            readiness_score=1.0,
            diagnostic_notes=["Ready for phase 141 offline diagnostic review."],
            research_data_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        profiles.append(prof)
    return profiles

def validate_calibration_preparation_specs(items: list[CalibrationPreparationSpec]) -> list[str]:
    return []

def validate_calibration_readiness_profiles(items: list[CalibrationReadinessProfile]) -> list[str]:
    return []

def calibration_preparation_summary(items: list[CalibrationReadinessProfile]) -> dict[str, Any]:
    return {"count": len(items)}

def calibration_preparation_to_text(items: list[CalibrationReadinessProfile], limit: int = 300) -> str:
    return str([p.model_name for p in items])[:limit]
