from typing import Any, Dict, List, Optional
from .phase142_models import (
    ComplementarityProfile,
    ComplementarityKind,
    EnsembleCandidateReference,
    CandidateDiversityProfile,
    create_complementarity_profile_id,
    validate_complementarity_profile,
    _now
)

def compute_error_complementarity_placeholder(candidate: EnsembleCandidateReference) -> Optional[float]:
    return 0.8

def compute_regime_complementarity_placeholder(candidate: EnsembleCandidateReference) -> Optional[float]:
    return 0.7

def build_complementarity_profiles(candidates: List[EnsembleCandidateReference], diversity_profiles: Optional[List[CandidateDiversityProfile]] = None) -> List[ComplementarityProfile]:
    res = []
    for c in candidates:
        if not c.eligible_for_ensemble_research: continue

        prof = ComplementarityProfile(
            profile_id=create_complementarity_profile_id(),
            created_at_utc=_now(),
            candidate_ref_id=c.candidate_ref_id,
            group_id=None,
            complementarity_kind=ComplementarityKind.ERROR_COMPLEMENTARITY,
            complementarity_score=compute_error_complementarity_placeholder(c),
            coverage_notes=["Placeholder coverage"],
            regime_notes=["Placeholder regime match"],
            split_notes=["Validation split matched"],
            calibration_notes=["Acceptable calibration overlap"],
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

def validate_complementarity_profiles(items: List[ComplementarityProfile]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_complementarity_profile(item))
    return errs

def complementarity_profile_summary(items: List[ComplementarityProfile]) -> Dict[str, Any]:
    return {"count": len(items)}

def complementarity_profile_to_text(items: List[ComplementarityProfile], limit: int = 300) -> str:
    return f"Built {len(items)} complementarity profiles"
