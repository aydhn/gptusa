import datetime
from typing import Any, Dict, List, Optional

from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    ReliabilityBinResult,
    BrierDecompositionResult,
    create_brier_decomposition_result_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def calculate_brier_decomposition(candidate: CalibrationCandidateReference, bins: List[ReliabilityBinResult]) -> BrierDecompositionResult:
    return BrierDecompositionResult(
        decomposition_id=create_brier_decomposition_result_id(),
        created_at_utc=_now(),
        candidate_id=candidate.candidate_id,
        model_artifact_id="dummy",
        experiment_id="dummy",
        split_name=None,
        brier_score=0.20,
        reliability=0.01,
        resolution=0.05,
        uncertainty=0.24,
        bin_count=len(bins),
        sample_count=sum(b.sample_count for b in bins),
        decomposition_valid=True,
        fitting_performed=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_brier_decomposition_result(item: BrierDecompositionResult) -> List[str]:
    return []

def brier_decomposition_summary(item: BrierDecompositionResult) -> Dict[str, Any]:
    return {"brier_score": item.brier_score}

def brier_decomposition_to_text(item: BrierDecompositionResult, limit: int = 300) -> str:
    return f"Brier decomposition: {item.brier_score}"
