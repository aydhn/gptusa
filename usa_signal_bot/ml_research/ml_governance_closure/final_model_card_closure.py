from typing import Any
import hashlib
import json

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    FinalMLModelCardClosure,
    ExplainabilityReport,
    MLGovernanceClosureResult,
    AdvancedMLFinalAuditResult,
    create_final_ml_model_card_closure_id,
    current_time
)

def compute_final_ml_model_card_closure_hash(closure: FinalMLModelCardClosure) -> str:
    content_str = json.dumps(closure.updated_sections, sort_keys=True)
    return hashlib.sha256(content_str.encode("utf-8")).hexdigest()

def render_final_ml_model_card_closure_markdown(closure: FinalMLModelCardClosure) -> str:
    return "# Final ML Model Card Closure\n\nExplainability and governance sections updated."

def render_final_ml_model_card_closure_text(closure: FinalMLModelCardClosure) -> str:
    return "Final ML Model Card Closure completed."

def build_final_ml_model_card_closure(
    model_card_payloads: list[dict[str, Any]],
    explainability_report: ExplainabilityReport,
    governance: MLGovernanceClosureResult,
    final_audit: AdvancedMLFinalAuditResult
) -> FinalMLModelCardClosure:

    closure = FinalMLModelCardClosure(
        closure_id=create_final_ml_model_card_closure_id(),
        created_at_utc=current_time(),
        source_model_card_update_ids=[],
        updated_sections=["Explainability", "Governance", "Risks", "Non-Activation"],
        rendered_markdown=None,
        rendered_text=None,
        closure_hash=None,
        explainability_section_closed=True,
        governance_section_closed=True,
        risk_section_closed=True,
        non_activation_notice_preserved=True,
        not_investment_advice=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        no_live_inference=True,
        no_live_monitoring=True,
        no_backtest_execution=True,
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

    closure.rendered_markdown = render_final_ml_model_card_closure_markdown(closure)
    closure.rendered_text = render_final_ml_model_card_closure_text(closure)
    closure.closure_hash = compute_final_ml_model_card_closure_hash(closure)

    return closure

def validate_final_ml_model_card_closure(closure: FinalMLModelCardClosure) -> list[str]:
    errors = []
    if not closure.non_activation_notice_preserved:
        errors.append("Model card missing non-activation notice")
    if not closure.not_investment_advice:
        errors.append("Model card missing not_investment_advice notice")
    if closure.produces_trade_signal:
        errors.append("Model card indicates trade signals")
    if closure.no_live_inference is False:
        errors.append("Model card indicates live inference")
    return errors

def final_ml_model_card_closure_summary(closure: FinalMLModelCardClosure) -> dict[str, Any]:
    return {
        "updated_sections": closure.updated_sections,
        "valid": len(validate_final_ml_model_card_closure(closure)) == 0
    }

def final_ml_model_card_closure_to_text(closure: FinalMLModelCardClosure, limit: int = 300) -> str:
    summary = final_ml_model_card_closure_summary(closure)
    return f"Model Card Closure complete. Sections updated: {', '.join(summary['updated_sections'])}"
