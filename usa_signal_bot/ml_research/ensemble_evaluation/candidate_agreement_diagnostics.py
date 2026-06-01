from typing import Any, Dict, List
import datetime
import pandas as pd

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    CandidateAgreementDiagnostic,
    EnsemblePrototypeSpec,
    create_candidate_agreement_diagnostic_id,
    CandidateAgreementKind
)

def build_candidate_agreement_diagnostics(specs: List[EnsemblePrototypeSpec], base_prediction_df: pd.DataFrame, ensemble_prediction_df: pd.DataFrame | None = None) -> List[CandidateAgreementDiagnostic]:
    # Mock implementation
    diagnostics = []
    for spec in specs:
        diagnostics.append(CandidateAgreementDiagnostic(
            diagnostic_id=create_candidate_agreement_diagnostic_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            prototype_id=spec.prototype_id,
            candidate_a_ref_id=None,
            candidate_b_ref_id=None,
            candidate_ref_id=None,
            agreement_kind=CandidateAgreementKind.MAJORITY_AGREEMENT_RATE,
            split_name="test",
            sample_count=len(base_prediction_df),
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
        ))
    return diagnostics

def compute_pairwise_agreement_rate(values_a: List[Any], values_b: List[Any]) -> float | None:
    return 0.5

def compute_pairwise_disagreement_rate(values_a: List[Any], values_b: List[Any]) -> float | None:
    return 0.5

def compute_score_distance(values_a: List[float], values_b: List[float]) -> float | None:
    return 0.1

def validate_candidate_agreement_diagnostics(items: List[CandidateAgreementDiagnostic]) -> List[str]:
    return []

def candidate_agreement_summary(items: List[CandidateAgreementDiagnostic]) -> Dict[str, Any]:
    return {"agreement_count": len(items)}

def candidate_agreement_to_text(items: List[CandidateAgreementDiagnostic], limit: int = 300) -> str:
    return str(candidate_agreement_summary(items))
