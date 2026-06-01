from typing import Any, Dict, List
import hashlib
import json
from .phase142_models import (
    EnsemblePreparationReport,
    CandidateGroupSpec,
    EnsembleFamilySpec,
    BlendPolicySpec,
    BlendCoefficientPlan,
    PredictionCorrelationDiagnostic,
    CandidateDiversityProfile,
    ComplementarityProfile,
    CalibrationAwareEligibilityProfile,
    EnsembleScaffoldingQuality,
    create_ensemble_preparation_report_id,
    validate_ensemble_preparation_report,
    _now
)

def compute_ensemble_preparation_report_hash(report: EnsemblePreparationReport) -> str:
    # Minimal deterministic hash
    s = f"{report.candidate_group.group_id}_{report.blend_plan.plan_id}_{report.quality.value}"
    return hashlib.sha256(s.encode()).hexdigest()

def build_ensemble_preparation_report_for_group(
    group: CandidateGroupSpec,
    family_spec: EnsembleFamilySpec,
    policy: BlendPolicySpec,
    blend_plan: BlendCoefficientPlan,
    correlations: List[PredictionCorrelationDiagnostic],
    diversity_profiles: List[CandidateDiversityProfile],
    complementarity_profiles: List[ComplementarityProfile],
    eligibility_profiles: List[CalibrationAwareEligibilityProfile]
) -> EnsemblePreparationReport:

    c_ids = [c.candidate_ref_id for c in group.candidate_refs]
    grp_corrs = [c for c in correlations if c.candidate_a_ref_id in c_ids and c.candidate_b_ref_id in c_ids]
    grp_divs = [d for d in diversity_profiles if d.candidate_ref_id in c_ids]
    grp_comps = [c for c in complementarity_profiles if c.candidate_ref_id in c_ids]
    grp_eligs = [e for e in eligibility_profiles if e.candidate_ref_id in c_ids]

    qual = EnsembleScaffoldingQuality.HIGH
    if not blend_plan.coefficient_valid:
        qual = EnsembleScaffoldingQuality.INVALID
    elif any(e.status.value != "ELIGIBLE_FOR_PHASE143_RESEARCH" for e in grp_eligs):
        qual = EnsembleScaffoldingQuality.WARNING

    rep = EnsemblePreparationReport(
        report_id=create_ensemble_preparation_report_id(),
        created_at_utc=_now(),
        candidate_group=group,
        family_spec=family_spec,
        blend_policy=policy,
        blend_plan=blend_plan,
        correlation_diagnostics=grp_corrs,
        diversity_profiles=grp_divs,
        complementarity_profiles=grp_comps,
        eligibility_profiles=grp_eligs,
        report_hash=None,
        report_valid=(qual != EnsembleScaffoldingQuality.INVALID),
        quality=qual,
        fitting_performed=False,
        final_ensemble_prediction_created=False,
        threshold_optimization_performed=False,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    rep.report_hash = compute_ensemble_preparation_report_hash(rep)
    return rep

def build_ensemble_preparation_reports(
    groups: List[CandidateGroupSpec],
    family_specs: List[EnsembleFamilySpec],
    policies: List[BlendPolicySpec],
    blend_plans: List[BlendCoefficientPlan],
    correlations: List[PredictionCorrelationDiagnostic],
    diversity_profiles: List[CandidateDiversityProfile],
    complementarity_profiles: List[ComplementarityProfile],
    eligibility_profiles: List[CalibrationAwareEligibilityProfile]
) -> List[EnsemblePreparationReport]:

    res = []
    fam_map = {f.family_kind: f for f in family_specs}
    pol_map = {p.policy_id: p for p in policies}

    for bp in blend_plans:
        pol = pol_map.get(bp.policy_id)
        if not pol: continue
        fam = fam_map.get(pol.ensemble_family_kind)
        if not fam: continue
        grp = next((g for g in groups if g.group_id == bp.candidate_group_id), None)
        if not grp: continue

        rep = build_ensemble_preparation_report_for_group(
            grp, fam, pol, bp, correlations, diversity_profiles, complementarity_profiles, eligibility_profiles
        )
        res.append(rep)
    return res

def validate_ensemble_preparation_reports(items: List[EnsemblePreparationReport]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_ensemble_preparation_report(item))
    return errs

def ensemble_preparation_report_summary(items: List[EnsemblePreparationReport]) -> Dict[str, Any]:
    return {"count": len(items)}

def ensemble_preparation_report_to_text(items: List[EnsemblePreparationReport], limit: int = 300) -> str:
    return f"Built {len(items)} ensemble preparation reports"
