"""Time-window based performance and risk attribution."""

from typing import Any, Dict, List
from collections import defaultdict
import datetime

from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution, RiskAttributionContribution
from usa_signal_bot.attribution.pnl_attribution import calculate_contribution_for_group
from usa_signal_bot.attribution.drawdown_attribution import drawdown_contribution_by_dimension

def _get_window_key(timestamp: str, window: str) -> str:
    if not timestamp:
        return "UNKNOWN_DATE"

    formats = {
        "daily": "%Y-%m-%d",
        "weekly": "%Y-W%W",
        "monthly": "%Y-%m",
        "yearly": "%Y",
    }

    if window not in formats:
        return "UNKNOWN_DATE"

    try:
        dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime(formats[window])
    except ValueError:
        return "UNKNOWN_DATE"

def group_events_by_time_window(events: List[AttributionTradeEvent], window: str = "monthly") -> Dict[str, List[AttributionTradeEvent]]:
    groups = defaultdict(list)
    for e in events:
        key = _get_window_key(e.timestamp_utc, window)
        groups[key].append(e)
    return dict(groups)

def time_window_performance_attribution(events: List[AttributionTradeEvent], window: str = "monthly") -> List[AttributionContribution]:
    groups = group_events_by_time_window(events, window)
    total_net = sum(e.net_pnl_usd for e in events if e.net_pnl_usd is not None)

    contribs = []
    for name, grp in groups.items():
        contribs.append(calculate_contribution_for_group(name, AttributionDimension.TIMEFRAME, grp, total_net))

    return sorted(contribs, key=lambda x: x.name) # Sort chronologically

def time_window_risk_attribution(events: List[AttributionTradeEvent], window: str = "monthly") -> List[RiskAttributionContribution]:
    groups = group_events_by_time_window(events, window)
    contribs = []
    for name, grp in groups.items():
        dd = drawdown_contribution_by_dimension(grp, AttributionDimension.TIMEFRAME)
        if dd:
            dd[0].name = name
            contribs.append(dd[0])
    return sorted(contribs, key=lambda x: x.name)

def time_window_signal_summary(events: List[AttributionTradeEvent], window: str = "monthly") -> Dict[str, Any]:
    perf = time_window_performance_attribution(events, window)
    summary = {}
    for p in perf:
        summary[p.name] = {"net_pnl": p.net_pnl_usd, "win_rate": p.win_rate}
    return summary

def time_window_attribution_to_text(contributions: List[AttributionContribution], limit: int = 100) -> str:
    lines = ["--- Time Window Attribution ---"]
    for c in contributions[:limit]:
        lines.append(f"[{c.name}] Net PnL: ${c.net_pnl_usd:.2f} (Trades: {c.trade_count}, WR: {c.win_rate or 0:.1f}%)")
    return "\n".join(lines)
