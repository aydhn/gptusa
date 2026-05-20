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
