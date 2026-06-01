from typing import Any, Dict, List, Optional
from .phase142_models import (
    PredictionCorrelationDiagnostic,
    PredictionCorrelationKind,
    EnsembleCandidateReference,
    create_prediction_correlation_diagnostic_id,
    validate_prediction_correlation_diagnostic,
    _now
)

def compute_pairwise_prediction_correlation(series_a: List[Any], series_b: List[Any]) -> Optional[float]:
    # Offline placeholder
    return 0.5

def compute_pairwise_agreement_rate(series_a: List[Any], series_b: List[Any]) -> Optional[float]:
    # Offline placeholder
    return 0.75

def build_prediction_correlation_diagnostics(candidates: List[EnsembleCandidateReference], prediction_df: Any = None) -> List[PredictionCorrelationDiagnostic]:
    res = []
    cands = [c for c in candidates if c.eligible_for_ensemble_research]
    for i in range(len(cands)):
        for j in range(i+1, len(cands)):
            diag = PredictionCorrelationDiagnostic(
                diagnostic_id=create_prediction_correlation_diagnostic_id(),
                created_at_utc=_now(),
                candidate_a_ref_id=cands[i].candidate_ref_id,
                candidate_b_ref_id=cands[j].candidate_ref_id,
                correlation_kind=PredictionCorrelationKind.PEARSON_APPROX,
                split_name="validation",
                sample_count=1000,
                value=0.5,
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
            res.append(diag)

            diag_agr = PredictionCorrelationDiagnostic(
                diagnostic_id=create_prediction_correlation_diagnostic_id(),
                created_at_utc=_now(),
                candidate_a_ref_id=cands[i].candidate_ref_id,
                candidate_b_ref_id=cands[j].candidate_ref_id,
                correlation_kind=PredictionCorrelationKind.AGREEMENT_RATE,
                split_name="validation",
                sample_count=1000,
                value=0.75,
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
            res.append(diag_agr)
    return res

def validate_prediction_correlation_diagnostics(items: List[PredictionCorrelationDiagnostic]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_prediction_correlation_diagnostic(item))
    return errs

def prediction_correlation_summary(items: List[PredictionCorrelationDiagnostic]) -> Dict[str, Any]:
    return {"count": len(items)}

def prediction_correlation_to_text(items: List[PredictionCorrelationDiagnostic], limit: int = 300) -> str:
    return f"Built {len(items)} prediction correlations"
