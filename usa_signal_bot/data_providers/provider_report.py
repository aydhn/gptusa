
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderAbstractionFullReview, create_provider_abstraction_full_review_id, _now
from usa_signal_bot.core.enums import ProviderReportType
from usa_signal_bot.data_providers.provider_abstraction import build_default_provider_abstraction_context

def build_provider_abstraction_full_review() -> ProviderAbstractionFullReview:
    ctx = build_default_provider_abstraction_context()
    return ProviderAbstractionFullReview(
        review_id=create_provider_abstraction_full_review_id(),
        created_at_utc=_now(),
        report_type=ProviderReportType.FULL_PHASE106_REVIEW,
        kickoff_ingestion=ctx.kickoff_ingestion,
        context=ctx,
        registry_entries=ctx.registry_entries,
        adapter_specs=[],
        capability_matrix=ctx.capability_matrix,
        safety_policy=ctx.safety_policy,
        fallback_plans=ctx.fallback_plans,
        output_paths={}
    )

def provider_abstraction_full_review_summary(review: ProviderAbstractionFullReview) -> dict[str, Any]:
    return {"type": review.report_type}

def provider_abstraction_limitations_text() -> str:
    return "Phase 106 is metadata only. No real fetch occurs."

def provider_abstraction_full_review_to_text(review: ProviderAbstractionFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id}: {review.report_type}"
