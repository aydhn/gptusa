"""Gross and net PnL attribution calculators."""

from typing import List
from collections import defaultdict

from usa_signal_bot.core.enums import (
    AttributionDimension,
    ContributionDirection,
    AttributionQuality,
)
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent,
    AttributionContribution,
    create_attribution_contribution_id,
)


def calculate_win_rate(events: List[AttributionTradeEvent]) -> float | None:
    win = sum(1 for e in events if e.net_pnl_usd is not None and e.net_pnl_usd > 0)
    loss = sum(1 for e in events if e.net_pnl_usd is not None and e.net_pnl_usd <= 0)
    total = win + loss
    if total == 0:
        return None
    return (win / total) * 100.0


def classify_contribution_direction(
    net_pnl_usd: float | None,
) -> ContributionDirection:
    if net_pnl_usd is None:
        return ContributionDirection.INSUFFICIENT_DATA
    if net_pnl_usd > 0:
        return ContributionDirection.POSITIVE
    if net_pnl_usd < 0:
        return ContributionDirection.NEGATIVE
    return ContributionDirection.NEUTRAL


def classify_attribution_quality(
    events: List[AttributionTradeEvent],
) -> AttributionQuality:
    valid_pnl = sum(1 for e in events if e.net_pnl_usd is not None)
    if valid_pnl == 0:
        return AttributionQuality.INSUFFICIENT_DATA
    if valid_pnl < 10:
        return AttributionQuality.WEAK
    if valid_pnl < 30:
        return AttributionQuality.NOISY
    if valid_pnl >= 30:
        return AttributionQuality.HIGH
    return AttributionQuality.ACCEPTABLE


def calculate_contribution_for_group(
    name: str,
    dimension: AttributionDimension,
    events: List[AttributionTradeEvent],
    total_net_pnl: float | None = None,
) -> AttributionContribution:
    gross = 0.0
    net = 0.0
    cost = 0.0
    win_count = 0
    loss_count = 0

    for e in events:
        if e.gross_pnl_usd is not None:
            gross += e.gross_pnl_usd

        net_val = e.net_pnl_usd
        if net_val is not None:
            net += net_val
            if net_val > 0:
                win_count += 1
            else:
                loss_count += 1

        if e.total_cost_usd is not None:
            cost += e.total_cost_usd

    trade_count = len(events)

    win_rate = calculate_win_rate(events)
    avg_net = net / trade_count if trade_count > 0 else None

    pct_total = None
    if total_net_pnl and total_net_pnl != 0:
        pct_total = (net / total_net_pnl) * 100.0

    quality = classify_attribution_quality(events)
    direction = classify_contribution_direction(net)

    warnings = []
    if quality in [AttributionQuality.WEAK, AttributionQuality.NOISY]:
        warnings.append("Low sample size for attribution group.")

    return AttributionContribution(
        contribution_id=create_attribution_contribution_id(name),
        dimension=dimension,
        name=name,
        contribution_direction=direction,
        gross_pnl_usd=gross,
        net_pnl_usd=net,
        total_cost_usd=cost,
        trade_count=trade_count,
        win_count=win_count,
        loss_count=loss_count,
        win_rate=win_rate,
        avg_net_pnl_usd=avg_net,
        contribution_pct_total=pct_total,
        quality=quality,
        warnings=warnings,
    )


def _extract_dimension_key(
    e: AttributionTradeEvent, dimension: AttributionDimension
) -> str:
    if dimension == AttributionDimension.SYMBOL:
        return e.symbol or "UNKNOWN"
    if dimension == AttributionDimension.STRATEGY:
        return e.strategy_name or "UNKNOWN"
    if dimension == AttributionDimension.SIGNAL_FAMILY:
        return e.signal_family or "UNKNOWN"
    if dimension == AttributionDimension.SECTOR:
        return e.sector or "UNKNOWN"
    if dimension == AttributionDimension.CLUSTER:
        return e.cluster or "UNKNOWN"
    if dimension == AttributionDimension.REGIME:
        return e.regime_label or "UNKNOWN"
    if dimension == AttributionDimension.SIDE:
        return e.side or "UNKNOWN"
    if dimension == AttributionDimension.SIZING_STATUS:
        return e.sizing_status or "UNKNOWN"
    if dimension == AttributionDimension.REBALANCE_ACTION:
        return e.rebalance_action_type or "UNKNOWN"
    return "UNKNOWN"


def aggregate_pnl_by_dimension(
    events: List[AttributionTradeEvent], dimension: AttributionDimension
) -> List[AttributionContribution]:
    groups = defaultdict(list)

    for e in events:
        key = _extract_dimension_key(e, dimension)
        groups[key].append(e)

    total_net_pnl = sum(e.net_pnl_usd for e in events if e.net_pnl_usd is not None)

    contributions = []
    for name, group_events in groups.items():
        contributions.append(
            calculate_contribution_for_group(
                name, dimension, group_events, total_net_pnl
            )
        )

    return sorted(contributions, key=lambda x: x.net_pnl_usd, reverse=True)


def pnl_attribution_to_text(
    contributions: List[AttributionContribution], limit: int = 100
) -> str:
    if not contributions:
        return "No contributions to display."

    dimension = contributions[0].dimension.value
    lines = [f"--- PnL Attribution by {dimension} ---"]
    for c in contributions[:limit]:
        wr = f"{c.win_rate:.1f}%" if c.win_rate is not None else "N/A"
        pct = (
            f"{c.contribution_pct_total:.1f}%"
            if c.contribution_pct_total is not None
            else "N/A"
        )
        lines.append(
            f"[{c.contribution_direction.value[:3]}] {c.name}: Net PnL: ${c.net_pnl_usd:.2f} "
            f"(Gross: ${c.gross_pnl_usd:.2f}, Cost: ${c.total_cost_usd:.2f}) | "
            f"Trades: {c.trade_count} | WR: {wr} | Share: {pct}"
        )
    return "\n".join(lines)
