from typing import Any, Dict
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import *

def model_comparison_ingestion_result_to_text(item: ModelComparisonIngestionResult) -> str: return str(item)
def calibration_candidate_reference_to_text(item: CalibrationCandidateReference) -> str: return str(item)
def calibration_input_profile_to_text(item: CalibrationInputProfile, limit: int = 300) -> str: return str(item)[:limit]
def reliability_bin_result_to_text(item: ReliabilityBinResult) -> str: return str(item)
def calibration_metric_result_to_text(item: CalibrationMetricResult) -> str: return str(item)
def brier_decomposition_result_to_text(item: BrierDecompositionResult, limit: int = 300) -> str: return str(item)[:limit]
def score_distribution_diagnostic_to_text(item: ScoreDistributionDiagnostic, limit: int = 300) -> str: return str(item)[:limit]
def class_balance_diagnostic_to_text(item: ClassBalanceDiagnostic, limit: int = 300) -> str: return str(item)[:limit]
def calibration_diagnostics_report_to_text(item: CalibrationDiagnosticsReport, limit: int = 300) -> str: return str(item)[:limit]
def post_training_validation_to_text(item: PostTrainingValidationResult, limit: int = 300) -> str: return str(item)[:limit]
def calibration_governance_to_text(item: CalibrationGovernanceResult, limit: int = 300) -> str: return str(item)[:limit]
def model_card_calibration_update_to_text(item: ModelCardCalibrationUpdate, limit: int = 300) -> str: return str(item)[:limit]
def calibration_readiness_gate_to_text(item: CalibrationReadinessGate, limit: int = 300) -> str: return str(item)[:limit]
def calibration_diagnostics_context_to_text(item: CalibrationDiagnosticsContext, limit: int = 300) -> str: return str(item)[:limit]
def calibration_diagnostics_full_review_to_text(item: CalibrationDiagnosticsFullReview, limit: int = 300) -> str: return str(item)[:limit]
def calibration_diagnostics_store_summary_to_text(summary: Dict[str, Any]) -> str: return str(summary)
def calibration_diagnostics_limitations_text() -> str: return "Phase 141 is local offline only. No execution."
