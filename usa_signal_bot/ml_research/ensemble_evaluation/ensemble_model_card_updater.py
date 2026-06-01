from typing import Any, Dict, List
import datetime
import hashlib

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsembleModelCardUpdate,
    create_ensemble_model_card_update_id,
    OfflineEnsembleEvaluationReport,
    NonActivationEnsembleRegistry
)

def update_model_cards_with_ensemble_evaluation(model_card_payloads: List[Dict[str, Any]], reports: List[OfflineEnsembleEvaluationReport], registry: NonActivationEnsembleRegistry) -> List[EnsembleModelCardUpdate]:
    # Mock
    return []

def update_model_card_for_ensemble_prototype(card_payload: Dict[str, Any] | None, report: OfflineEnsembleEvaluationReport, registry_entry: Dict[str, Any] | None = None) -> EnsembleModelCardUpdate:
    update = EnsembleModelCardUpdate(
        update_id=create_ensemble_model_card_update_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        source_model_card_update_id=None,
        prototype_id=report.prototype_id,
        evaluation_report_id=report.report_id,
        registry_entry_id=registry_entry.get("entry_id") if registry_entry else None,
        updated_sections=["metrics"],
        rendered_markdown="# Mock",
        rendered_text="Mock",
        update_hash=None,
        prototype_evaluation_updated=True,
        blend_diagnostics_updated=True,
        non_activation_registry_updated=True,
        non_activation_notice_preserved=True,
        not_investment_advice=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        no_live_inference=True,
        no_strategy_activation=True,
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
    update.update_hash = compute_ensemble_model_card_update_hash(update)
    return update

def render_ensemble_model_card_update_markdown(update: EnsembleModelCardUpdate) -> str:
    return update.rendered_markdown or ""

def render_ensemble_model_card_update_text(update: EnsembleModelCardUpdate) -> str:
    return update.rendered_text or ""

def compute_ensemble_model_card_update_hash(update: EnsembleModelCardUpdate) -> str:
    s = f"{update.update_id}_{update.prototype_id}"
    return hashlib.sha256(s.encode()).hexdigest()

def validate_ensemble_model_card_updates(items: List[EnsembleModelCardUpdate]) -> List[str]:
    return []

def ensemble_model_card_update_summary(items: List[EnsembleModelCardUpdate]) -> Dict[str, Any]:
    return {"update_count": len(items)}

def ensemble_model_card_update_to_text(items: List[EnsembleModelCardUpdate], limit: int = 300) -> str:
    return str(ensemble_model_card_update_summary(items))
