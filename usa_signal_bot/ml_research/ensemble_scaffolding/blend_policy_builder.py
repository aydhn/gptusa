from typing import Any, Dict, List
from .phase142_models import (
    BlendPolicySpec,
    CandidateGroupSpec,
    EnsembleFamilySpec,
    BlendPolicyKind,
    EnsembleFamilyKind,
    create_blend_policy_spec_id,
    validate_blend_policy_spec,
    _now
)

def build_equal_coefficient_policy(group: CandidateGroupSpec, family_kind: EnsembleFamilyKind = EnsembleFamilyKind.SIMPLE_AVERAGE_RESEARCH_ENSEMBLE) -> BlendPolicySpec:
    return BlendPolicySpec(
        policy_id=create_blend_policy_spec_id(),
        created_at_utc=_now(),
        policy_name="Equal Coefficient Policy",
        policy_kind=BlendPolicyKind.EQUAL_COEFFICIENT,
        candidate_group_id=group.group_id,
        ensemble_family_kind=family_kind,
        coefficient_sum_required=1.0,
        coefficient_non_negative_required=True,
        coefficient_cap=None,
        uses_calibration_metrics=False,
        uses_diversity_metrics=False,
        uses_ranking_metrics=False,
        fitting_allowed_in_phase142=False,
        final_prediction_allowed_in_phase142=False,
        threshold_optimization_allowed=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_rank_based_coefficient_policy(group: CandidateGroupSpec) -> BlendPolicySpec:
    return BlendPolicySpec(
        policy_id=create_blend_policy_spec_id(),
        created_at_utc=_now(),
        policy_name="Rank-Based Coefficient Policy",
        policy_kind=BlendPolicyKind.RANK_BASED_COEFFICIENT,
        candidate_group_id=group.group_id,
        ensemble_family_kind=EnsembleFamilyKind.RANK_WEIGHTED_RESEARCH_ENSEMBLE,
        coefficient_sum_required=1.0,
        coefficient_non_negative_required=True,
        coefficient_cap=0.8,
        uses_calibration_metrics=False,
        uses_diversity_metrics=False,
        uses_ranking_metrics=True,
        fitting_allowed_in_phase142=False,
        final_prediction_allowed_in_phase142=False,
        threshold_optimization_allowed=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_calibration_aware_coefficient_policy(group: CandidateGroupSpec) -> BlendPolicySpec:
    return BlendPolicySpec(
        policy_id=create_blend_policy_spec_id(),
        created_at_utc=_now(),
        policy_name="Calibration-Aware Coefficient Policy",
        policy_kind=BlendPolicyKind.CALIBRATION_AWARE_COEFFICIENT,
        candidate_group_id=group.group_id,
        ensemble_family_kind=EnsembleFamilyKind.CALIBRATION_AWARE_RESEARCH_ENSEMBLE,
        coefficient_sum_required=1.0,
        coefficient_non_negative_required=True,
        coefficient_cap=0.8,
        uses_calibration_metrics=True,
        uses_diversity_metrics=False,
        uses_ranking_metrics=False,
        fitting_allowed_in_phase142=False,
        final_prediction_allowed_in_phase142=False,
        threshold_optimization_allowed=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_default_blend_policies(groups: List[CandidateGroupSpec], family_specs: List[EnsembleFamilySpec]) -> List[BlendPolicySpec]:
    res = []
    for g in groups:
        res.append(build_equal_coefficient_policy(g))
        res.append(build_rank_based_coefficient_policy(g))
        res.append(build_calibration_aware_coefficient_policy(g))
    return res

def validate_blend_policies(items: List[BlendPolicySpec]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_blend_policy_spec(item))
    return errs

def blend_policy_summary(items: List[BlendPolicySpec]) -> Dict[str, Any]:
    return {"count": len(items)}

def blend_policy_to_text(items: List[BlendPolicySpec], limit: int = 300) -> str:
    return f"Built {len(items)} blend policies"
