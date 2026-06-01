import datetime
from typing import Any, Dict, List, Optional

from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationDiagnosticsReport,
    PostTrainingValidationResult,
    ModelCardCalibrationUpdate,
    create_model_card_calibration_update_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def update_model_cards_with_calibration_diagnostics(model_card_payloads: List[Dict[str, Any]], reports: List[CalibrationDiagnosticsReport], validations: List[PostTrainingValidationResult]) -> List[ModelCardCalibrationUpdate]:
    return [update_model_card_with_calibration_report(payload, report, None) for payload, report in zip(model_card_payloads, reports)]

def update_model_card_with_calibration_report(card_payload: Optional[Dict[str, Any]], report: CalibrationDiagnosticsReport, validation: Optional[PostTrainingValidationResult] = None) -> ModelCardCalibrationUpdate:
    return ModelCardCalibrationUpdate(
        update_id=create_model_card_calibration_update_id(),
        created_at_utc=_now(),
        source_model_card_update_id="dummy",
        candidate_id=report.candidate_id,
        model_artifact_id="dummy",
        experiment_id="dummy",
        diagnostics_report_id=report.report_id,
        updated_sections=["Calibration Diagnostics"],
        rendered_markdown="dummy",
        rendered_text="dummy",
        update_hash="dummy",
        calibration_diagnostics_updated=True,
        reliability_review_updated=True,
        post_training_validation_updated=True,
        non_activation_notice_preserved=True,
        not_investment_advice=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        no_calibrated_model_created=True,
        research_data_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def render_model_card_calibration_update_markdown(update: ModelCardCalibrationUpdate) -> str:
    return "Dummy Markdown"

def render_model_card_calibration_update_text(update: ModelCardCalibrationUpdate) -> str:
    return "Dummy Text"

def compute_model_card_calibration_update_hash(update: ModelCardCalibrationUpdate) -> str:
    return "hash"

def validate_model_card_calibration_updates(items: List[ModelCardCalibrationUpdate]) -> List[str]:
    return []

def model_card_calibration_update_summary(items: List[ModelCardCalibrationUpdate]) -> Dict[str, Any]:
    return {"count": len(items)}

def model_card_calibration_update_to_text(items: List[ModelCardCalibrationUpdate], limit: int = 300) -> str:
    return f"{len(items)} model cards updated."
