"""Regime attribution and transition risk."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import AttributionDimension, RiskContributionType, ContributionDirection
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionContribution, RiskAttributionContribution, create_risk_attribution_contribution_id
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension
from usa_signal_bot.attribution.cost_attribution import aggregate_cost_by_dimension

def regime_performance_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_pnl_by_dimension(events, AttributionDimension.REGIME)

def regime_cost_attribution(events: List[AttributionTradeEvent]) -> List[AttributionContribution]:
    return aggregate_cost_by_dimension(events, AttributionDimension.REGIME)

def regime_drawdown_proxy(events: List[AttributionTradeEvent]) -> List[RiskAttributionContribution]:
    # Simple proxy: if net PnL is negative, assume it contributes to drawdown
    regimes = regime_performance_attribution(events)
    risk_contribs = []

    for r in regimes:
        dd = abs(r.net_pnl_usd) if r.net_pnl_usd < 0 else 0.0
        risk_contribs.append(RiskAttributionContribution(
            contribution_id=create_risk_attribution_contribution_id(f"regime_{r.name}"),
            risk_type=RiskContributionType.REGIME_TRANSITION,
            dimension=AttributionDimension.REGIME,
            name=r.name,
            drawdown_contribution_usd=dd,
            contribution_direction=ContributionDirection.NEGATIVE if dd > 0 else ContributionDirection.NEUTRAL
        ))

    return sorted(risk_contribs, key=lambda x: x.drawdown_contribution_usd or 0.0, reverse=True)

def regime_contribution_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    perf = regime_performance_attribution(events)
    return {
        "best_regime": perf[0].name if perf else None,
        "best_regime_pnl": perf[0].net_pnl_usd if perf else None,
        "worst_regime": perf[-1].name if perf else None,
        "worst_regime_pnl": perf[-1].net_pnl_usd if perf else None
    }

def regime_attribution_to_text(events: List[AttributionTradeEvent]) -> str:
    perf = regime_performance_attribution(events)
    lines = ["--- Regime Attribution ---"]
    for c in perf:
        lines.append(f"{c.name}: Net PnL: ${c.net_pnl_usd:.2f} (Gross: ${c.gross_pnl_usd:.2f}, Cost: ${c.total_cost_usd:.2f})")
    return "\n".join(lines)
