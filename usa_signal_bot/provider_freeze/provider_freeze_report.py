from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeContext,
    ProviderFreezeFullReview,
    create_provider_freeze_context_id,
    create_provider_freeze_full_review_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import ProviderFreezeStatus, ProviderFreezeDecision, ProviderFreezeReportType
from typing import Any, Dict

def build_provider_freeze_context() -> ProviderFreezeContext:
    return ProviderFreezeContext(
        context_id=create_provider_freeze_context_id(),
        created_at_utc=_utcnow_str(),
        status=ProviderFreezeStatus.DRAFT,
        decision=ProviderFreezeDecision.UNKNOWN
    )

def build_provider_freeze_full_review() -> ProviderFreezeFullReview:
    return ProviderFreezeFullReview(
        review_id=create_provider_freeze_full_review_id(),
        created_at_utc=_utcnow_str(),
        report_type=ProviderFreezeReportType.FULL_PHASE114_REVIEW
    )

def provider_freeze_full_review_summary(review: ProviderFreezeFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "context_id": review.context.context_id,
        "ready_for_phase115": review.context.ready_for_phase115,
        "freeze_valid": review.freeze_bundle.freeze_valid,
        "multi_provider_review_passed": review.multi_provider_review.multi_provider_review_passed,
        "rehearsal_passed": review.rehearsal_report.rehearsal_passed,
        "errors": len(review.errors),
        "warnings": len(review.warnings)
    }

def provider_freeze_limitations_text() -> str:
    return """Phase 114 Limitations:
- This is NOT an active paper trading phase.
- No broker orders, no paper state mutations, no live Telegram messages, no dashboard.
- No web scraping, no HTML parsing, no paid APIs, no network fetches during tests.
- Rehearsals operate purely on metadata and offline artifacts.
- "Ready for Phase 115" does NOT constitute an approval for live trading."""

def provider_freeze_full_review_to_text(review: ProviderFreezeFullReview, limit: int = 300) -> str:
    lines = [
        f"Provider Freeze Full Review: {review.review_id}",
        f"Ready for Phase 115: {review.context.ready_for_phase115}",
        f"Freeze Valid: {review.freeze_bundle.freeze_valid}",
        f"Review Passed: {review.multi_provider_review.multi_provider_review_passed}",
        f"Rehearsal Passed: {review.rehearsal_report.rehearsal_passed}"
    ]
    if review.errors:
        lines.append("\nErrors:")
        for e in review.errors[:limit]:
            lines.append(f" - {e}")
    if review.warnings:
        lines.append("\nWarnings:")
        for w in review.warnings[:limit]:
            lines.append(f" - {w}")
    lines.append("\n" + provider_freeze_limitations_text())
    return "\n".join(lines)
