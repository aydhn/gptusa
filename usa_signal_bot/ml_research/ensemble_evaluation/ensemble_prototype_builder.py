from typing import Any, Dict, List
import datetime

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeSpec,
    create_ensemble_prototype_spec_id,
    EnsemblePrototypeKind,
    OfflineEnsemblePredictionKind,
    EnsemblePrototypeRiskFlag
)

def build_ensemble_prototype_specs(groups: List[Dict[str, Any]], blend_plans: List[Dict[str, Any]]) -> List[EnsemblePrototypeSpec]:
    specs = []
    group_map = {g.get("candidate_group_id"): g for g in groups}

    for plan in blend_plans:
        g = group_map.get(plan.get("candidate_group_id"))
        if g:
            specs.append(build_ensemble_prototype_spec_for_group(g, plan))

    return specs

def build_ensemble_prototype_spec_for_group(group_payload: Dict[str, Any], blend_plan_payload: Dict[str, Any]) -> EnsemblePrototypeSpec:

    coeffs = blend_plan_payload.get("coefficient_by_candidate_ref_id", {})
    sum_coeffs = sum(coeffs.values()) if coeffs else 0.0

    return EnsemblePrototypeSpec(
        prototype_id=create_ensemble_prototype_spec_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        prototype_name=blend_plan_payload.get("blend_plan_name", "Unknown Prototype"),
        prototype_kind=infer_ensemble_prototype_kind(blend_plan_payload),
        candidate_group_id=group_payload.get("candidate_group_id", "unknown"),
        blend_plan_id=blend_plan_payload.get("blend_plan_id", "unknown"),
        candidate_ref_ids=list(coeffs.keys()),
        coefficient_by_candidate_ref_id=coeffs,
        coefficient_sum=sum_coeffs,
        coefficient_valid=abs(sum_coeffs - 1.0) < 0.01 if coeffs else False,
        output_kind=OfflineEnsemblePredictionKind.RESEARCH_ENSEMBLE_SCORE,
        offline_evaluation_only=True,
        live_inference_allowed=False,
        online_inference_allowed=False,
        threshold_optimization_allowed=False,
        deployment_allowed=False,
        broker_allowed=False,
        paper_mutation_allowed=False,
        strategy_activation_allowed=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def infer_ensemble_prototype_kind(blend_plan_payload: Dict[str, Any]) -> EnsemblePrototypeKind:
    if "blend" in blend_plan_payload.get("blend_plan_name", "").lower():
        return EnsemblePrototypeKind.COEFFICIENT_BLEND_PROTOTYPE
    return EnsemblePrototypeKind.SIMPLE_AVERAGE_PROTOTYPE

def validate_ensemble_prototype_specs(items: List[EnsemblePrototypeSpec]) -> List[str]:
    errors = []
    for spec in items:
        if not spec.offline_evaluation_only:
            errors.append("Spec is not offline evaluation only")
        if spec.produces_trade_signal or spec.produces_portfolio_weights:
            errors.append("Spec produces trading outputs")
    return errors

def ensemble_prototype_spec_summary(items: List[EnsemblePrototypeSpec]) -> Dict[str, Any]:
    return {"spec_count": len(items)}

def ensemble_prototype_spec_to_text(items: List[EnsemblePrototypeSpec], limit: int = 300) -> str:
    return str(ensemble_prototype_spec_summary(items))
