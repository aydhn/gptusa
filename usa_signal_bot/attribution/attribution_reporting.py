"""Formatting and reporting for attribution data."""

from typing import Any, Dict, List
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent, AttributionContribution, RiskAttributionContribution,
    SignalContribution, AttributionScorecard, AttributionReview
)
from usa_signal_bot.attribution.pnl_attribution import pnl_attribution_to_text
from usa_signal_bot.attribution.risk_attribution import risk_attribution_to_text
from usa_signal_bot.attribution.signal_attribution import signal_contribution_to_text
from usa_signal_bot.attribution.attribution_scorecard import attribution_scorecard_to_text

def attribution_trade_event_to_text(item: AttributionTradeEvent) -> str:
    return f"{item.symbol} {item.side or 'UNK'} | Net: ${item.net_pnl_usd or 0.0:.2f} | Strat: {item.strategy_name or 'UNK'}"

def attribution_contribution_to_text(item: AttributionContribution) -> str:
    return f"{item.dimension.value}: {item.name} | Net: ${item.net_pnl_usd:.2f} | WR: {item.win_rate or 0.0:.1f}%"

def risk_attribution_contribution_to_text(item: RiskAttributionContribution) -> str:
    return f"{item.dimension.value}: {item.name} | {item.risk_type.value}"

def signal_contribution_to_text_item(item: SignalContribution) -> str:
    name = item.signal_id or item.signal_family or item.strategy_name or "UNKNOWN"
    return f"{name} | Status: {item.status.value} | Net: ${item.net_pnl_usd:.2f}"

def attribution_review_to_text(item: AttributionReview, limit: int = 100) -> str:
    lines = [
        f"=== ATTRIBUTION REVIEW: {item.review_id} ===",
        f"Report Type: {item.report_type.value}",
        f"Created At: {item.created_at_utc}"
    ]

    if item.scorecard:
        lines.append("\n" + attribution_scorecard_to_text(item.scorecard))

    lines.append("\n" + pnl_attribution_to_text(item.performance_contributions, limit))
    lines.append("\n" + risk_attribution_to_text(item.risk_contributions, limit))
    lines.append("\n" + signal_contribution_to_text(item.signal_contributions, limit))

    lines.append("\n" + attribution_limitations_text())
    return "\n".join(lines)

def attribution_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Attribution Store Summary:\nTotal Reviews: {summary.get('reviews_count')}\nLatest Review: {summary.get('latest_review')}"

def attribution_limitations_text() -> str:
    return (
        "--- ATTRIBUTION LIMITATIONS ---\n"
        "1. This is local backtest/paper attribution analytics ONLY.\n"
        "2. These metrics do NOT represent real broker performance.\n"
        "3. High attribution scores or positive signal contributions are NOT investment advice.\n"
        "4. A PASS or high score is NOT a live trading approval.\n"
        "5. Past performance attribution does not guarantee future results."
    )
