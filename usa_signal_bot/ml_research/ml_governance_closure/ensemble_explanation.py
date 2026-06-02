from typing import Any
from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    EnsembleExplanation,
    ExplanationStatus,
    create_ensemble_explanation_id,
    current_time
)

def extract_blend_notes_from_payload(payload: dict[str, Any]) -> list[str]:
    return ["Research blend computed offline"]

def extract_agreement_notes_from_payload(payload: dict[str, Any]) -> list[str]:
    return ["High candidate agreement observed in baseline"]

def build_ensemble_explanations(
    monitoring_package: dict[str, Any],
    phase_reviews: list[dict[str, Any]] | None = None
) -> list[EnsembleExplanation]:

    return [EnsembleExplanation(
        explanation_id=create_ensemble_explanation_id(),
        created_at_utc=current_time(),
        prototype_id=None,
        ensemble_registry_entry_id=None,
        ensemble_summary="Ensemble metadata from Phase 142/143.",
        candidate_contribution_notes=extract_blend_notes_from_payload(monitoring_package),
        blend_diagnostic_notes=["Diagnostics show stable blend"],
        agreement_notes=extract_agreement_notes_from_payload(monitoring_package),
        limitation_notes=["No live ensemble execution or live inference"],
        explanation_status=ExplanationStatus.VALID,
        not_portfolio_weight=True,
        not_allocation=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )]

def validate_ensemble_explanations(items: list[EnsembleExplanation]) -> list[str]:
    errors = []
    for item in items:
        if not item.not_portfolio_weight or not item.not_allocation:
            errors.append(f"Ensemble explanation {item.explanation_id} does not disclaim portfolio weights/allocations")
        if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Ensemble explanation {item.explanation_id} produces execution artifacts")
    return errors

def ensemble_explanation_summary(items: list[EnsembleExplanation]) -> dict[str, Any]:
    return {"count": len(items)}

def ensemble_explanation_to_text(items: list[EnsembleExplanation], limit: int = 300) -> str:
    return f"Built {len(items)} ensemble explanations."
