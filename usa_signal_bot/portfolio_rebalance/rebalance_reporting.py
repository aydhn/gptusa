from typing import Any, Dict, List
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, DriftMeasurement,
    RebalanceAction, TurnoverAssessment, RebalancePlan, RebalanceReview,
    PortfolioPosition
)
from usa_signal_bot.portfolio_rebalance.portfolio_state import current_portfolio_state_to_text
from usa_signal_bot.portfolio_rebalance.target_extractor import target_portfolio_state_to_text
from usa_signal_bot.portfolio_rebalance.drift_calculator import drift_measurements_to_text
from usa_signal_bot.portfolio_rebalance.turnover_control import turnover_assessment_to_text

def portfolio_position_to_text(item: PortfolioPosition) -> str:
    return f"{item.symbol}: {item.quantity} units @ ${item.market_value_usd:.2f} ({item.side or 'LONG'})"

def rebalance_action_to_text(item: RebalanceAction) -> str:
    delta = f"${item.delta_notional_usd:.2f}" if item.delta_notional_usd is not None else "N/A"
    return f"{item.symbol} [{item.action_type.value}]: Delta {delta} | Status: {item.status.value}"

def rebalance_plan_to_text(item: RebalancePlan, limit: int = 100) -> str:
    lines = [
        f"--- Rebalance Plan: {item.plan_id} ---",
        f"Mode: {item.mode.value} | Status: {item.status.value}",
        f"Total Delta Notional: ${item.total_delta_notional_usd or 0:.2f}",
        f"Actions: {item.proposed_action_count} proposed, {item.suppressed_action_count} suppressed, {item.blocked_action_count} blocked"
    ]
    if item.turnover_assessment:
        lines.append(turnover_assessment_to_text(item.turnover_assessment))

    if item.actions:
        lines.append(f"\nProposed Actions (showing up to {limit}):")
        proposed = [a for a in item.actions if a.status.value == "PROPOSED"]
        for a in proposed[:limit]:
            lines.append(f"  {rebalance_action_to_text(a)}")

        suppressed = [a for a in item.actions if "SUPPRESSED" in a.status.value]
        if suppressed:
            lines.append(f"\nSuppressed Actions ({len(suppressed)}):")
            for a in suppressed[:limit]:
                lines.append(f"  {rebalance_action_to_text(a)}")

    return "\n".join(lines)

def rebalance_review_to_text(item: RebalanceReview, limit: int = 100) -> str:
    lines = [
        f"=== REBALANCE REVIEW: {item.review_id} ===",
        f"Report Type: {item.report_type.value}",
        f"Date: {item.created_at_utc}"
    ]

    if item.current_state:
        lines.append("\n" + current_portfolio_state_to_text(item.current_state))

    if item.target_state:
        lines.append("\n" + target_portfolio_state_to_text(item.target_state))

    if item.drift_measurements:
        lines.append("\n" + drift_measurements_to_text(item.drift_measurements, limit))

    if item.plan:
        lines.append("\n" + rebalance_plan_to_text(item.plan, limit))

    lines.append("\n" + rebalance_limitations_text())

    return "\n".join(lines)

def rebalance_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return (
        f"Rebalance Store Summary:\n"
        f"  Current States: {summary.get('current_states', 0)}\n"
        f"  Target States: {summary.get('target_states', 0)}\n"
        f"  Plans: {summary.get('plans', 0)}\n"
        f"  Reviews: {summary.get('reviews', 0)}"
    )

def rebalance_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- This rebalance plan is local metadata for backtest and paper tracking.\n"
        "- It does NOT generate or send live broker orders.\n"
        "- Output does NOT constitute financial or investment advice.\n"
        "- A 'PASS' or 'PROPOSED' status is NOT a live trading approval."
    )
