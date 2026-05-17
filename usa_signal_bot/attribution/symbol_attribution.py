"""Symbol-level performance and cost attribution."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension
from usa_signal_bot.attribution.cost_attribution import calculate_cost_drag_pct

def symbol_performance_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_pnl_by_dimension(events, AttributionDimension.SYMBOL)

def top_symbol_contributors(events: List[AttributionTradeEvent], top_n: int = 10) -> List[AttributionContribution]:
    contributions = symbol_performance_attribution(events)
    # Sort descending by net PnL
    return sorted(contributions, key=lambda x: x.net_pnl_usd, reverse=True)[:top_n]

def worst_symbol_contributors(events: List[AttributionTradeEvent], top_n: int = 10) -> List[AttributionContribution]:
    contributions = symbol_performance_attribution(events)
    # Sort ascending by net PnL to get worst
    return sorted(contributions, key=lambda x: x.net_pnl_usd)[:top_n]

def symbol_cost_drag_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    contributions = symbol_performance_attribution(events)
    summary = {}
    for c in contributions:
        drag = calculate_cost_drag_pct(c.gross_pnl_usd, c.total_cost_usd)
        summary[c.name] = drag
    return summary

def symbol_attribution_to_text(events: List[AttributionTradeEvent], top_n: int = 10) -> str:
    lines = []
    lines.append(f"--- Top {top_n} Symbol Contributors ---")
    top = top_symbol_contributors(events, top_n)
    for c in top:
        lines.append(f"{c.name}: Net PnL: ${c.net_pnl_usd:.2f} (Trades: {c.trade_count}, WR: {c.win_rate or 0:.1f}%)")

    lines.append(f"\n--- Worst {top_n} Symbol Contributors ---")
    worst = worst_symbol_contributors(events, top_n)
    for c in worst:
        lines.append(f"{c.name}: Net PnL: ${c.net_pnl_usd:.2f} (Trades: {c.trade_count}, WR: {c.win_rate or 0:.1f}%)")

    return "\n".join(lines)
