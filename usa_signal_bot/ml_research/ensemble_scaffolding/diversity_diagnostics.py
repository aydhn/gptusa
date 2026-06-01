from typing import Any, Dict, List
from .phase142_models import (
    CandidateDiversityProfile,
    DiversityMetricKind,
    EnsembleCandidateReference,
    PredictionCorrelationDiagnostic,
    create_candidate_diversity_profile_id,
    validate_candidate_diversity_profile,
    _now
)

def compute_correlation_diversity_score(candidate_ref_id: str, correlations: List[PredictionCorrelationDiagnostic]) -> Optional[float]:
    # Placeholder heuristic
    rels = [c for c in correlations if c.candidate_a_ref_id == candidate_ref_id or c.candidate_b_ref_id == candidate_ref_id]
    if not rels: return 0.0
    return 1.0 - sum(c.value for c in rels if c.value) / len(rels)

def compute_calibration_diversity_bonus(candidate: EnsembleCandidateReference) -> Optional[float]:
    return 0.1 if candidate.calibration_warning_count == 0 else 0.0

def build_candidate_diversity_profiles(candidates: List[EnsembleCandidateReference], correlations: Optional[List[PredictionCorrelationDiagnostic]] = None) -> List[CandidateDiversityProfile]:
    res = []
    corrs = correlations or []
    for c in candidates:
        if not c.eligible_for_ensemble_research: continue

        prof = CandidateDiversityProfile(
            profile_id=create_candidate_diversity_profile_id(),
            created_at_utc=_now(),
            candidate_ref_id=c.candidate_ref_id,
            group_id=None,
            metric_kind=DiversityMetricKind.CORRELATION_DIVERSITY,
            diversity_score=compute_correlation_diversity_score(c.candidate_ref_id, corrs),
            correlation_penalty=0.1,
            stability_bonus=0.05,
            calibration_bonus=compute_calibration_diversity_bonus(c),
            diagnostic_notes=["Offline heuristic evaluated"],
            profile_valid=True,
            research_data_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        res.append(prof)
    return res

def validate_candidate_diversity_profiles(items: List[CandidateDiversityProfile]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_candidate_diversity_profile(item))
    return errs

def diversity_diagnostics_summary(items: List[CandidateDiversityProfile]) -> Dict[str, Any]:
    return {"count": len(items)}

def diversity_diagnostics_to_text(items: List[CandidateDiversityProfile], limit: int = 300) -> str:
    return f"Built {len(items)} diversity profiles"
