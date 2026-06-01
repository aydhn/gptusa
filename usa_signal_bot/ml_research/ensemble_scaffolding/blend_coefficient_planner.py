from typing import Any, Dict, List
from .phase142_models import (
    BlendCoefficientPlan,
    CandidateGroupSpec,
    BlendPolicySpec,
    BlendCoefficientStatus,
    BlendPolicyKind,
    create_blend_coefficient_plan_id,
    validate_blend_coefficient_plan,
    _now
)
import hashlib
import json

def compute_blend_plan_hash(plan: BlendCoefficientPlan) -> str:
    s = json.dumps(plan.coefficient_by_candidate_ref_id, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def build_equal_blend_coefficient_plan(group: CandidateGroupSpec, policy: BlendPolicySpec) -> BlendCoefficientPlan:
    n = max(1, group.actual_candidate_count)
    coef = 1.0 / n
    coefs = {c.candidate_ref_id: coef for c in group.candidate_refs}

    return BlendCoefficientPlan(
        plan_id=create_blend_coefficient_plan_id(),
        created_at_utc=_now(),
        policy_id=policy.policy_id,
        candidate_group_id=group.group_id,
        status=BlendCoefficientStatus.PLANNED,
        coefficient_by_candidate_ref_id=coefs,
        coefficient_sum=sum(coefs.values()),
        coefficient_valid=True,
        coefficient_label="equal_weights_metadata",
        not_portfolio_weight=True,
        not_allocation=True,
        not_target_weight=True,
        fitting_performed=False,
        final_ensemble_prediction_created=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_rank_based_blend_coefficient_plan(group: CandidateGroupSpec, policy: BlendPolicySpec) -> BlendCoefficientPlan:
    # Placeholder heuristic
    n = max(1, group.actual_candidate_count)
    coefs = {}
    total = sum(range(1, n+1))
    for i, c in enumerate(group.candidate_refs):
        weight = (n - i) / total
        if policy.coefficient_cap and weight > policy.coefficient_cap:
            weight = policy.coefficient_cap
        coefs[c.candidate_ref_id] = weight

    s = sum(coefs.values())
    if s > 0:
        coefs = {k: v/s for k, v in coefs.items()}

    return BlendCoefficientPlan(
        plan_id=create_blend_coefficient_plan_id(),
        created_at_utc=_now(),
        policy_id=policy.policy_id,
        candidate_group_id=group.group_id,
        status=BlendCoefficientStatus.PLANNED,
        coefficient_by_candidate_ref_id=coefs,
        coefficient_sum=sum(coefs.values()),
        coefficient_valid=True,
        coefficient_label="rank_weights_metadata",
        not_portfolio_weight=True,
        not_allocation=True,
        not_target_weight=True,
        fitting_performed=False,
        final_ensemble_prediction_created=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_calibration_aware_blend_coefficient_plan(group: CandidateGroupSpec, policy: BlendPolicySpec) -> BlendCoefficientPlan:
    # Placeholder heuristic based on warning count inversed
    n = max(1, group.actual_candidate_count)
    coefs = {}
    for c in group.candidate_refs:
        w = 1.0 / (1.0 + c.calibration_warning_count)
        coefs[c.candidate_ref_id] = w

    s = sum(coefs.values())
    if s > 0:
        coefs = {k: v/s for k, v in coefs.items()}

    return BlendCoefficientPlan(
        plan_id=create_blend_coefficient_plan_id(),
        created_at_utc=_now(),
        policy_id=policy.policy_id,
        candidate_group_id=group.group_id,
        status=BlendCoefficientStatus.PLANNED,
        coefficient_by_candidate_ref_id=coefs,
        coefficient_sum=sum(coefs.values()),
        coefficient_valid=True,
        coefficient_label="cal_weights_metadata",
        not_portfolio_weight=True,
        not_allocation=True,
        not_target_weight=True,
        fitting_performed=False,
        final_ensemble_prediction_created=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_blend_coefficient_plans(groups: List[CandidateGroupSpec], policies: List[BlendPolicySpec]) -> List[BlendCoefficientPlan]:
    res = []
    for g in groups:
        for p in policies:
            if p.candidate_group_id == g.group_id:
                if p.policy_kind == BlendPolicyKind.EQUAL_COEFFICIENT:
                    res.append(build_equal_blend_coefficient_plan(g, p))
                elif p.policy_kind == BlendPolicyKind.RANK_BASED_COEFFICIENT:
                    res.append(build_rank_based_blend_coefficient_plan(g, p))
                elif p.policy_kind == BlendPolicyKind.CALIBRATION_AWARE_COEFFICIENT:
                    res.append(build_calibration_aware_blend_coefficient_plan(g, p))
    return res

def validate_blend_coefficient_plans(items: List[BlendCoefficientPlan]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_blend_coefficient_plan(item))
    return errs

def blend_coefficient_plan_summary(items: List[BlendCoefficientPlan]) -> Dict[str, Any]:
    return {"count": len(items)}

def blend_coefficient_plan_to_text(items: List[BlendCoefficientPlan], limit: int = 300) -> str:
    return f"Built {len(items)} blend coefficient plans"
