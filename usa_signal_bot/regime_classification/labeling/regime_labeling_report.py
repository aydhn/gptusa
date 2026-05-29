from typing import Any
from usa_signal_bot.core.enums import (
    RegimeLabelingStatus,
    RegimeLabelingDecision,
    RegimeLabelingReportType
)
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelingContext,
    RegimeLabelingFullReview,
    create_regime_labeling_context_id,
    create_regime_labeling_full_review_id,
    _now_utc
)

def build_regime_labeling_context() -> RegimeLabelingContext:
    return RegimeLabelingContext(
        context_id=create_regime_labeling_context_id(),
        created_at_utc=_now_utc(),
        status=RegimeLabelingStatus.CREATED,
        decision=RegimeLabelingDecision.UNKNOWN,
        source_regime_feature_engineering_review_id=None,
    )

def build_regime_labeling_full_review() -> RegimeLabelingFullReview:
    ctx = build_regime_labeling_context()
    return RegimeLabelingFullReview(
        review_id=create_regime_labeling_full_review_id(),
        created_at_utc=_now_utc(),
        report_type=RegimeLabelingReportType.FULL_PHASE128_REVIEW,
        ingestion=None,
        context=ctx,
        labeling_specs=[],
        label_results=[],
        window_results=[],
        label_sequences=[],
        stability_profiles=[],
        candidate_validation=None,
        readiness_gate=None
    )

def regime_labeling_full_review_summary(review: RegimeLabelingFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase129": review.context.ready_for_phase129 if review.context else False,
        "labeling_specs": len(review.labeling_specs),
        "heuristic_results": len(review.label_results),
        "rolling_windows": len(review.window_results),
        "sequences": len(review.label_sequences),
        "stability_profiles": len(review.stability_profiles),
    }

def regime_labeling_limitations_text() -> str:
    return """
Phase 128 Limitations:
- Phase 128 is NOT strategy activation or deployment.
- No trade signals, order decisions, or portfolio weights are generated.
- No ML model training or prediction occurs here.
- No broker API integration, real paper trading, or live execution is allowed.
- Local research data only.
- Deterministic and heuristic labeling approaches only.
"""

def regime_labeling_full_review_to_text(review: RegimeLabelingFullReview, limit: int = 300) -> str:
    summary = regime_labeling_full_review_summary(review)
    text = f"Review ID: {summary['review_id']}\n"
    text += f"Ready for Phase 129: {summary['ready_for_phase129']}\n"
    text += f"Specs: {summary['labeling_specs']}, Labels: {summary['heuristic_results']}, Windows: {summary['rolling_windows']}\n"
    text += regime_labeling_limitations_text()
    return text
