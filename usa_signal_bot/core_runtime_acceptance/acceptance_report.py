from typing import Dict, Any, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    CoreRuntimeAcceptanceFullReview,
    LifecycleReviewIngestionResult,
    ConsolidationEvidenceItem,
    CoreRuntimeAcceptanceReport,
    AdvancedFoundationFreezeBundle,
    DataProviderExpansionKickoffGate,
    CoreRuntimeAcceptanceReportType,
    create_core_runtime_acceptance_full_review_id,
    _now
)

def build_core_runtime_acceptance_full_review(
    lifecycle: LifecycleReviewIngestionResult,
    evidence: List[ConsolidationEvidenceItem],
    acceptance: CoreRuntimeAcceptanceReport,
    freeze: AdvancedFoundationFreezeBundle,
    gate: DataProviderExpansionKickoffGate
) -> CoreRuntimeAcceptanceFullReview:
    return CoreRuntimeAcceptanceFullReview(
        review_id=create_core_runtime_acceptance_full_review_id(),
        created_at_utc=_now(),
        report_type=CoreRuntimeAcceptanceReportType.FULL_PHASE105_REVIEW,
        lifecycle_ingestion=lifecycle,
        evidence_items=evidence,
        acceptance_report=acceptance,
        foundation_freeze=freeze,
        kickoff_gate=gate
    )

def core_runtime_acceptance_full_review_summary(review: CoreRuntimeAcceptanceFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "accepted": review.acceptance_report.core_runtime_accepted,
        "frozen": review.foundation_freeze.frozen,
        "gate_passed": review.kickoff_gate.ready_for_phase106
    }

def phase105_limitations_text() -> str:
    return "Phase 105 is not activation. No broker API. No paper order. No paper mutation. No Telegram real send. No scraping. No HTML parsing. No dashboard. Not investment advice."

def core_runtime_acceptance_full_review_to_text(review: CoreRuntimeAcceptanceFullReview, limit: int = 300) -> str:
    return f"Core Runtime Acceptance Full Review: {review.review_id}"
