from typing import Any, Dict, List
from .phase142_models import (
    EnsembleFamilySpec,
    EnsembleFamilyKind,
    EnsembleCandidateKind,
    BlendPolicyKind,
    create_ensemble_family_spec_id,
    validate_ensemble_family_spec,
    _now
)

def build_simple_average_research_family() -> EnsembleFamilySpec:
    return EnsembleFamilySpec(
        family_id=create_ensemble_family_spec_id(),
        created_at_utc=_now(),
        family_name="Simple Average Research Ensemble",
        family_kind=EnsembleFamilyKind.SIMPLE_AVERAGE_RESEARCH_ENSEMBLE,
        description="Averages candidate predictions",
        supported_candidate_kinds=[EnsembleCandidateKind.CALIBRATION_AWARE_CANDIDATE, EnsembleCandidateKind.PROBABILITY_CANDIDATE],
        supported_blend_policies=[BlendPolicyKind.EQUAL_COEFFICIENT],
        fitting_allowed_in_phase142=False,
        final_prediction_allowed_in_phase142=False,
        implementation_deferred_to_phase143=True,
        requires_heavy_dependency=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_coefficient_blend_research_family() -> EnsembleFamilySpec:
    return EnsembleFamilySpec(
        family_id=create_ensemble_family_spec_id(),
        created_at_utc=_now(),
        family_name="Coefficient Blend Research Ensemble",
        family_kind=EnsembleFamilyKind.COEFFICIENT_BLEND_RESEARCH_ENSEMBLE,
        description="Weighted blend using pre-planned coefficients",
        supported_candidate_kinds=[EnsembleCandidateKind.CALIBRATION_AWARE_CANDIDATE],
        supported_blend_policies=[BlendPolicyKind.RANK_BASED_COEFFICIENT, BlendPolicyKind.CALIBRATION_AWARE_COEFFICIENT, BlendPolicyKind.DIVERSITY_AWARE_COEFFICIENT],
        fitting_allowed_in_phase142=False,
        final_prediction_allowed_in_phase142=False,
        implementation_deferred_to_phase143=True,
        requires_heavy_dependency=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_rank_weighted_research_family() -> EnsembleFamilySpec:
    f = build_coefficient_blend_research_family()
    f.family_name = "Rank-Weighted Research Ensemble"
    f.family_kind = EnsembleFamilyKind.RANK_WEIGHTED_RESEARCH_ENSEMBLE
    f.supported_blend_policies = [BlendPolicyKind.RANK_BASED_COEFFICIENT]
    return f

def build_calibration_aware_research_family() -> EnsembleFamilySpec:
    f = build_coefficient_blend_research_family()
    f.family_name = "Calibration-Aware Research Ensemble"
    f.family_kind = EnsembleFamilyKind.CALIBRATION_AWARE_RESEARCH_ENSEMBLE
    f.supported_blend_policies = [BlendPolicyKind.CALIBRATION_AWARE_COEFFICIENT]
    return f

def build_diversity_aware_research_family() -> EnsembleFamilySpec:
    f = build_coefficient_blend_research_family()
    f.family_name = "Diversity-Aware Research Ensemble"
    f.family_kind = EnsembleFamilyKind.DIVERSITY_AWARE_RESEARCH_ENSEMBLE
    f.supported_blend_policies = [BlendPolicyKind.DIVERSITY_AWARE_COEFFICIENT]
    return f

def build_default_ensemble_family_specs() -> List[EnsembleFamilySpec]:
    return [
        build_simple_average_research_family(),
        build_coefficient_blend_research_family(),
        build_rank_weighted_research_family(),
        build_calibration_aware_research_family(),
        build_diversity_aware_research_family()
    ]

def validate_ensemble_family_specs(items: List[EnsembleFamilySpec]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_ensemble_family_spec(item))
    return errs

def ensemble_family_specs_summary(items: List[EnsembleFamilySpec]) -> Dict[str, Any]:
    return {"count": len(items)}

def ensemble_family_specs_to_text(items: List[EnsembleFamilySpec], limit: int = 300) -> str:
    return f"Built {len(items)} ensemble family specs"
