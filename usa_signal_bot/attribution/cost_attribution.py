"""Cost, slippage, and impact attribution calculators."""

from typing import Dict, List, Optional
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension, calculate_contribution_for_group

def calculate_cost_drag_pct(gross_pnl_usd: Optional[float], total_cost_usd: Optional[float]) -> Optional[float]:
    if gross_pnl_usd is None or total_cost_usd is None or gross_pnl_usd <= 0:
        return None
    return (total_cost_usd / gross_pnl_usd) * 100.0

def identify_cost_degraded_groups(contributions: List[AttributionContribution], cost_drag_threshold_pct: float = 50.0) -> List[AttributionContribution]:
    degraded = []
    for c in contributions:
        drag = calculate_cost_drag_pct(c.gross_pnl_usd, c.total_cost_usd)
        if drag is not None and drag >= cost_drag_threshold_pct:
            degraded.append(c)
        elif c.gross_pnl_usd > 0 and c.net_pnl_usd <= 0:
            # Turned winner into loser
            degraded.append(c)
    return degraded

def aggregate_cost_by_dimension(events: List[AttributionTradeEvent], dimension: AttributionDimension) -> List[AttributionContribution]:
    # Reuse PnL aggregator and sort by total cost instead
    contributions = aggregate_pnl_by_dimension(events, dimension)
    return sorted(contributions, key=lambda x: x.total_cost_usd, reverse=True)

def aggregate_cost_by_component(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    slippage_events = [e for e in events if e.slippage_cost_usd]
    impact_events = [e for e in events if e.market_impact_cost_usd]
    # Fee is inferred as total - slippage - impact
    fee_events = []
    for e in events:
        if e.total_cost_usd is not None:
            slip = e.slippage_cost_usd or 0.0
            imp = e.market_impact_cost_usd or 0.0
            fee = e.total_cost_usd - slip - imp
            if fee > 0:
                fee_events.append(e) # Not perfect, but provides a count proxy

    components = []
    total_net = sum(e.net_pnl_usd for e in events if e.net_pnl_usd is not None)

    if slippage_events:
        c = calculate_contribution_for_group("Slippage", AttributionDimension.COST_COMPONENT, slippage_events, total_net)
        c.total_cost_usd = sum(e.slippage_cost_usd for e in slippage_events if e.slippage_cost_usd)
        components.append(c)

    if impact_events:
        c = calculate_contribution_for_group("MarketImpact", AttributionDimension.COST_COMPONENT, impact_events, total_net)
        c.total_cost_usd = sum(e.market_impact_cost_usd for e in impact_events if e.market_impact_cost_usd)
        components.append(c)

    if fee_events:
        c = calculate_contribution_for_group("FeesAndCommissions", AttributionDimension.COST_COMPONENT, fee_events, total_net)
        c.total_cost_usd = sum((e.total_cost_usd or 0.0) - (e.slippage_cost_usd or 0.0) - (e.market_impact_cost_usd or 0.0) for e in events)
        components.append(c)

    return sorted(components, key=lambda x: x.total_cost_usd, reverse=True)

def cost_attribution_to_text(contributions: List[AttributionContribution], limit: int = 100) -> str:
    if not contributions:
        return "No cost contributions to display."

    dimension = contributions[0].dimension.value
    lines = [f"--- Cost Attribution by {dimension} ---"]
    for c in contributions[:limit]:
        drag = calculate_cost_drag_pct(c.gross_pnl_usd, c.total_cost_usd)
        drag_str = f"{drag:.1f}%" if drag is not None else "N/A"
        lines.append(
            f"{c.name}: Total Cost: ${c.total_cost_usd:.2f} | "
            f"Gross PnL: ${c.gross_pnl_usd:.2f} | Net PnL: ${c.net_pnl_usd:.2f} | Cost Drag: {drag_str}"
        )
    return "\n".join(lines)
