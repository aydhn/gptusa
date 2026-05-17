from typing import Any, Dict
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticReview, DiagnosticReportType, create_diagnostic_review_id
from usa_signal_bot.diagnostics.event_normalizer import normalize_diagnostic_events
from usa_signal_bot.core.enums import DiagnosticScope
from usa_signal_bot.diagnostics.backtest_adapter import build_diagnostic_review_from_backtest_result
from datetime import datetime, timezone

def build_diagnostics_by_walk_forward_window(result: Dict[str, Any]) -> Dict[str, DiagnosticReview]:
    reviews = {}
    windows = result.get("windows", [])
    for idx, w in enumerate(windows):
        # Trick: Treat window like a backtest result
        review = build_diagnostic_review_from_backtest_result(w)
        reviews[f"window_{idx}"] = review
    return reviews

def attach_diagnostics_to_walk_forward_result(result: Dict[str, Any], reviews_by_window: Dict[str, DiagnosticReview] = None) -> Dict[str, Any]:
    if reviews_by_window is None:
        reviews_by_window = build_diagnostics_by_walk_forward_window(result)

    if "metadata" not in result:
        result["metadata"] = {}

    degraded_windows = 0
    for w_name, rev in reviews_by_window.items():
        if rev.scorecard and rev.scorecard.diagnostic_status.value in ["DEGRADED", "FAILING"]:
            degraded_windows += 1

    result["metadata"]["diagnostics"] = {
        "total_windows_analyzed": len(reviews_by_window),
        "degraded_windows": degraded_windows,
        "oos_degradation_warning": degraded_windows > 0
    }
    return result

def walk_forward_diagnostics_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("metadata", {}).get("diagnostics", {})

def walk_forward_diagnostics_warnings(result: Dict[str, Any]) -> list[str]:
    diags = walk_forward_diagnostics_summary(result)
    warnings = []
    if diags.get("oos_degradation_warning"):
        warnings.append("Walk-forward analysis shows degradation in OOS windows.")
    return warnings
