"""Attribution summary ranking."""

from typing import Any, Dict, List
from usa_signal_bot.attribution.attribution_models import AttributionContribution, RiskAttributionContribution, SignalContribution

def rank_contributions_by_net_pnl(contributions: List[AttributionContribution], descending: bool = True) -> List[AttributionContribution]:
    return sorted(contributions, key=lambda x: x.net_pnl_usd, reverse=descending)

def rank_contributions_by_cost_drag(contributions: List[AttributionContribution], descending: bool = True) -> List[AttributionContribution]:
    def drag(c):
        return (c.total_cost_usd / c.gross_pnl_usd) if c.gross_pnl_usd and c.gross_pnl_usd > 0 else 0.0
    return sorted(contributions, key=drag, reverse=descending)

def rank_risk_contributions(contributions: List[RiskAttributionContribution], descending: bool = True) -> List[RiskAttributionContribution]:
    def val(c):
        return c.drawdown_contribution_usd or c.volatility_contribution_proxy or c.concentration_contribution_pct or 0.0
    return sorted(contributions, key=val, reverse=descending)

def rank_signal_contributions(contributions: List[SignalContribution], descending: bool = True) -> List[SignalContribution]:
    return sorted(contributions, key=lambda x: x.net_pnl_usd, reverse=descending)

def attribution_ranking_summary(
    contributions: List[AttributionContribution],
    risk_contributions: List[RiskAttributionContribution],
    signal_contributions: List[SignalContribution]
) -> Dict[str, Any]:

    top_perf = rank_contributions_by_net_pnl(contributions)
    worst_perf = rank_contributions_by_net_pnl(contributions, descending=False)

    top_risk = rank_risk_contributions(risk_contributions)

    return {
        "top_performer": top_perf[0].name if top_perf else None,
        "worst_performer": worst_perf[0].name if worst_perf else None,
        "top_risk_contributor": top_risk[0].name if top_risk else None,
        "top_signal": signal_contributions[0].signal_id if signal_contributions else None
    }

def attribution_ranking_summary_to_text(summary: Dict[str, Any]) -> str:
    lines = [
        "--- Attribution Ranking Summary ---",
        f"Top Performer: {summary.get('top_performer', 'N/A')}",
        f"Worst Performer: {summary.get('worst_performer', 'N/A')}",
        f"Top Risk Contributor: {summary.get('top_risk_contributor', 'N/A')}",
        f"Top Signal: {summary.get('top_signal', 'N/A')}"
    ]
    return "\n".join(lines)
