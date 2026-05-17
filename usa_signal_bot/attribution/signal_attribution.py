"""Signal contribution and quality mapping."""

from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import AttributionDimension, SignalContributionStatus
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, SignalContribution, create_signal_contribution_id
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension

def convert_contribution_to_signal(c, status: SignalContributionStatus, family: Optional[str] = None, strat: Optional[str] = None, sig_id: Optional[str] = None) -> SignalContribution:
    return SignalContribution(
        contribution_id=create_signal_contribution_id(c.name),
        signal_family=family or (c.name if c.dimension == AttributionDimension.SIGNAL_FAMILY else None),
        strategy_name=strat or (c.name if c.dimension == AttributionDimension.STRATEGY else None),
        signal_id=sig_id,
        status=status,
        gross_pnl_usd=c.gross_pnl_usd,
        net_pnl_usd=c.net_pnl_usd,
        cost_drag_usd=c.total_cost_usd,
        trade_count=c.trade_count,
        win_rate=c.win_rate
    )

def classify_signal_contribution(net: float, gross: float, cost: float) -> SignalContributionStatus:
    if net > 0:
        return SignalContributionStatus.CONTRIBUTIVE
    if gross > 0 and net <= 0:
        return SignalContributionStatus.COST_DEGRADED
    if net < 0:
        return SignalContributionStatus.DETRIMENTAL
    return SignalContributionStatus.NEUTRAL

def build_signal_contributions(events: List[AttributionTradeEvent], dimension: AttributionDimension) -> List[SignalContribution]:
    contribs = aggregate_pnl_by_dimension(events, dimension)
    result = []
    for c in contribs:
        status = classify_signal_contribution(c.net_pnl_usd, c.gross_pnl_usd, c.total_cost_usd)
        result.append(convert_contribution_to_signal(c, status))
    return result

def signal_contribution_by_family(events: List[AttributionTradeEvent]) -> List[SignalContribution]:
    return build_signal_contributions(events, AttributionDimension.SIGNAL_FAMILY)

def signal_contribution_by_strategy(events: List[AttributionTradeEvent]) -> List[SignalContribution]:
    return build_signal_contributions(events, AttributionDimension.STRATEGY)

def signal_contribution_by_id(events: List[AttributionTradeEvent]) -> List[SignalContribution]:
    # Custom aggregation for signal IDs
    from collections import defaultdict
    from usa_signal_bot.attribution.pnl_attribution import calculate_contribution_for_group
    groups = defaultdict(list)
    for e in events:
        key = e.signal_id or "UNKNOWN"
        groups[key].append(e)

    result = []
    total_net = sum(e.net_pnl_usd for e in events if e.net_pnl_usd)
    for name, grp in groups.items():
        c = calculate_contribution_for_group(name, AttributionDimension.UNKNOWN, grp, total_net)
        status = classify_signal_contribution(c.net_pnl_usd, c.gross_pnl_usd, c.total_cost_usd)
        result.append(convert_contribution_to_signal(c, status, sig_id=name))

    return sorted(result, key=lambda x: x.net_pnl_usd, reverse=True)

def identify_detrimental_signals(contributions: List[SignalContribution]) -> List[SignalContribution]:
    return [c for c in contributions if c.status in (SignalContributionStatus.DETRIMENTAL, SignalContributionStatus.COST_DEGRADED)]

def signal_score_alignment_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    # Mock summary since we don't carry full quality metadata in the event currently
    return {"alignment_status": "OK", "score_correlation_proxy": 0.5}

def signal_contribution_to_text(contributions: List[SignalContribution], limit: int = 100) -> str:
    lines = [f"--- Signal Contributions ({len(contributions)} items) ---"]
    for c in contributions[:limit]:
        name = c.signal_id or c.signal_family or c.strategy_name or "UNKNOWN"
        lines.append(f"[{c.status.value}] {name}: Net PnL: ${c.net_pnl_usd:.2f} (Cost Drag: ${c.cost_drag_usd:.2f})")
    return "\n".join(lines)
