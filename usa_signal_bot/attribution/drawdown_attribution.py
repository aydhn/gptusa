"""Drawdown contribution and running equity tracking."""

from typing import Any, Dict, List
from collections import defaultdict
from usa_signal_bot.core.enums import (
    AttributionDimension,
    RiskContributionType,
    ContributionDirection,
)
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent,
    RiskAttributionContribution,
    create_risk_attribution_contribution_id,
)


def calculate_running_equity(
    events: List[AttributionTradeEvent], starting_equity: float = 100000.0
) -> List[Dict[str, Any]]:
    # Sort by timestamp if available, else retain input order
    sorted_events = sorted(events, key=lambda x: x.timestamp_utc or "")

    equity = starting_equity
    points = [
        {
            "timestamp": None,
            "equity": equity,
            "peak": equity,
            "drawdown": 0.0,
            "event_id": None,
        }
    ]

    peak = equity
    for e in sorted_events:
        net = e.net_pnl_usd or 0.0
        equity += net
        if equity > peak:
            peak = equity

        dd = peak - equity
        points.append(
            {
                "timestamp": e.timestamp_utc,
                "equity": equity,
                "peak": peak,
                "drawdown": dd,
                "event_id": e.event_id,
                "net_pnl_usd": net,
            }
        )
    return points


def calculate_event_drawdowns(
    equity_points: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    return [p for p in equity_points if p["event_id"] is not None]


def _get_dimension_key(
    e: AttributionTradeEvent, dimension: AttributionDimension
) -> str:
    if dimension == AttributionDimension.SYMBOL:
        return e.symbol or "UNKNOWN"
    elif dimension == AttributionDimension.STRATEGY:
        return e.strategy_name or "UNKNOWN"
    elif dimension == AttributionDimension.SECTOR:
        return e.sector or "UNKNOWN"
    elif dimension == AttributionDimension.CLUSTER:
        return e.cluster or "UNKNOWN"
    return "UNKNOWN"


def drawdown_contribution_by_dimension(
    events: List[AttributionTradeEvent], dimension: AttributionDimension
) -> List[RiskAttributionContribution]:
    groups = defaultdict(float)
    for e in events:
        key = _get_dimension_key(e, dimension)

        # Drawdown proxy: sum of negative net PnL
        net = e.net_pnl_usd or 0.0
        if net < 0:
            groups[key] += abs(net)

    contribs = []
    for name, dd_sum in groups.items():
        contribs.append(
            RiskAttributionContribution(
                contribution_id=create_risk_attribution_contribution_id(name),
                risk_type=RiskContributionType.DRAWDOWN,
                dimension=dimension,
                name=name,
                drawdown_contribution_usd=dd_sum,
                contribution_direction=(
                    ContributionDirection.NEGATIVE
                    if dd_sum > 0
                    else ContributionDirection.NEUTRAL
                ),
            )
        )
    return sorted(
        contribs, key=lambda x: x.drawdown_contribution_usd or 0.0, reverse=True
    )


def identify_drawdown_contributors(
    events: List[AttributionTradeEvent], top_n: int = 10
) -> List[RiskAttributionContribution]:
    return drawdown_contribution_by_dimension(events, AttributionDimension.SYMBOL)[
        :top_n
    ]


def drawdown_attribution_to_text(
    contributions: List[RiskAttributionContribution], limit: int = 50
) -> str:
    lines = [f"--- Drawdown Attribution ---"]
    for c in contributions[:limit]:
        lines.append(
            f"{c.name}: Drawdown Contribution: ${c.drawdown_contribution_usd or 0.0:.2f}"
        )
    return "\n".join(lines)
