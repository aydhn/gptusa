from typing import Any, Dict, List
from .phase142_models import (
    CandidateGroupSpec,
    EnsembleCandidateReference,
    CandidateGroupKind,
    create_candidate_group_spec_id,
    validate_candidate_group_spec,
    _now
)

def build_top_ranked_candidate_group(candidates: List[EnsembleCandidateReference], max_group_size: int = 3) -> CandidateGroupSpec:
    cands = sorted([c for c in candidates if c.eligible_for_ensemble_research], key=lambda x: x.rank or 999)[:max_group_size]
    return CandidateGroupSpec(
        group_id=create_candidate_group_spec_id(),
        created_at_utc=_now(),
        group_name="Top Ranked",
        group_kind=CandidateGroupKind.TOP_RANKED_GROUP,
        candidate_refs=cands,
        min_candidate_count=2,
        max_candidate_count=max_group_size,
        actual_candidate_count=len(cands),
        group_valid=len(cands) >= 2,
        calibration_aware=False,
        diversity_aware=False,
        regime_aware=False,
        research_only=True,
        eligible_for_phase143_offline_ensemble_eval=len(cands) >= 2,
        eligible_for_live_use=False,
        eligible_for_paper_use=False,
        eligible_for_broker_use=False,
        eligible_for_deployment=False,
        eligible_for_strategy_activation=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_calibration_aware_candidate_group(candidates: List[EnsembleCandidateReference], max_group_size: int = 3) -> CandidateGroupSpec:
    cands = sorted([c for c in candidates if c.eligible_for_ensemble_research], key=lambda x: x.calibration_warning_count)[:max_group_size]
    return CandidateGroupSpec(
        group_id=create_candidate_group_spec_id(),
        created_at_utc=_now(),
        group_name="Calibration Aware",
        group_kind=CandidateGroupKind.CALIBRATION_AWARE_GROUP,
        candidate_refs=cands,
        min_candidate_count=2,
        max_candidate_count=max_group_size,
        actual_candidate_count=len(cands),
        group_valid=len(cands) >= 2,
        calibration_aware=True,
        diversity_aware=False,
        regime_aware=False,
        research_only=True,
        eligible_for_phase143_offline_ensemble_eval=len(cands) >= 2,
        eligible_for_live_use=False,
        eligible_for_paper_use=False,
        eligible_for_broker_use=False,
        eligible_for_deployment=False,
        eligible_for_strategy_activation=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_diversity_candidate_group_placeholder(candidates: List[EnsembleCandidateReference], max_group_size: int = 3) -> CandidateGroupSpec:
    cands = [c for c in candidates if c.eligible_for_ensemble_research][:max_group_size]
    return CandidateGroupSpec(
        group_id=create_candidate_group_spec_id(),
        created_at_utc=_now(),
        group_name="Diversity Aware",
        group_kind=CandidateGroupKind.DIVERSITY_AWARE_GROUP,
        candidate_refs=cands,
        min_candidate_count=2,
        max_candidate_count=max_group_size,
        actual_candidate_count=len(cands),
        group_valid=len(cands) >= 2,
        calibration_aware=False,
        diversity_aware=True,
        regime_aware=False,
        research_only=True,
        eligible_for_phase143_offline_ensemble_eval=len(cands) >= 2,
        eligible_for_live_use=False,
        eligible_for_paper_use=False,
        eligible_for_broker_use=False,
        eligible_for_deployment=False,
        eligible_for_strategy_activation=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_candidate_groups(candidates: List[EnsembleCandidateReference], max_group_size: int = 3) -> List[CandidateGroupSpec]:
    return [
        build_top_ranked_candidate_group(candidates, max_group_size),
        build_calibration_aware_candidate_group(candidates, max_group_size),
        build_diversity_candidate_group_placeholder(candidates, max_group_size)
    ]

def validate_candidate_groups(items: List[CandidateGroupSpec]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_candidate_group_spec(item))
    return errs

def candidate_grouping_summary(items: List[CandidateGroupSpec]) -> Dict[str, Any]:
    return {"count": len(items)}

def candidate_grouping_to_text(items: List[CandidateGroupSpec], limit: int = 300) -> str:
    return f"Built {len(items)} candidate groups"
