from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowMetricDirection, ShadowComparisonOutcome
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowMetricComparison, ShadowSessionComparisonReport,
    create_shadow_metric_comparison_id, create_shadow_session_comparison_report_id,
    ShadowAcceptanceGate, utc_now_iso
)
from usa_signal_bot.paper_shadow_governance.metric_extractor import extract_shadow_metrics

def infer_shadow_metric_higher_is_better(metric_name: str) -> bool:
    if "pnl" in metric_name or "return" in metric_name or metric_name in ["signal_count", "candidate_count", "ledger_event_count"]:
        return True
    return False

def compare_shadow_metric(metric_name: str, baseline_value: Any, candidate_value: Any, higher_is_better: bool = True) -> ShadowMetricComparison:
    bv = baseline_value if baseline_value is not None else 0.0
    cv = candidate_value if candidate_value is not None else 0.0
    try:
        delta = float(cv) - float(bv)
    except:
        delta = 0.0
    pct = (delta / abs(float(bv))) * 100 if bv else 0.0

    if delta > 0:
        dir = ShadowMetricDirection.IMPROVED if higher_is_better else ShadowMetricDirection.WORSENED
    elif delta < 0:
        dir = ShadowMetricDirection.WORSENED if higher_is_better else ShadowMetricDirection.IMPROVED
    else:
        dir = ShadowMetricDirection.UNCHANGED

    return ShadowMetricComparison(
        comparison_id=create_shadow_metric_comparison_id(metric_name),
        metric_name=metric_name,
        baseline_value=bv,
        candidate_value=cv,
        delta_value=delta,
        delta_pct=pct,
        direction=dir,
        higher_is_better=higher_is_better,
        interpretation=dir.value,
        warnings=[], errors=[]
    )

def determine_shadow_comparison_outcome(comparisons: List[ShadowMetricComparison], gates: List[ShadowAcceptanceGate] = None) -> ShadowComparisonOutcome:
    improved = sum(1 for c in comparisons if c.direction == ShadowMetricDirection.IMPROVED)
    worsened = sum(1 for c in comparisons if c.direction == ShadowMetricDirection.WORSENED)
    if improved > worsened:
        return ShadowComparisonOutcome.CANDIDATE_BETTER
    elif worsened > improved:
        return ShadowComparisonOutcome.BASELINE_BETTER
    return ShadowComparisonOutcome.MIXED

def compare_shadow_sessions(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowSessionComparisonReport:
    bm = extract_shadow_metrics(baseline_payload)
    cm = extract_shadow_metrics(candidate_payload)
    comps = []
    for k in set(bm.keys()).union(cm.keys()):
        comps.append(compare_shadow_metric(k, bm.get(k), cm.get(k), infer_shadow_metric_higher_is_better(k)))

    outcome = determine_shadow_comparison_outcome(comps)
    return ShadowSessionComparisonReport(
        report_id=create_shadow_session_comparison_report_id(),
        created_at_utc=utc_now_iso(),
        baseline_session_id=baseline_payload.get("session_id"),
        candidate_session_id=candidate_payload.get("session_id"),
        outcome=outcome,
        metric_comparisons=comps,
        risk_delta={}, safety_delta={}, ledger_completeness={}, notification_review={},
        acceptance_scorecard=None, summary={}, warnings=[], errors=[]
    )

def shadow_comparison_summary(report: ShadowSessionComparisonReport) -> Dict[str, Any]:
    return {"outcome": report.outcome.value, "metric_count": len(report.metric_comparisons)}

def shadow_session_comparator_to_text(report: ShadowSessionComparisonReport) -> str:
    return f"Comparison Report {report.report_id} - Outcome: {report.outcome.value}"
