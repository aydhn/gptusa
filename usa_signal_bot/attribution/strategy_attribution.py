"""Strategy-level performance and cost attribution."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension
from usa_signal_bot.attribution.cost_attribution import identify_cost_degraded_groups

def strategy_performance_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_pnl_by_dimension(events, AttributionDimension.STRATEGY)

def strategy_cost_adjusted_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    # Returns the same list since total_cost_usd is already aggregated.
    # Provided for API parity and conceptual separation.
    return strategy_performance_attribution(events)

def strategy_win_rate_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    contributions = strategy_performance_attribution(events)
    return {c.name: c.win_rate for c in contributions}

def strategy_failure_candidates(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    contributions = strategy_performance_attribution(events)
    return identify_cost_degraded_groups(contributions)

def strategy_attribution_to_text(events: List[AttributionTradeEvent], limit: int = 50) -> str:
    contributions = strategy_performance_attribution(events)
    lines = ["--- Strategy Attribution ---"]
    for c in contributions[:limit]:
        drag = c.total_cost_usd / c.gross_pnl_usd * 100 if c.gross_pnl_usd else 0
        lines.append(f"{c.name}: Net PnL: ${c.net_pnl_usd:.2f} | Gross: ${c.gross_pnl_usd:.2f} | Cost: ${c.total_cost_usd:.2f} ({drag:.1f}%) | WR: {c.win_rate or 0:.1f}%")

    fails = strategy_failure_candidates(events)
    if fails:
        lines.append("\n--- Strategy Cost Failures (Degraded) ---")
        for f in fails:
            lines.append(f"{f.name}: Gross ${f.gross_pnl_usd:.2f} -> Net ${f.net_pnl_usd:.2f}")

    return "\n".join(lines)
