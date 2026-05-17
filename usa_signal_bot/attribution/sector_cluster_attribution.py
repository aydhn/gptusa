"""Sector and cluster performance attribution."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension
from usa_signal_bot.attribution.cost_attribution import calculate_cost_drag_pct

def sector_performance_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_pnl_by_dimension(events, AttributionDimension.SECTOR)

def cluster_performance_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_pnl_by_dimension(events, AttributionDimension.CLUSTER)

def sector_cluster_cost_drag_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    sectors = sector_performance_attribution(events)
    clusters = cluster_performance_attribution(events)

    summary = {"sectors": {}, "clusters": {}}
    for c in sectors:
        summary["sectors"][c.name] = calculate_cost_drag_pct(c.gross_pnl_usd, c.total_cost_usd)
    for c in clusters:
        summary["clusters"][c.name] = calculate_cost_drag_pct(c.gross_pnl_usd, c.total_cost_usd)
    return summary

def sector_cluster_contribution_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    sectors = sector_performance_attribution(events)
    clusters = cluster_performance_attribution(events)
    return {
        "top_sector": sectors[0].name if sectors else None,
        "top_sector_pnl": sectors[0].net_pnl_usd if sectors else None,
        "worst_sector": sectors[-1].name if sectors else None,
        "worst_sector_pnl": sectors[-1].net_pnl_usd if sectors else None,
        "top_cluster": clusters[0].name if clusters else None,
        "worst_cluster": clusters[-1].name if clusters else None
    }

def sector_cluster_attribution_to_text(events: List[AttributionTradeEvent]) -> str:
    sectors = sector_performance_attribution(events)
    clusters = cluster_performance_attribution(events)

    lines = ["--- Sector Attribution ---"]
    for c in sectors:
        lines.append(f"{c.name}: Net PnL: ${c.net_pnl_usd:.2f} (Trades: {c.trade_count})")

    lines.append("\n--- Cluster Attribution ---")
    for c in clusters:
        lines.append(f"{c.name}: Net PnL: ${c.net_pnl_usd:.2f} (Trades: {c.trade_count})")

    return "\n".join(lines)
