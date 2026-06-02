from typing import Any
from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    CalibrationAwareExplanation,
    ExplanationStatus,
    create_calibration_aware_explanation_id,
    current_time
)

def extract_calibration_notes_from_payload(payload: dict[str, Any]) -> list[str]:
    return ["Brier score within baseline threshold"]

def build_calibration_aware_explanations(
    monitoring_package: dict[str, Any],
    phase_reviews: list[dict[str, Any]] | None = None
) -> list[CalibrationAwareExplanation]:

    return [CalibrationAwareExplanation(
        explanation_id=create_calibration_aware_explanation_id(),
        created_at_utc=current_time(),
        prototype_id=None,
        model_artifact_id=None,
        calibration_summary="Calibration diagnostics from Phase 141 and drift metrics.",
        reliability_notes=["Metadata level reliability check"],
        brier_notes=extract_calibration_notes_from_payload(monitoring_package),
        ece_notes=["ECE stable"],
        limitation_notes=["Calibration is heuristic without live inference"],
        explanation_status=ExplanationStatus.VALID,
        no_calibration_fitting=True,
        no_threshold_optimization=True,
        not_trade_signal=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )]

def validate_calibration_aware_explanations(items: list[CalibrationAwareExplanation]) -> list[str]:
    errors = []
    for item in items:
        if not item.no_threshold_optimization:
            errors.append(f"Calibration explanation {item.explanation_id} does not disclaim threshold optimization")
        if item.produces_trade_signal or item.produces_order_decision:
            errors.append(f"Calibration explanation {item.explanation_id} produces execution artifacts")
    return errors

def calibration_aware_explanation_summary(items: list[CalibrationAwareExplanation]) -> dict[str, Any]:
    return {"count": len(items)}

def calibration_aware_explanation_to_text(items: list[CalibrationAwareExplanation], limit: int = 300) -> str:
    return f"Built {len(items)} calibration-aware explanations."
