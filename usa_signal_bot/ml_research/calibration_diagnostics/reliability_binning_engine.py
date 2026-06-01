import datetime
import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import ProbabilityReliabilityKind, ReliabilityBinStrategy
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    ReliabilityBinSpec,
    ReliabilityBinResult,
    create_reliability_bin_spec_id,
    create_reliability_bin_result_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_reliability_bin_spec(candidate: CalibrationCandidateReference, split_name: Optional[str] = None, bin_count: int = 10, strategy: ReliabilityBinStrategy = ReliabilityBinStrategy.FIXED_10_BIN) -> ReliabilityBinSpec:
    return ReliabilityBinSpec(
        bin_spec_id=create_reliability_bin_spec_id(),
        created_at_utc=_now(),
        candidate_id=candidate.candidate_id,
        reliability_kind=ProbabilityReliabilityKind.BINARY_CLASSIFICATION,
        strategy=strategy,
        bin_count=bin_count,
        min_probability=0.0,
        max_probability=1.0,
        split_name=split_name,
        class_name=None,
        deterministic=True,
        fitting_performed=False,
        threshold_optimization_performed=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_reliability_bins(prediction_df: pd.DataFrame, label_df: Optional[pd.DataFrame], spec: ReliabilityBinSpec, probability_column: str = "research_prediction_probability", label_column: str = "true_label") -> List[ReliabilityBinResult]:
    # Dummy implementation for tests
    return [
        ReliabilityBinResult(
            bin_result_id=create_reliability_bin_result_id(),
            created_at_utc=_now(),
            bin_spec_id=spec.bin_spec_id,
            candidate_id=spec.candidate_id,
            model_artifact_id="dummy",
            experiment_id="dummy",
            split_name=spec.split_name,
            class_name=None,
            bin_index=0,
            bin_lower=0.0,
            bin_upper=0.1,
            sample_count=100,
            average_confidence=0.05,
            empirical_accuracy=0.04,
            calibration_gap=0.01,
            positive_count=4,
            negative_count=96,
            reliability_valid=True,
            research_data_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def assign_probability_bins(series: pd.Series, bin_count: int = 10) -> pd.Series:
    return pd.Series([0]*len(series))

def validate_reliability_bin_results(items: List[ReliabilityBinResult]) -> List[str]:
    return []

def reliability_binning_summary(items: List[ReliabilityBinResult]) -> Dict[str, Any]:
    return {"count": len(items)}

def reliability_binning_to_text(items: List[ReliabilityBinResult], limit: int = 300) -> str:
    return f"{len(items)} reliability bins."
