"""Volatility, concentration, and cost fragility proxy attribution."""

from typing import List
from collections import defaultdict
from usa_signal_bot.core.enums import AttributionDimension, RiskContributionType, ContributionDirection
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, RiskAttributionContribution, create_risk_attribution_contribution_id

def risk_attribution_by_dimension(events: List[AttributionTradeEvent], dimension: AttributionDimension) -> List[RiskAttributionContribution]:
    # Placeholder for general risk attribution
    return volatility_contribution_proxy(events, dimension)

def volatility_contribution_proxy(events: List[AttributionTradeEvent], dimension: AttributionDimension) -> List[RiskAttributionContribution]:
    # Proxy: sum of absolute PnL / total absolute PnL
    groups = defaultdict(float)
    total_abs_pnl = sum(abs(e.net_pnl_usd or 0.0) for e in events)

    if total_abs_pnl == 0:
        return []

    for e in events:
        key = e.symbol if dimension == AttributionDimension.SYMBOL else (e.strategy_name or "UNKNOWN")
        groups[key] += abs(e.net_pnl_usd or 0.0)

    contribs = []
    for name, abs_pnl in groups.items():
        contribs.append(RiskAttributionContribution(
            contribution_id=create_risk_attribution_contribution_id(name),
            risk_type=RiskContributionType.VOLATILITY,
            dimension=dimension,
            name=name,
            volatility_contribution_proxy=(abs_pnl / total_abs_pnl) * 100.0,
            contribution_direction=ContributionDirection.MIXED
        ))
    return sorted(contribs, key=lambda x: x.volatility_contribution_proxy or 0.0, reverse=True)

def concentration_risk_contribution_proxy(events: List[AttributionTradeEvent], dimension: AttributionDimension) -> List[RiskAttributionContribution]:
    groups = defaultdict(float)
    total_notional = sum(e.notional_usd or 0.0 for e in events)

    if total_notional == 0:
        return []

    for e in events:
        key = e.symbol if dimension == AttributionDimension.SYMBOL else (e.strategy_name or "UNKNOWN")
        groups[key] += (e.notional_usd or 0.0)

    contribs = []
    for name, notional in groups.items():
        contribs.append(RiskAttributionContribution(
            contribution_id=create_risk_attribution_contribution_id(name),
            risk_type=RiskContributionType.CONCENTRATION,
            dimension=dimension,
            name=name,
            concentration_contribution_pct=(notional / total_notional) * 100.0,
            contribution_direction=ContributionDirection.MIXED
        ))
    return sorted(contribs, key=lambda x: x.concentration_contribution_pct or 0.0, reverse=True)

def liquidity_risk_contribution_proxy(events: List[AttributionTradeEvent]) -> List[RiskAttributionContribution]:
    # Mock proxy
    return []

def cost_fragility_contribution_proxy(events: List[AttributionTradeEvent]) -> List[RiskAttributionContribution]:
    # Mock proxy
    return []

def risk_attribution_to_text(contributions: List[RiskAttributionContribution], limit: int = 100) -> str:
    lines = ["--- Risk Attribution ---"]
    for c in contributions[:limit]:
        vol = f"{c.volatility_contribution_proxy:.1f}%" if c.volatility_contribution_proxy is not None else "N/A"
        conc = f"{c.concentration_contribution_pct:.1f}%" if c.concentration_contribution_pct is not None else "N/A"
        lines.append(f"[{c.risk_type.value}] {c.name}: Volatility Proxy: {vol} | Concentration: {conc}")
    return "\n".join(lines)
