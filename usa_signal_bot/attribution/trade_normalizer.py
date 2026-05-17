"""Normalizes diverse trade event payloads into AttributionTradeEvent."""

from typing import Any, Dict, List, Optional
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, create_attribution_trade_event_id

def infer_signal_family(payload: Dict[str, Any]) -> Optional[str]:
    family = payload.get("signal_family")
    if family:
        return family
    signal_id = payload.get("signal_id")
    if signal_id:
        return signal_id.split("_")[0]
    strategy = payload.get("strategy_name")
    if strategy:
        return strategy.split("_")[0]
    return None

def infer_cost_fields(payload: Dict[str, Any]) -> Dict[str, Optional[float]]:
    total = payload.get("total_cost_usd")
    if total is None and payload.get("cost_usd") is not None:
        total = payload.get("cost_usd")

    if total is None:
        return {"total_cost_usd": None, "slippage_cost_usd": None, "market_impact_cost_usd": None}

    slippage = payload.get("slippage_cost_usd", payload.get("slippage_usd"))
    impact = payload.get("market_impact_cost_usd", payload.get("market_impact_usd"))
    return {
        "total_cost_usd": float(total),
        "slippage_cost_usd": float(slippage) if slippage is not None else None,
        "market_impact_cost_usd": float(impact) if impact is not None else None
    }

def normalize_trade_event(payload: Dict[str, Any]) -> AttributionTradeEvent:
    symbol = payload.get("symbol", "UNKNOWN")
    gross_pnl = payload.get("gross_pnl_usd")
    net_pnl = payload.get("net_pnl_usd")

    costs = infer_cost_fields(payload)

    if net_pnl is None and gross_pnl is not None and costs["total_cost_usd"] is not None:
        net_pnl = float(gross_pnl) - float(costs["total_cost_usd"])

    qty = payload.get("quantity")
    notional = payload.get("notional_usd", payload.get("notional"))

    metadata = payload.get("metadata", {})
    if "spread_cost_usd" in payload:
        metadata["spread_cost_usd"] = payload["spread_cost_usd"]

    return AttributionTradeEvent(
        event_id=payload.get("event_id") or create_attribution_trade_event_id(symbol),
        symbol=str(symbol),
        timestamp_utc=payload.get("timestamp_utc", payload.get("timestamp", payload.get("date"))),
        strategy_name=payload.get("strategy_name", payload.get("strategy")),
        signal_id=payload.get("signal_id"),
        signal_family=infer_signal_family(payload),
        side=payload.get("side", payload.get("action")),
        quantity=float(qty) if qty is not None else None,
        notional_usd=float(notional) if notional is not None else None,
        gross_pnl_usd=float(gross_pnl) if gross_pnl is not None else None,
        net_pnl_usd=float(net_pnl) if net_pnl is not None else None,
        total_cost_usd=costs["total_cost_usd"],
        slippage_cost_usd=costs["slippage_cost_usd"],
        market_impact_cost_usd=costs["market_impact_cost_usd"],
        sector=payload.get("sector"),
        cluster=payload.get("cluster"),
        regime_label=payload.get("regime_label", payload.get("regime")),
        liquidity_bucket=payload.get("liquidity_bucket", payload.get("liquidity")),
        risk_bucket=payload.get("risk_bucket", payload.get("risk")),
        sizing_status=payload.get("sizing_status", payload.get("status")),
        rebalance_action_type=payload.get("rebalance_action_type", payload.get("rebalance_action")),
        metadata=metadata
    )

def normalize_trade_events(payloads: List[Dict[str, Any]]) -> List[AttributionTradeEvent]:
    return [normalize_trade_event(p) for p in payloads]

def normalize_backtest_trades(result: Dict[str, Any]) -> List[AttributionTradeEvent]:
    trades = result.get("trades", [])
    if not trades and "events" in result:
        trades = result["events"]
    return normalize_trade_events(trades)

def normalize_paper_trades(payload: Dict[str, Any]) -> List[AttributionTradeEvent]:
    trades = payload.get("closed_trades", payload.get("trades", []))
    return normalize_trade_events(trades)

def normalize_rebalance_actions(payload: Dict[str, Any]) -> List[AttributionTradeEvent]:
    actions = payload.get("rebalance_actions", payload.get("actions", []))
    events = []
    for action in actions:
        norm = normalize_trade_event(action)
        if not norm.rebalance_action_type:
            norm.rebalance_action_type = action.get("action_type", "UNKNOWN")
        events.append(norm)
    return events

def trade_events_to_text(events: List[AttributionTradeEvent], limit: int = 50) -> str:
    lines = [f"--- Attribution Trade Events ({len(events)} total) ---"]
    for i, e in enumerate(events[:limit]):
        net = f"{e.net_pnl_usd:.2f}" if e.net_pnl_usd is not None else "N/A"
        gross = f"{e.gross_pnl_usd:.2f}" if e.gross_pnl_usd is not None else "N/A"
        cost = f"{e.total_cost_usd:.2f}" if e.total_cost_usd is not None else "N/A"
        lines.append(f"[{e.timestamp_utc or 'NO_DATE'}] {e.symbol} {e.side or 'UNK'}: Net PnL: ${net} (Gross: ${gross}, Cost: ${cost}) - Strat: {e.strategy_name or 'UNK'}")
    if len(events) > limit:
        lines.append(f"... and {len(events) - limit} more events.")
    return "\n".join(lines)
