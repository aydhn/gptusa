"""Position sizing attribution and allocation status mapping."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension

def sizing_status_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_pnl_by_dimension(events, AttributionDimension.SIZING_STATUS)

def sizing_multiplier_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    # Placeholder for actual multiplier tracking
    return {"average_multiplier": 1.0}

def sizing_blocked_or_reduced_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    stats = sizing_status_attribution(events)
    summary = {}
    for s in stats:
        if s.name in ["REDUCED", "CAPPED", "BLOCKED", "SUPPRESSED", "THROTTLED"]:
            summary[s.name] = {"count": s.trade_count, "net_pnl": s.net_pnl_usd}
    return summary

def estimate_sizing_contribution_proxy(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    return {"sizing_value_add_usd": 0.0}

def sizing_attribution_to_text(events: List[AttributionTradeEvent]) -> str:
    stats = sizing_status_attribution(events)
    lines = ["--- Sizing Attribution ---"]
    for s in stats:
        lines.append(f"{s.name}: Net PnL: ${s.net_pnl_usd:.2f} (Trades: {s.trade_count})")
    return "\n".join(lines)
