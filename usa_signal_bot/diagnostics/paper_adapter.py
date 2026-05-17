from typing import Any, Dict
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticReview, DiagnosticReportType, create_diagnostic_review_id
from usa_signal_bot.diagnostics.event_normalizer import diagnostic_events_from_paper_payload
from usa_signal_bot.diagnostics.backtest_adapter import build_diagnostic_review_from_backtest_result
from datetime import datetime, timezone

def build_diagnostic_review_from_paper_payload(payload: Dict[str, Any]) -> DiagnosticReview:
    events = diagnostic_events_from_paper_payload(payload)
    # Simulate full review process using existing adapter as base
    review = build_diagnostic_review_from_backtest_result({"trades": payload.get("closed_trades", [])})
    review.report_type = DiagnosticReportType.FULL_DIAGNOSTICS_REVIEW
    return review

def attach_diagnostics_to_paper_analytics(payload: Dict[str, Any], review: DiagnosticReview = None) -> Dict[str, Any]:
    if review is None:
        review = build_diagnostic_review_from_paper_payload(payload)

    if "metadata" not in payload:
        payload["metadata"] = {}

    payload["metadata"]["diagnostics"] = {
        "review_id": review.review_id,
        "diagnostic_status": review.scorecard.diagnostic_status.value if review.scorecard else "UNKNOWN",
        "failure_mode_count": len(review.failure_assessments),
        "remediation_hint_count": len(review.remediation_hints)
    }
    return payload

def paper_diagnostics_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("metadata", {}).get("diagnostics", {})

def paper_diagnostics_warnings(payload: Dict[str, Any]) -> list[str]:
    diags = paper_diagnostics_summary(payload)
    warnings = []
    if diags.get("diagnostic_status") in ["DEGRADED", "FAILING"]:
        warnings.append("Paper diagnostics indicate degraded performance.")
    return warnings
