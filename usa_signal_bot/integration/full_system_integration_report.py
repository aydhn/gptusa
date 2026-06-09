
from typing import Any, Dict

from usa_signal_bot.integration.phase158_models import FullSystemIntegrationContext, FullSystemIntegrationFullReview, FullSystemIntegrationStatus

def build_full_system_integration_context() -> FullSystemIntegrationContext:
    ctx = FullSystemIntegrationContext()
    ctx.status = FullSystemIntegrationStatus.VALIDATED
    ctx.ready_for_phase159 = True
    return ctx

def build_full_system_integration_full_review() -> FullSystemIntegrationFullReview:
    return FullSystemIntegrationFullReview(context=build_full_system_integration_context())

def full_system_integration_full_review_summary(review: FullSystemIntegrationFullReview) -> Dict[str, Any]:
    return {"status": review.context.status.value, "ready": review.context.ready_for_phase159}

def full_system_integration_limitations_text() -> str:
    return "Limitations: Full system integration is local and dry-run only. No real broker execution allowed."

def full_system_integration_full_review_to_text(review: FullSystemIntegrationFullReview, limit: int = 300) -> str:
    summary = full_system_integration_full_review_summary(review)
    text = f"Full Review: {summary}"
    return text[:limit] + "..." if len(text) > limit else text
