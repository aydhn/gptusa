from datetime import datetime, timezone
from typing import Any, Dict

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderRuntimeContext,
    ProviderRuntimeFullReview,
    create_provider_runtime_context_id,
    create_provider_runtime_full_review_id
)
from usa_signal_bot.core.enums import ProviderRuntimeStatus, ProviderRuntimeDecision

def build_provider_runtime_context() -> ProviderRuntimeContext:
    return ProviderRuntimeContext(
        context_id=create_provider_runtime_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=ProviderRuntimeStatus.DRAFT,
        decision=ProviderRuntimeDecision.UNKNOWN
    )

def build_provider_runtime_full_review() -> ProviderRuntimeFullReview:
    return ProviderRuntimeFullReview(
        review_id=create_provider_runtime_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

def provider_runtime_full_review_summary(review: ProviderRuntimeFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "context_id": review.context.context_id,
        "adapter_count": len(review.adapter_specs),
        "dry_run_count": len(review.dry_run_results),
        "contract_tests_passed": review.contract_test_report.contract_tests_passed
    }

def provider_runtime_limitations_text() -> str:
    return """
LIMITATIONS:
- This is NOT an active paper trading environment.
- This is NOT a live execution environment.
- Broker API integration is EXPLICITLY PROHIBITED.
- Real paper state mutation is EXPLICITLY PROHIBITED.
- Telegram real send is EXPLICITLY PROHIBITED.
- Web scraping and HTML parsing are EXPLICITLY PROHIBITED.
- Paid APIs are EXPLICITLY PROHIBITED.
- Network fetch is DISABLED by default. Real network tests are EXPLICITLY PROHIBITED.
- PASS results do NOT constitute live trading approval or investment advice.
"""

def provider_runtime_full_review_to_text(review: ProviderRuntimeFullReview, limit: int = 300) -> str:
    lines = [
        "=== Provider Runtime Full Review ===",
        f"Review ID: {review.review_id}",
        f"Context ID: {review.context.context_id}",
        f"Adapter Count: {len(review.adapter_specs)}",
        f"Dry Run Count: {len(review.dry_run_results)}",
        f"Contract Tests Passed: {review.contract_test_report.contract_tests_passed}",
        provider_runtime_limitations_text()
    ]
    return "\n".join(lines)
