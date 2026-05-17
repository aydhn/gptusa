"""Rebalance action and turnover cost attribution."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension

def rebalance_action_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_pnl_by_dimension(events, AttributionDimension.REBALANCE_ACTION)

def turnover_cost_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    # Reuse rebalance_action_attribution, sorted by cost
    contribs = rebalance_action_attribution(events)
    return sorted(contribs, key=lambda x: x.total_cost_usd, reverse=True)

def rebalance_pnl_proxy_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    contribs = rebalance_action_attribution(events)
    return {c.name: c.net_pnl_usd for c in contribs}

def rebalance_cost_drag_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    contribs = turnover_cost_attribution(events)
    summary = {}
    for c in contribs:
        if c.gross_pnl_usd and c.gross_pnl_usd > 0:
            summary[c.name] = (c.total_cost_usd / c.gross_pnl_usd) * 100.0
        else:
            summary[c.name] = None
    return summary

def rebalance_attribution_to_text(events: List[AttributionTradeEvent]) -> str:
    contribs = rebalance_action_attribution(events)
    lines = ["--- Rebalance Action Attribution ---"]
    for c in contribs:
        lines.append(f"{c.name}: Net PnL: ${c.net_pnl_usd:.2f} | Cost: ${c.total_cost_usd:.2f} | Trades: {c.trade_count}")
    return "\n".join(lines)
