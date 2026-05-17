from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticReview, DiagnosticReportType, FailureModeAssessment
from usa_signal_bot.diagnostics.event_normalizer import diagnostic_events_from_attribution_review
from usa_signal_bot.diagnostics.backtest_adapter import build_diagnostic_review_from_backtest_result

def build_diagnostics_from_attribution_review(attribution_payload: Dict[str, Any]) -> DiagnosticReview:
    events = diagnostic_events_from_attribution_review(attribution_payload)
    return build_diagnostic_review_from_backtest_result({"trades": [e.__dict__ for e in events]})

def attribution_negative_contributor_diagnostics(attribution_payload: Dict[str, Any]) -> List[FailureModeAssessment]:
    review = build_diagnostics_from_attribution_review(attribution_payload)
    return review.failure_assessments

def attribution_cost_degradation_diagnostics(attribution_payload: Dict[str, Any]) -> List[FailureModeAssessment]:
    review = build_diagnostics_from_attribution_review(attribution_payload)
    return [a for a in review.failure_assessments if a.failure_mode.value in ["COST_DRAG_ERASED_EDGE", "HIGH_SLIPPAGE", "HIGH_MARKET_IMPACT"]]

def attach_diagnostics_to_attribution_review(attribution_payload: Dict[str, Any], diagnostic_review: DiagnosticReview) -> Dict[str, Any]:
    if "metadata" not in attribution_payload:
        attribution_payload["metadata"] = {}
    attribution_payload["metadata"]["diagnostics"] = {
        "review_id": diagnostic_review.review_id,
        "diagnostic_status": diagnostic_review.scorecard.diagnostic_status.value if diagnostic_review.scorecard else "UNKNOWN",
        "failure_modes": len(diagnostic_review.failure_assessments)
    }
    return attribution_payload

def attribution_diagnostics_adapter_to_text(payload: Dict[str, Any]) -> str:
    diags = payload.get("metadata", {}).get("diagnostics", {})
    return f"Attribution Diagnostics: Status {diags.get('diagnostic_status')}, Failures: {diags.get('failure_modes')}"
