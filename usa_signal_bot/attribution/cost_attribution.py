"""Cost, slippage, and impact attribution calculators."""

from typing import List
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent,
    AttributionContribution,
)
from usa_signal_bot.attribution.pnl_attribution import (
    aggregate_pnl_by_dimension,
    calculate_contribution_for_group,
)


def calculate_cost_drag_pct(
    gross_pnl_usd: float | None, total_cost_usd: float | None
) -> float | None:
    if gross_pnl_usd is None or total_cost_usd is None or gross_pnl_usd <= 0:
        return None
    return (total_cost_usd / gross_pnl_usd) * 100.0


def identify_cost_degraded_groups(
    contributions: List[AttributionContribution], cost_drag_threshold_pct: float = 50.0
) -> List[AttributionContribution]:
    degraded = []
    for c in contributions:
        drag = calculate_cost_drag_pct(c.gross_pnl_usd, c.total_cost_usd)
        if drag is not None and drag >= cost_drag_threshold_pct:
            degraded.append(c)
        elif c.gross_pnl_usd > 0 and c.net_pnl_usd <= 0:
            # Turned winner into loser
            degraded.append(c)
    return degraded


def aggregate_cost_by_dimension(
    events: List[AttributionTradeEvent], dimension: AttributionDimension
) -> List[AttributionContribution]:
    # Reuse PnL aggregator and sort by total cost instead
    contributions = aggregate_pnl_by_dimension(events, dimension)
    return sorted(contributions, key=lambda x: x.total_cost_usd, reverse=True)


def aggregate_cost_by_component(
    events: List[AttributionTradeEvent],
) -> List[AttributionContribution]:
    slippage_events = []
    impact_events = []
    fee_events = []

    total_net = 0.0
    total_slippage_cost = 0.0
    total_impact_cost = 0.0
    total_fee_cost = 0.0

    for e in events:
        if e.net_pnl_usd is not None:
            total_net += e.net_pnl_usd

        slip = e.slippage_cost_usd
        if slip:
            slippage_events.append(e)
            total_slippage_cost += slip

        imp = e.market_impact_cost_usd
        if imp:
            impact_events.append(e)
            total_impact_cost += imp

        total_cost = e.total_cost_usd
        if total_cost is not None:
            slip_val = slip or 0.0
            imp_val = imp or 0.0
            fee = total_cost - slip_val - imp_val
            if fee > 0:
                fee_events.append(e)

        total_fee_cost += (total_cost or 0.0) - (slip or 0.0) - (imp or 0.0)

    components = []

    if slippage_events:
        c = calculate_contribution_for_group(
            "Slippage", AttributionDimension.COST_COMPONENT, slippage_events, total_net
        )
        c.total_cost_usd = total_slippage_cost
        components.append(c)

    if impact_events:
        c = calculate_contribution_for_group(
            "MarketImpact",
            AttributionDimension.COST_COMPONENT,
            impact_events,
            total_net,
        )
        c.total_cost_usd = total_impact_cost
        components.append(c)

    if fee_events:
        c = calculate_contribution_for_group(
            "FeesAndCommissions",
            AttributionDimension.COST_COMPONENT,
            fee_events,
            total_net,
        )
        c.total_cost_usd = total_fee_cost
        components.append(c)

    return sorted(components, key=lambda x: x.total_cost_usd, reverse=True)


def cost_attribution_to_text(
    contributions: List[AttributionContribution], limit: int = 100
) -> str:
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
