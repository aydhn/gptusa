from typing import Any, Dict, List, Optional
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticEvent, create_diagnostic_event_id
from usa_signal_bot.core.enums import DiagnosticScope
from usa_signal_bot.core.exceptions import DiagnosticEventNormalizationError

def normalize_diagnostic_event(payload: Dict[str, Any], scope: Optional[DiagnosticScope] = None) -> DiagnosticEvent:
    if scope is None:
        scope = infer_diagnostic_scope(payload)

    warnings = []

    # Redact broker fields
    for k in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if k in payload:
            payload[k] = "REDACTED"

    net_pnl = payload.get("net_pnl_usd") or payload.get("net_profit") or payload.get("pnl")
    gross_pnl = payload.get("gross_pnl_usd") or payload.get("gross_profit")
    cost = payload.get("total_cost_usd") or payload.get("cost") or payload.get("fees", 0.0)

    if net_pnl is None:
        warnings.append("Missing net_pnl_usd")
    if gross_pnl is None and net_pnl is not None:
        gross_pnl = net_pnl + cost

    event = DiagnosticEvent(
        event_id=payload.get("event_id") or payload.get("trade_id") or payload.get("signal_id") or create_diagnostic_event_id(payload.get("symbol")),
        scope=scope,
        symbol=payload.get("symbol"),
        strategy_name=payload.get("strategy_name") or payload.get("strategy"),
        signal_id=payload.get("signal_id"),
        signal_family=payload.get("signal_family"),
        timestamp_utc=payload.get("timestamp_utc") or payload.get("timestamp") or payload.get("date"),
        side=payload.get("side") or payload.get("direction"),
        gross_pnl_usd=gross_pnl,
        net_pnl_usd=net_pnl,
        total_cost_usd=cost,
        return_pct=payload.get("return_pct"),
        drawdown_impact_usd=payload.get("drawdown_impact_usd"),
        signal_score=payload.get("signal_score") or payload.get("score"),
        confidence=payload.get("confidence"),
        regime_label=payload.get("regime_label") or payload.get("regime"),
        sector=payload.get("sector"),
        cluster=payload.get("cluster"),
        liquidity_bucket=payload.get("liquidity_bucket"),
        cost_bucket=payload.get("cost_bucket"),
        sizing_status=payload.get("sizing_status"),
        rebalance_action_type=payload.get("rebalance_action_type"),
        metadata=infer_failure_relevant_fields(payload),
        warnings=warnings
    )
    return event

def normalize_diagnostic_events(payloads: List[Dict[str, Any]], scope: Optional[DiagnosticScope] = None) -> List[DiagnosticEvent]:
    return [normalize_diagnostic_event(p, scope) for p in payloads]

def diagnostic_events_from_backtest_result(result: Dict[str, Any]) -> List[DiagnosticEvent]:
    events = result.get("trades", [])
    if not events:
        events = result.get("events", [])
    return normalize_diagnostic_events(events, DiagnosticScope.TRADE)

def diagnostic_events_from_walk_forward_result(result: Dict[str, Any]) -> List[DiagnosticEvent]:
    events = []
    for w in result.get("windows", []):
        events.extend(w.get("trades", []))
    return normalize_diagnostic_events(events, DiagnosticScope.TRADE)

def diagnostic_events_from_paper_payload(payload: Dict[str, Any]) -> List[DiagnosticEvent]:
    events = payload.get("closed_trades", [])
    if not events:
        events = payload.get("trades", [])
    return normalize_diagnostic_events(events, DiagnosticScope.TRADE)

def diagnostic_events_from_attribution_review(payload: Dict[str, Any]) -> List[DiagnosticEvent]:
    events = payload.get("trades", [])
    if not events:
        events = payload.get("events", [])
    return normalize_diagnostic_events(events, DiagnosticScope.TRADE)

def infer_diagnostic_scope(payload: Dict[str, Any]) -> DiagnosticScope:
    if "trade_id" in payload or "net_profit" in payload or "net_pnl_usd" in payload:
        return DiagnosticScope.TRADE
    if "signal_id" in payload or "direction" in payload:
        return DiagnosticScope.SIGNAL
    return DiagnosticScope.UNKNOWN

def infer_failure_relevant_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if isinstance(v, (str, int, float, bool)) and k not in [
        "event_id", "trade_id", "signal_id", "symbol", "strategy_name", "strategy",
        "signal_family", "timestamp_utc", "timestamp", "date", "side", "direction",
        "gross_pnl_usd", "gross_profit", "net_pnl_usd", "net_profit", "pnl",
        "total_cost_usd", "cost", "fees", "return_pct", "drawdown_impact_usd",
        "signal_score", "score", "confidence", "regime_label", "regime",
        "sector", "cluster", "liquidity_bucket", "cost_bucket", "sizing_status",
        "rebalance_action_type"
    ]}

def diagnostic_events_to_text(events: List[DiagnosticEvent], limit: int = 50) -> str:
    lines = [f"Diagnostic Events (Total: {len(events)}, Showing top {min(len(events), limit)}):"]
    for i, evt in enumerate(events[:limit]):
        lines.append(f"  {i+1}. [{evt.event_id}] {evt.symbol} {evt.side} - Net PnL: {evt.net_pnl_usd} | Scope: {evt.scope.value}")
    return "\n".join(lines)
