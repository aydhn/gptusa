from typing import Any, Dict
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeFinalClosureContext,
    RegimeFinalClosureFullReview,
    RegimeFinalClosureStatus,
    RegimeFinalClosureDecision,
    RegimeFinalClosureReportType,
    create_regime_final_closure_context_id,
    create_regime_final_closure_full_review_id
)
from datetime import datetime, timezone

def build_regime_final_closure_context() -> RegimeFinalClosureContext:
    return RegimeFinalClosureContext(
        context_id=create_regime_final_closure_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=RegimeFinalClosureStatus.DRAFT,
        decision=RegimeFinalClosureDecision.UNKNOWN
    )

def build_regime_final_closure_full_review() -> RegimeFinalClosureFullReview:
    ctx = build_regime_final_closure_context()
    return RegimeFinalClosureFullReview(
        review_id=create_regime_final_closure_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=RegimeFinalClosureReportType.FULL_PHASE135_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        artifact_chain_validation=ctx.artifact_chain_validation,
        final_closure_result=ctx.final_closure_result,
        freeze_seal=ctx.freeze_seal,
        final_safety_audit=ctx.final_safety_audit,
        ml_input_contract=ctx.ml_input_contract,
        ml_kickoff_gate=ctx.ml_kickoff_gate
    )

def regime_final_closure_full_review_summary(review: RegimeFinalClosureFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id}

def regime_final_closure_limitations_text() -> str:
    return "Phase 135 is research closure only. No trading, no deployment, no model training."

def regime_final_closure_full_review_to_text(review: RegimeFinalClosureFullReview, limit: int = 300) -> str:
    return f"Review ID: {review.review_id}\nType: {review.report_type.name}"
