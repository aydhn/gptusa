from typing import Any, Dict, List, Optional
import hashlib
from .phase142_models import (
    ModelCardEnsembleUpdate,
    EnsemblePreparationReport,
    EnsembleGovernanceResult,
    create_model_card_ensemble_update_id,
    validate_model_card_ensemble_update,
    _now
)

def compute_model_card_ensemble_update_hash(update: ModelCardEnsembleUpdate) -> str:
    return hashlib.sha256((update.rendered_markdown or "").encode()).hexdigest()

def render_model_card_ensemble_update_markdown(update: ModelCardEnsembleUpdate) -> str:
    return f"# Ensemble Scaffold\nUpdate: {update.update_id}\n"

def render_model_card_ensemble_update_text(update: ModelCardEnsembleUpdate) -> str:
    return f"Ensemble Update: {update.update_id}"

def update_model_card_with_ensemble_report(card_payload: Optional[Dict[str, Any]], report: EnsemblePreparationReport, governance: Optional[EnsembleGovernanceResult] = None) -> ModelCardEnsembleUpdate:
    upd = ModelCardEnsembleUpdate(
        update_id=create_model_card_ensemble_update_id(),
        created_at_utc=_now(),
        source_model_card_update_id=card_payload.get('update_id') if card_payload else None,
        candidate_group_id=report.candidate_group.group_id,
        ensemble_report_id=report.report_id,
        updated_sections=["Ensemble Preparation"],
        rendered_markdown=None,
        rendered_text=None,
        update_hash=None,
        ensemble_preparation_updated=True,
        blend_policy_updated=True,
        calibration_aware_governance_updated=True,
        non_activation_notice_preserved=True,
        not_investment_advice=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        no_ensemble_fitting_performed=True,
        no_final_ensemble_prediction_created=True,
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
    upd.rendered_markdown = render_model_card_ensemble_update_markdown(upd)
    upd.rendered_text = render_model_card_ensemble_update_text(upd)
    upd.update_hash = compute_model_card_ensemble_update_hash(upd)
    return upd

def update_model_cards_with_ensemble_scaffolding(model_card_payloads: List[Dict[str, Any]], reports: List[EnsemblePreparationReport], governance: EnsembleGovernanceResult) -> List[ModelCardEnsembleUpdate]:
    res = []
    # simple mock mapping
    for r in reports:
        res.append(update_model_card_with_ensemble_report(None, r, governance))
    return res

def validate_model_card_ensemble_updates(items: List[ModelCardEnsembleUpdate]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_model_card_ensemble_update(item))
    return errs

def model_card_ensemble_update_summary(items: List[ModelCardEnsembleUpdate]) -> Dict[str, Any]:
    return {"count": len(items)}

def model_card_ensemble_update_to_text(items: List[ModelCardEnsembleUpdate], limit: int = 300) -> str:
    return f"Generated {len(items)} model card ensemble updates"
