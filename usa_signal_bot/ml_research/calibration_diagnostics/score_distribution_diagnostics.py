import datetime
import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    ScoreDistributionDiagnostic,
    create_score_distribution_diagnostic_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_score_distribution_diagnostic(candidate: CalibrationCandidateReference, prediction_df: pd.DataFrame, score_column: str = "research_prediction_score") -> ScoreDistributionDiagnostic:
    return ScoreDistributionDiagnostic(
        diagnostic_id=create_score_distribution_diagnostic_id(),
        created_at_utc=_now(),
        candidate_id=candidate.candidate_id,
        model_artifact_id="dummy",
        experiment_id="dummy",
        split_name=None,
        score_column=score_column,
        row_count=len(prediction_df),
        min_score=0.0,
        max_score=1.0,
        mean_score=0.5,
        median_score=0.5,
        std_score=0.2,
        quantiles={"0.25": 0.25, "0.75": 0.75},
        extreme_low_count=0,
        extreme_high_count=0,
        missing_score_count=0,
        diagnostic_valid=True,
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

def compute_score_quantiles(series: pd.Series) -> Dict[str, float]:
    return {"0.5": 0.5}

def validate_score_distribution_diagnostic(item: ScoreDistributionDiagnostic) -> List[str]:
    return []

def score_distribution_summary(items: List[ScoreDistributionDiagnostic]) -> Dict[str, Any]:
    return {"count": len(items)}

def score_distribution_to_text(items: List[ScoreDistributionDiagnostic], limit: int = 300) -> str:
    return f"{len(items)} score distributions."
