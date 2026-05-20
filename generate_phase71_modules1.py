import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

write_file("usa_signal_bot/paper_shadow_governance/__init__.py", """
# Paper Shadow Governance module
""")

write_file("usa_signal_bot/paper_shadow_governance/session_ingestion.py", """
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ShadowComparisonRole

def extract_shadow_session_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("session_id") or payload.get("id")

def extract_shadow_session_role(payload: Dict[str, Any]) -> ShadowComparisonRole:
    role_str = payload.get("metadata", {}).get("role", "UNKNOWN")
    try:
        return ShadowComparisonRole(role_str)
    except ValueError:
        return ShadowComparisonRole.UNKNOWN

def extract_shadow_session_safety_flags(payload: Dict[str, Any]) -> List[str]:
    return payload.get("safety_flags", [])

def shadow_session_ingestion_warnings(payload: Dict[str, Any]) -> List[str]:
    warnings = []
    if not extract_shadow_session_id(payload):
        warnings.append("Missing session_id in payload.")
    flags = extract_shadow_session_safety_flags(payload)
    if "REAL_ORDER_RISK" in flags or "PAPER_MUTATION_RISK" in flags:
        warnings.append("Critical safety risk flag detected in ingestion.")
    return warnings

def ingest_shadow_session_payload(payload: Dict[str, Any], role: ShadowComparisonRole = ShadowComparisonRole.UNKNOWN) -> Dict[str, Any]:
    cleaned = payload.copy()
    if "metadata" not in cleaned:
        cleaned["metadata"] = {}
    cleaned["metadata"]["ingested_role"] = role.value
    cleaned["ingestion_warnings"] = shadow_session_ingestion_warnings(cleaned)
    return cleaned

def ingest_shadow_sessions(baseline_payload: Optional[Dict[str, Any]], candidate_payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    res = {}
    if baseline_payload:
        res["baseline"] = ingest_shadow_session_payload(baseline_payload, ShadowComparisonRole.BASELINE)
    else:
        res["baseline"] = None
    if candidate_payload:
        res["candidate"] = ingest_shadow_session_payload(candidate_payload, ShadowComparisonRole.CANDIDATE)
    else:
        res["candidate"] = None
    return res

def shadow_session_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return f"Shadow Ingestion [Role: {payload.get('metadata', {}).get('ingested_role')}] - ID: {extract_shadow_session_id(payload)}"
""")

write_file("usa_signal_bot/paper_shadow_governance/metric_extractor.py", """
from typing import Any, Dict, List, Optional

def required_shadow_comparison_metrics() -> List[str]:
    return [
        "signal_count", "candidate_count", "intent_count",
        "risk_approved_intent_count", "blocked_intent_count",
        "simulated_fill_count", "simulated_total_cost_usd",
        "simulated_slippage_usd", "simulated_pnl_usd",
        "return_pct", "max_drawdown_pct", "safety_flag_count",
        "ledger_event_count", "notification_warning_count"
    ]

def extract_shadow_counts(session_payload: Dict[str, Any]) -> Dict[str, int]:
    m = session_payload.get("metrics", {})
    return {
        "signal_count": m.get("signal_count", 0),
        "candidate_count": m.get("candidate_count", 0),
        "intent_count": m.get("intent_count", 0),
        "risk_approved_intent_count": m.get("risk_approved_intent_count", 0),
        "blocked_intent_count": m.get("blocked_intent_count", 0),
        "simulated_fill_count": m.get("simulated_fill_count", 0),
        "safety_flag_count": len(session_payload.get("safety_flags", [])),
        "ledger_event_count": len(session_payload.get("ledger", [])),
        "notification_warning_count": m.get("notification_warning_count", 0)
    }

def extract_shadow_pnl_metrics(session_payload: Dict[str, Any]) -> Dict[str, Optional[float]]:
    m = session_payload.get("metrics", {})
    return {
        "simulated_pnl_usd": m.get("simulated_pnl_usd", 0.0),
        "return_pct": m.get("return_pct", 0.0),
        "max_drawdown_pct": m.get("max_drawdown_pct", 0.0)
    }

def extract_shadow_cost_metrics(session_payload: Dict[str, Any]) -> Dict[str, Optional[float]]:
    m = session_payload.get("metrics", {})
    return {
        "simulated_total_cost_usd": m.get("simulated_total_cost_usd", 0.0),
        "simulated_slippage_usd": m.get("simulated_slippage_usd", 0.0)
    }

def extract_shadow_safety_metrics(session_payload: Dict[str, Any]) -> Dict[str, int]:
    return {
        "safety_flag_count": len(session_payload.get("safety_flags", []))
    }

def extract_shadow_metrics(session_payload: Dict[str, Any]) -> Dict[str, Any]:
    metrics = {}
    metrics.update(extract_shadow_counts(session_payload))
    metrics.update(extract_shadow_pnl_metrics(session_payload))
    metrics.update(extract_shadow_cost_metrics(session_payload))
    return metrics

def shadow_metrics_quality_warnings(metrics: Dict[str, Any]) -> List[str]:
    req = required_shadow_comparison_metrics()
    missing = [m for m in req if m not in metrics or metrics[m] is None]
    if missing:
        return [f"Missing metrics: {missing}"]
    return []

def shadow_metric_extractor_to_text(metrics: Dict[str, Any]) -> str:
    return str(metrics)
""")

write_file("usa_signal_bot/paper_shadow_governance/session_comparator.py", """
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
""")

print("Modules 1 generated successfully.")
