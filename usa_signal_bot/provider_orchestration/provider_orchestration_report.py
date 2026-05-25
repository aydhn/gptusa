from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ProviderOrchestrationStatus, ProviderOrchestrationDecision, ProviderOrchestrationReportType
from usa_signal_bot.provider_orchestration.phase110_models import (
    ProviderOrchestrationContext, ProviderOrchestrationFullReview,
    create_provider_orchestration_context_id, create_provider_orchestration_full_review_id
)

def build_provider_orchestration_context() -> ProviderOrchestrationContext:
    return ProviderOrchestrationContext(
        context_id=create_provider_orchestration_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=ProviderOrchestrationStatus.CREATED,
        decision=ProviderOrchestrationDecision.UNKNOWN,
        source_provider_quality_review_id=None,
        metadata_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_provider_orchestration_full_review() -> ProviderOrchestrationFullReview:
    return ProviderOrchestrationFullReview(
        review_id=create_provider_orchestration_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=ProviderOrchestrationReportType.FULL_PHASE110_REVIEW,
        warnings=[],
        errors=[],
        output_paths={}
    )

def provider_orchestration_full_review_summary(review: ProviderOrchestrationFullReview) -> dict[str, Any]:
    return {
        "id": review.review_id,
        "type": review.report_type.value,
        "plans": len(review.route_plans),
        "results": len(review.route_results)
    }

def provider_orchestration_limitations_text() -> str:
    return """
--- Phase 110 Provider Orchestration Limitations ---
- Phase 110 is NOT activation.
- NO broker API. NO paper orders. NO paper mutation.
- NO Telegram real send. NO scraping. NO HTML parsing. NO dashboard.
- NO paid API. Tests do NOT use real networks.
- Provider routes and blends are NOT trade signals or investment advice.
- Refresh plans do NOT fetch real data.
"""

def provider_orchestration_full_review_to_text(review: ProviderOrchestrationFullReview, limit: int = 300) -> str:
    lines = [
        f"--- Full Provider Orchestration Review ---",
        f"ID: {review.review_id}",
        f"Type: {review.report_type.value}",
        f"Route Plans: {len(review.route_plans)}",
        f"Route Results: {len(review.route_results)}",
        f"Blend Results: {len(review.blend_results)}"
    ]
    if review.context:
        lines.append(f"Context Status: {review.context.status.value}")
    if review.errors:
        lines.append(f"Errors: {review.errors}")
    return "\n".join(lines)
