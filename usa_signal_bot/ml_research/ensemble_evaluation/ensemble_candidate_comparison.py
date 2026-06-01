from typing import Any, Dict, List
import datetime

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsembleCandidateComparisonResult,
    OfflineEnsembleEvaluationMetricResult,
    create_ensemble_candidate_comparison_id,
    EnsembleCandidateComparisonKind
)

def build_ensemble_candidate_comparisons(ensemble_metrics: List[OfflineEnsembleEvaluationMetricResult], candidate_metric_rows: List[Dict[str, Any]] | None = None) -> List[EnsembleCandidateComparisonResult]:
    # Mock
    return []

def compare_ensemble_to_candidate_metric(prototype_id: str, candidate_ref_id: str | None, metric_name: str, ensemble_value: float | None, candidate_value: float | None, split_name: str | None = None) -> EnsembleCandidateComparisonResult:
    return EnsembleCandidateComparisonResult(
        comparison_id=create_ensemble_candidate_comparison_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        prototype_id=prototype_id,
        candidate_ref_id=candidate_ref_id,
        comparison_kind=EnsembleCandidateComparisonKind.ENSEMBLE_VS_BEST_CANDIDATE,
        split_name=split_name,
        ensemble_metric_value=ensemble_value,
        candidate_metric_value=candidate_value,
        delta_value=ensemble_value - candidate_value if ensemble_value is not None and candidate_value is not None else None,
        comparison_notes=[],
        comparison_valid=True,
        non_trading_comparison=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_ensemble_candidate_comparisons(items: List[EnsembleCandidateComparisonResult]) -> List[str]:
    return []

def ensemble_candidate_comparison_summary(items: List[EnsembleCandidateComparisonResult]) -> Dict[str, Any]:
    return {"comparison_count": len(items)}

def ensemble_candidate_comparison_to_text(items: List[EnsembleCandidateComparisonResult], limit: int = 300) -> str:
    return str(ensemble_candidate_comparison_summary(items))
